#!/usr/bin/env python3
"""Peer Codex sessions over the app-server protocol.

  codex_peer.py new --name NAME [--cwd DIR] [--model M] [--effort E]
                    [--sandbox S] [--approval A] [--timeout SEC] PROMPT
  codex_peer.py send [--effort E] [--timeout SEC] ID_OR_NAME MESSAGE
  codex_peer.py read ID_OR_NAME
  codex_peer.py stop

One codex app-server per machine listens on ~/.claude/codex-peer.sock. `new`
and `send` start it when the socket does not answer. Exit 0 on success, 1 on
error, 2 when a turn outlives --timeout (the turn keeps running; use `read`).
"""

import argparse
import base64
import itertools
import json
import os
import re
import shutil
import signal
import socket
import struct
import subprocess
import sys
import time

CLAUDE_DIR = os.path.expanduser("~/.claude")
SOCKET_PATH = os.path.join(CLAUDE_DIR, "codex-peer.sock")
LOG_PATH = os.path.join(CLAUDE_DIR, "codex-peer.log")
PID_PATH = os.path.join(CLAUDE_DIR, "codex-peer.pid")
CLIENT_NAME = "spin-peer-codex-session"
CLIENT_VERSION = "0.1.0"
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
START_WAIT_SECONDS = 30


class Timeout(Exception):
    pass


class WebSocket:
    def __init__(self, sock):
        self.sock = sock
        self.buf = b""
        key = base64.b64encode(os.urandom(16)).decode()
        self.sock.sendall(
            (
                "GET / HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
            ).encode()
        )
        while b"\r\n\r\n" not in self.buf:
            self._fill()
        head, _, self.buf = self.buf.partition(b"\r\n\r\n")
        if b" 101 " not in head.split(b"\r\n")[0]:
            raise RuntimeError("websocket upgrade rejected: " + head.decode(errors="replace"))

    def _fill(self):
        try:
            chunk = self.sock.recv(65536)
        except socket.timeout:
            raise Timeout()
        if not chunk:
            raise EOFError("app-server closed the connection")
        self.buf += chunk

    def _need(self, n):
        while len(self.buf) < n:
            self._fill()

    def send_text(self, text):
        payload = text.encode()
        mask = os.urandom(4)
        n = len(payload)
        header = bytearray([0x81])
        if n < 126:
            header.append(0x80 | n)
        elif n < 65536:
            header.append(0x80 | 126)
            header += struct.pack(">H", n)
        else:
            header.append(0x80 | 127)
            header += struct.pack(">Q", n)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(bytes(header) + mask + masked)

    def _read_frame(self):
        self._need(2)
        b0, b1 = self.buf[0], self.buf[1]
        fin, opcode, masked, length = b0 & 0x80, b0 & 0x0F, b1 & 0x80, b1 & 0x7F
        offset = 2
        if length == 126:
            self._need(offset + 2)
            length = struct.unpack(">H", self.buf[offset:offset + 2])[0]
            offset += 2
        elif length == 127:
            self._need(offset + 8)
            length = struct.unpack(">Q", self.buf[offset:offset + 8])[0]
            offset += 8
        mask = None
        if masked:
            self._need(offset + 4)
            mask = self.buf[offset:offset + 4]
            offset += 4
        self._need(offset + length)
        data = self.buf[offset:offset + length]
        if mask:
            data = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
        self.buf = self.buf[offset + length:]
        return fin, opcode, data

    def recv_text(self):
        parts = b""
        while True:
            fin, opcode, data = self._read_frame()
            if opcode == 0x8:
                raise EOFError("app-server sent a close frame")
            if opcode == 0x9:
                self.sock.sendall(bytes([0x8A, 0x80]) + os.urandom(4))
                continue
            if opcode == 0xA:
                continue
            parts += data
            if fin:
                return parts.decode()


def log(message):
    print(message, file=sys.stderr, flush=True)


def answer_server_request(method, params):
    if method == "currentTime/read":
        return {"currentTimeAt": int(time.time())}
    if method in ("item/commandExecution/requestApproval", "item/fileChange/requestApproval"):
        return {"decision": "decline"}
    if method in ("execCommandApproval", "applyPatchApproval"):
        return {"decision": "denied"}
    if method == "item/tool/requestUserInput":
        return {"answers": {}}
    if method == "mcpServer/elicitation/request":
        return {"action": "decline"}
    if method == "item/permissions/requestApproval":
        return {"permissions": {}}
    return None


class Client:
    def __init__(self, path, deadline=None):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(path)
        self.sock = sock
        self.ws = WebSocket(sock)
        self.ids = itertools.count(1)
        self.deadline = deadline

    def _arm_timeout(self):
        if self.deadline is None:
            self.sock.settimeout(None)
            return
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise Timeout()
        self.sock.settimeout(remaining)

    def send(self, obj):
        self.ws.send_text(json.dumps(obj))

    def recv(self):
        self._arm_timeout()
        return json.loads(self.ws.recv_text())

    def request(self, method, params, on_notification=None):
        rid = next(self.ids)
        self.send({"jsonrpc": "2.0", "id": rid, "method": method, "params": params})
        while True:
            msg = self.recv()
            if msg.get("id") == rid and ("result" in msg or "error" in msg):
                if "error" in msg:
                    raise RuntimeError(f"{method} failed: {json.dumps(msg['error'])}")
                return msg["result"]
            self.dispatch(msg, on_notification)

    def dispatch(self, msg, on_notification):
        if "method" not in msg:
            return
        if "id" in msg:
            reply = answer_server_request(msg["method"], msg.get("params") or {})
            log(f"peer asked {msg['method']}; answered {json.dumps(reply)}")
            if reply is None:
                self.send({"jsonrpc": "2.0", "id": msg["id"], "error": {"code": -32601, "message": "unsupported by codex_peer"}})
            else:
                self.send({"jsonrpc": "2.0", "id": msg["id"], "result": reply})
        elif on_notification:
            on_notification(msg)

    def initialize(self):
        result = self.request(
            "initialize",
            {"clientInfo": {"name": CLIENT_NAME, "version": CLIENT_VERSION}, "capabilities": {"experimentalApi": True}},
        )
        self.send({"jsonrpc": "2.0", "method": "initialized", "params": {}})
        return result

    def run_turn(self, thread_id, prompt, effort):
        messages = []
        state = {"done": False, "turn": None}

        def watch(msg):
            params = msg.get("params") or {}
            if msg["method"] == "item/completed" and (params.get("item") or {}).get("type") == "agentMessage":
                messages.append(params["item"]["text"])
            if msg["method"] == "turn/completed" and params.get("threadId") == thread_id:
                state["done"] = True
                state["turn"] = params.get("turn") or {}

        params = {"threadId": thread_id, "input": [{"type": "text", "text": prompt}]}
        if effort:
            params["effort"] = effort
        self.request("turn/start", params, on_notification=watch)
        while not state["done"]:
            self.dispatch(self.recv(), watch)
        turn = state["turn"]
        if turn.get("status") != "completed":
            error = (turn.get("error") or {}).get("message") or turn.get("status")
            raise RuntimeError(f"turn ended with status {turn.get('status')}: {error}")
        return messages[-1] if messages else ""


def socket_answers():
    try:
        client = Client(SOCKET_PATH)
        client.initialize()
        client.sock.close()
        return True
    except (OSError, RuntimeError, EOFError, Timeout):
        return False


def start_server():
    codex = shutil.which("codex")
    if not codex:
        raise SystemExit("codex not found on PATH")
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)
    os.makedirs(CLAUDE_DIR, exist_ok=True)
    with open(LOG_PATH, "ab") as log_file:
        process = subprocess.Popen(
            [codex, "app-server", "--listen", f"unix://{SOCKET_PATH}"],
            stdin=subprocess.DEVNULL,
            stdout=log_file,
            stderr=log_file,
            start_new_session=True,
        )
    with open(PID_PATH, "w") as pid_file:
        pid_file.write(str(process.pid))
    waited = 0.0
    while waited < START_WAIT_SECONDS:
        if os.path.exists(SOCKET_PATH) and socket_answers():
            return
        if process.poll() is not None:
            raise SystemExit(f"codex app-server exited with {process.returncode}; see {LOG_PATH}")
        time.sleep(0.25)
        waited += 0.25
    raise SystemExit(f"codex app-server did not answer within {START_WAIT_SECONDS}s; see {LOG_PATH}")


def connect(timeout):
    if not socket_answers():
        start_server()
    deadline = time.monotonic() + timeout if timeout else None
    client = Client(SOCKET_PATH, deadline)
    client.initialize()
    return client


def resolve(client, ref):
    if UUID_RE.match(ref):
        return ref
    threads = client.request("thread/list", {"limit": 200})["data"]
    for thread in threads:
        if thread.get("name") == ref:
            return thread["id"]
    raise SystemExit(f"no thread named {ref!r}")


def last_agent_message(thread):
    for turn in reversed(thread.get("turns") or []):
        for item in reversed(turn.get("items") or []):
            if item.get("type") == "agentMessage":
                return turn, item["text"]
    return (thread.get("turns") or [None])[-1], ""


def print_reply(text):
    print(text)


def timed_out(thread_id, timeout):
    log(f"timeout after {timeout}s; thread {thread_id} keeps running. Read it later with: codex_peer.py read {thread_id}")
    sys.exit(2)


def cmd_new(args):
    client = connect(args.timeout)
    params = {
        "cwd": os.path.abspath(args.cwd),
        "sandbox": args.sandbox,
        "approvalPolicy": args.approval,
        "approvalsReviewer": "auto_review",
    }
    if args.model:
        params["model"] = args.model
    if args.effort:
        params["config"] = {"model_reasoning_effort": args.effort}
    thread_id = None
    try:
        started = client.request("thread/start", params)
        thread_id = started["thread"]["id"]
        client.request("thread/name/set", {"threadId": thread_id, "name": args.name})
        print(f"thread_id: {thread_id}")
        print(f"name: {args.name}")
        print(f"model: {started.get('model') or 'default'}")
        print(f"effort: {started.get('reasoningEffort') or 'default'}")
        print(f"sandbox: {args.sandbox}")
        print(f"approval: {args.approval}")
        print(f"attach: codex resume {thread_id}")
        print("", flush=True)
        print_reply(client.run_turn(thread_id, args.prompt, args.effort))
    except Timeout:
        timed_out(thread_id or args.name, args.timeout)


def cmd_send(args):
    client = connect(args.timeout)
    thread_id = None
    try:
        thread_id = resolve(client, args.thread)
        client.request("thread/resume", {"threadId": thread_id, "excludeTurns": True})
        print_reply(client.run_turn(thread_id, args.message, args.effort))
    except Timeout:
        timed_out(thread_id or args.thread, args.timeout)


def cmd_read(args):
    client = connect(None)
    thread_id = resolve(client, args.thread)
    thread = client.request("thread/read", {"threadId": thread_id, "includeTurns": True})["thread"]
    turn, text = last_agent_message(thread)
    status = (turn or {}).get("status") or "unknown"
    log(f"thread {thread_id}, last turn {status}")
    print_reply(text)


def cmd_stop(args):
    pid = None
    if os.path.exists(PID_PATH):
        with open(PID_PATH) as pid_file:
            pid = int(pid_file.read().strip() or 0)
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
            for _ in range(20):
                time.sleep(0.25)
                os.kill(pid, 0)
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        os.remove(PID_PATH)
        print(f"stopped app-server pid {pid}")
    else:
        print("no app-server pid recorded")
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    new = sub.add_parser("new", help="start a named peer thread and run its first turn")
    new.add_argument("--name", required=True)
    new.add_argument("--cwd", default=os.getcwd())
    new.add_argument("--model")
    new.add_argument("--effort")
    new.add_argument("--sandbox", default="workspace-write", choices=["read-only", "workspace-write", "danger-full-access"])
    new.add_argument("--approval", default="on-request", choices=["untrusted", "on-request", "never"])
    new.add_argument("--timeout", type=int, default=540)
    new.add_argument("prompt")
    new.set_defaults(run=cmd_new)

    send = sub.add_parser("send", help="run one more turn on an existing thread and print the reply")
    send.add_argument("--effort")
    send.add_argument("--timeout", type=int, default=540)
    send.add_argument("thread", metavar="ID_OR_NAME")
    send.add_argument("message")
    send.set_defaults(run=cmd_send)

    read = sub.add_parser("read", help="print the last agent message of a thread")
    read.add_argument("thread", metavar="ID_OR_NAME")
    read.set_defaults(run=cmd_read)

    stop = sub.add_parser("stop", help="stop the shared app-server")
    stop.set_defaults(run=cmd_stop)

    args = parser.parse_args()
    try:
        args.run(args)
    except (RuntimeError, EOFError, OSError) as error:
        raise SystemExit(f"error: {error}")


if __name__ == "__main__":
    main()

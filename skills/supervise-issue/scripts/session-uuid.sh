#!/bin/bash
set -euo pipefail
name=$1
cwd=${2:-}
if [ -n "$cwd" ] && [ -d "$cwd" ]; then cwd=$(cd "$cwd" && pwd); fi
claude agents --json --all | python3 -c '
import json, sys
name, cwd = sys.argv[1], sys.argv[2]
rows = [a for a in json.load(sys.stdin)
        if a.get("kind") == "background" and a.get("name") == name and (not cwd or a.get("cwd") == cwd)]
if not rows: sys.exit("no background session named %r%s" % (name, " in " + cwd if cwd else ""))
print(max(rows, key=lambda a: a.get("startedAt", 0))["sessionId"])
' "$name" "$cwd"

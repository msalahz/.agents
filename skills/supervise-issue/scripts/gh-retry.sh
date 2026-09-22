#!/bin/bash
set -euo pipefail
attempt=1
while true; do
  if gh "$@"; then
    exit 0
  fi
  if [ "$attempt" -ge 3 ]; then
    echo "gh failed after 3 attempts: gh $*" >&2
    exit 1
  fi
  attempt=$((attempt + 1))
  sleep 5
done

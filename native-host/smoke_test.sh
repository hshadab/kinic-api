#!/usr/bin/env bash
set -euo pipefail

# Simple smoke test: triggers kinic.store via local HTTP API.
# Requires: Extension connected (service worker keeps native port open)

HOST=${HOST:-127.0.0.1}
PORT=${PORT:-5007}

echo "Checking status..."
curl -sS "http://$HOST:$PORT/api/status" | jq . || true

echo "Triggering kinic.store (active tab by default)..."
curl -sS -X POST "http://$HOST:$PORT/api/kinic/store" \
  -H 'Content-Type: application/json' \
  -d '{"notes":"Saved via smoke test"}' | jq . || true

echo "Retrieving (simple query)..."
curl -sS -X POST "http://$HOST:$PORT/api/kinic/retrieve" \
  -H 'Content-Type: application/json' \
  -d '{"query":"test", "top_k": 3}' | jq . || true

#!/usr/bin/env bash
set -euo pipefail

HOST_NAME="com.kinic.api"
TARGET_DIR="$HOME/Library/Application Support/Google/Chrome/NativeMessagingHosts"
TARGET_FILE="$TARGET_DIR/$HOST_NAME.json"

if [[ -f "$TARGET_FILE" ]]; then
  rm -f "$TARGET_FILE"
  echo "Removed: $TARGET_FILE"
else
  echo "Manifest not found: $TARGET_FILE"
fi

echo "If you created additional manifests (Chrome Canary/Beta or Edge), remove those as well."


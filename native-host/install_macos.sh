#!/usr/bin/env bash
set -euo pipefail

# Install Kinic native host manifest for macOS (user scope)
# Places manifest at:
#   ~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.kinic.api.json

HOST_NAME="com.kinic.api"
TARGET_DIR="$HOME/Library/Application Support/Google/Chrome/NativeMessagingHosts"
TARGET_FILE="$TARGET_DIR/$HOST_NAME.json"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HOST_PATH="$SCRIPT_DIR/kinic_native_host.py"

if [[ ! -f "$HOST_PATH" ]]; then
  echo "Host script not found: $HOST_PATH" >&2
  exit 1
fi

mkdir -p "$TARGET_DIR"

MANIFEST_TEMPLATE="$SCRIPT_DIR/manifest/macos/com.kinic.api.json"
if [[ ! -f "$MANIFEST_TEMPLATE" ]]; then
  echo "Manifest template not found: $MANIFEST_TEMPLATE" >&2
  exit 1
fi

# Replace absolute path in template
ABS_PATH_MANIFEST=$(cat "$MANIFEST_TEMPLATE" | sed "s|/ABSOLUTE/PATH/TO/kinic_native_host.py|$HOST_PATH|g")
echo "$ABS_PATH_MANIFEST" > "$TARGET_FILE"

chmod +x "$HOST_PATH"
echo "Installed manifest: $TARGET_FILE"
echo "Ensure you replace DEV_EXTENSION_ID and PROD_EXTENSION_ID with your IDs."


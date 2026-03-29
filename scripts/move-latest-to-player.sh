#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="assets/generated"
DST_DIR="assets/sprites"
mkdir -p "$DST_DIR"

LATEST=$(ls -1t "$SRC_DIR"/sprite_*.png 2>/dev/null | head -n1 || true)
if [ -z "$LATEST" ]; then
  echo "No generated sprite found in $SRC_DIR" >&2
  exit 1
fi

DST="$DST_DIR/Player.png"
echo "Copying $LATEST -> $DST"
cp -f "$LATEST" "$DST"
echo "Done."

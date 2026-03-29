#!/usr/bin/env bash
set -euo pipefail

MANIFEST="docs/sprite-manifest.json"
if [ ! -f "$MANIFEST" ]; then
  echo "Manifest not found: $MANIFEST" >&2
  exit 1
fi

echo "Starting batch generation from $MANIFEST"
count=0
jq -c '.[]' "$MANIFEST" | while read -r item; do
  id=$(echo "$item" | jq -r '.id')
  prompt=$(echo "$item" | jq -r '.prompt')
  width=$(echo "$item" | jq -r '.width')
  height=$(echo "$item" | jq -r '.height')
  pixel=$(echo "$item" | jq -r '.pixel')
  bg_mode=$(echo "$item" | jq -r '.bg_mode')

  echo "Generating [$id] ($width x $height)"
  ./scripts/generate-sprite.sh "$prompt" "$width" "$height" "$pixel" "$bg_mode"

  # move latest generated file to named file
  LATEST=$(ls -1t assets/generated/sprite_*.png 2>/dev/null | head -n1 || true)
  if [ -z "$LATEST" ]; then
    echo "No generated file found for $id" >&2
    exit 2
  fi
  DEST="assets/generated/${id}.png"
  mv -f "$LATEST" "$DEST"
  echo "Saved to $DEST"
  count=$((count+1))
done

echo "Batch generation finished. Generated $count assets."

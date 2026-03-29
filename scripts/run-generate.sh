#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/run-generate.sh "PROMPT" [width] [height]
PROMPT="${1:-16-bit SNES style side view character: young male in a hoodie and cap}" 
WIDTH="${2:-64}"
HEIGHT="${3:-64}"

echo "Checking credits..."
./scripts/check-credits.sh
CR_EXIT=$?
if [ $CR_EXIT -eq 0 ]; then
  echo "Credits available — generating sprite..."
  ./scripts/generate-sprite.sh "$PROMPT" "$WIDTH" "$HEIGHT"
  exit 0
elif [ $CR_EXIT -eq 3 ]; then
  echo "No credits available. Aborting." >&2
  exit 3
else
  echo "Error checking credits (exit $CR_EXIT)." >&2
  exit $CR_EXIT
fi

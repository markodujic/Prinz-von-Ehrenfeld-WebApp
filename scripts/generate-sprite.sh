#!/usr/bin/env bash
set -euo pipefail

# Simple helper to call SpriteCook MCP (HTTP JSON‑RPC) and download result.
# Usage: ./scripts/generate-sprite.sh "PROMPT" [width] [height] [pixel:true|false] [bg_mode] [outdir]

API_KEY="${SPRITECOOK_API_KEY:-}"
if [ -z "$API_KEY" ]; then
  echo "Error: Set SPRITECOOK_API_KEY environment variable before running."
  exit 1
fi

PROMPT="$1"
WIDTH="${2:-64}"
HEIGHT="${3:-64}"
PIXEL="${4:-true}"
BG_MODE="${5:-transparent}"
OUTDIR="${6:-assets/generated}"
mkdir -p "$OUTDIR"

PAYLOAD=$(cat <<EOF
{"jsonrpc":"2.0","id":1,"method":"generate_game_art","params":{"prompt":"$PROMPT","width":$WIDTH,"height":$HEIGHT,"variations":1,"pixel":$PIXEL,"bg_mode":"$BG_MODE"}}
EOF
)

echo "Requesting sprite generation..."
RESP=$(curl -s -X POST https://api.spritecook.ai/mcp/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "$PAYLOAD")

URL=$(printf "%s" "$RESP" | python - <<PY
import sys, json
r = json.load(sys.stdin)
res = r.get('result') or r
assets = res.get('assets') if isinstance(res, dict) else None
if assets and len(assets)>0:
    print(assets[0].get('pixel_url') or assets[0].get('url') or '')
else:
    # fallback recursive search
    def find(o):
        if isinstance(o, dict):
            if 'pixel_url' in o: return o['pixel_url']
            for v in o.values():
                r = find(v)
                if r: return r
        if isinstance(o, list):
            for e in o:
                r = find(e)
                if r: return r
        return None
    print(find(r) or '')
PY
)

if [ -z "$URL" ]; then
  echo "No pixel_url found in response. Full response:" >&2
  echo "$RESP" >&2
  exit 1
fi

OUTFILE="$OUTDIR/sprite_$(date +%s).png"
echo "Downloading $URL → $OUTFILE"
curl -sL "$URL" -o "$OUTFILE"
echo "Saved to $OUTFILE"

exit 0

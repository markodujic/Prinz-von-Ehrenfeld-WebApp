#!/usr/bin/env bash
set -euo pipefail

API_KEY="${SPRITECOOK_API_KEY:-}"
if [ -z "$API_KEY" ]; then
  echo "Error: SPRITECOOK_API_KEY not set. Export it before running." >&2
  exit 2
fi

PAYLOAD='{"jsonrpc":"2.0","id":1,"method":"get_credit_balance","params":{}}'
RESP=$(curl -s -X POST https://api.spritecook.ai/mcp/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "$PAYLOAD")

# extract credits and concurrent_jobs using python for portability
echo "$RESP" | python - <<PY
import sys, json
try:
    r=json.load(sys.stdin)
except Exception as e:
    print('invalid response')
    sys.exit(2)
res=r.get('result') or r
credits = res.get('credits') if isinstance(res, dict) else None
concurrent = res.get('concurrent_jobs') if isinstance(res, dict) else None
if credits is None:
    # attempt nested search
    def find(o,k):
        if isinstance(o, dict):
            if k in o: return o[k]
            for v in o.values():
                r=find(v,k)
                if r is not None: return r
        if isinstance(o, list):
            for e in o:
                r=find(e,k)
                if r is not None: return r
        return None
    credits = find(res,'credits')
    concurrent = find(res,'concurrent_jobs')
print(f"credits:{credits}")
print(f"concurrent_jobs:{concurrent}")
if credits is None:
    sys.exit(2)
if isinstance(credits,(int,float)) and credits>0:
    sys.exit(0)
else:
    sys.exit(3)
PY

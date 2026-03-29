# SpriteCook Prompt Templates & CLI Examples

Kurz: Hier sind sofort nutzbare Prompt‑Templates für deine Hauptcharaktere und Beispiel‑Befehle (CLI + curl) zur Generierung mit SpriteCook.

## Prompt Templates (16‑bit SNES Stil)

- Kev (Standard, Hoodie, Doppelsprung)
```
16-bit SNES style side view character: young male in a hoodie and cap, neutral walking pose, small backpack, pixel art, transparent background, 64x64
```

- Silla (Schnell)
```
16-bit SNES style side view character: slim athletic female wearing a racing jacket and sneakers, dynamic running pose, pixel art, transparent background, 64x64
```

- Jojo (Tank)
```
16-bit SNES style side view character: stocky character in a colorful carnival outfit, heavy stance, pixel art, transparent background, 64x64
```

## CLI (empfohlen, wenn `npx spritecook-mcp` verfügbar)

Beispiel (einfacher Test):

```bash
npx spritecook-mcp generate_game_art \
  --prompt "16-bit SNES style side view character: young male in a hoodie and cap, neutral walking pose" \
  --width 64 --height 64 --variations 1 --pixel true --bg_mode transparent
```

## JSON‑RPC / curl Beispiel (falls du lieber HTTP nutzt)

Setze vorher die Umgebungsvariable `SPRITECOOK_API_KEY`.

```bash
API_KEY="$SPRITECOOK_API_KEY"
curl -s -X POST https://api.spritecook.ai/mcp/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "jsonrpc":"2.0",
    "id":1,
    "method":"generate_game_art",
    "params":{
      "prompt":"16-bit SNES style side view character: young male in a hoodie and cap, neutral walking pose",
      "width":64,
      "height":64,
      "variations":1,
      "pixel":true,
      "bg_mode":"transparent"
    }
  }'
```

Hinweis: Die Antwort enthält `pixel_url`(s) — lade die Datei per `curl -L <pixel_url> -o assets/sprite.png` herunter.

## Empfehlungen
- Generiere zuerst ein Hero‑Asset (z. B. Kev) und verwende dessen `asset_id` als `reference_asset_id` für Konsistenz.
- Für Batch‑Generierung nutze Skripte (unten). Prüfe `get_credit_balance` vor großen Jobs.

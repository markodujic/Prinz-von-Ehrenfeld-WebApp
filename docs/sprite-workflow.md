# SpriteCook Workflow — Schnellstart

Ziel: mit einem Befehl Guthaben prüfen und bei Verfügbarkeit ein Test‑Sprite generieren.

Voraussetzungen:
- Ein SpriteCook API‑Key in der Umgebungsvariablen `SPRITECOOK_API_KEY`
- Internetzugang

Bash (Linux/macOS/WSL / Git Bash / PowerShell mit bash):

```bash
export SPRITECOOK_API_KEY="DEIN_KEY"
./scripts/run-generate.sh "16-bit SNES style side view character: young male in a hoodie and cap" 64 64
```

PowerShell (Windows):

```powershell
$env:SPRITECOOK_API_KEY = "DEIN_KEY"
.\scripts\run-generate.ps1 -Prompt "16-bit SNES style side view character: young male in a hoodie and cap" -Width 64 -Height 64
```

Was die Skripte tun:
- `check-credits.*` prüft `get_credit_balance` und gibt Exitcode `0` (ok) / `3` (kein Guthaben) / `2` (Fehler) zurück.
- `generate-sprite.*` ruft `generate_game_art` und lädt die erste `pixel_url` in `assets/generated/` herunter.
- `run-generate.*` verbindet beides: erst Credits prüfen, dann generieren.

Wenn du möchtest, kann ich ein npm‑Script in `package.json` ergänzen, z. B. `npm run sprite:generate`, das das passende Skript aufruft.

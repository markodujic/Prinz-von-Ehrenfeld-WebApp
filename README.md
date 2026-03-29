# Prinz von Ehrenfeld – Jump ’n’ Run Webapp

## Spielidee
Ein überdrehtes 2D-Pixelart-Jump’n’Run im modernen Kölner Stadtteil Ehrenfeld. Sammle Kölsch-Kronen, besiege das Ordnungsamt und werde „Prinz vum Veedel“!

## Aktueller Stand (März 2026)
- Spieler **Kev** läuft und springt auf einer Spielfläche (960×600 px)
- **10 Plattformen:** 6 braune Einweg-Plattformen + 4 graue Solide auf 3 Höhenebenen
- **Animationen:** 8-Frame Lauf (12 FPS), 6-Frame Idle mit Atmen & Blinzeln (8 FPS), Sprungpose
- **Hitbox** bündig zur Figur (18×49 px), unabhängig vom 64×64 Sprite-Canvas
- Tastatur- und Touch-Steuerung

## Features (geplant)
- Drei spielbare Charaktere mit eigenen Fähigkeiten
- 5 Level mit unterschiedlichen Settings, Gegnern und Bossen
- Collectibles, Power-Ups und Highscore-System
- Kölsch-Lokalisierung für alle UI-Texte
- Integrierter Level-Editor

## Steuerung (Web)
- Bewegung: Pfeiltasten / A D
- Springen: Leertaste
- Touch: On-Screen-Buttons ◀ ▶ ↑

## Entwicklung
```bash
npm run web                                        # Webapp starten
pip install pillow
python scripts/generate-run-animation.py           # Kev Lauf-Sprites erzeugen
python scripts/generate-idle-animation.py          # Kev Idle-Sprites erzeugen
```

## Projektstruktur
```
app/index.tsx          ← Spielfeld, PLATFORMS-Array
components/Player.tsx  ← Physik, Kollision, Animations-Loop
assets/sprites/        ← Kev_*.png, weitere Charakter-Sprites
scripts/               ← Python-Sprite-Generatoren
```

## Assets & Lizenzen
Alle verwendeten Grafiken sind Open Source oder per Script generiert. Siehe ASSET_SOURCES.md für Details.

---

© 2026 Prinz von Ehrenfeld Team

- [Expo documentation](https://docs.expo.dev/): Learn fundamentals, or go into advanced topics with our [guides](https://docs.expo.dev/guides).
- [Learn Expo tutorial](https://docs.expo.dev/tutorial/introduction/): Follow a step-by-step tutorial where you'll create a project that runs on Android, iOS, and the web.

## Join the community

Join our community of developers creating universal apps.

- [Expo on GitHub](https://github.com/expo/expo): View our open source platform and contribute.
- [Discord community](https://chat.expo.dev): Chat with Expo users and ask questions.

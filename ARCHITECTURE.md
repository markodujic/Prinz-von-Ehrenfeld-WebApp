# Architektur – Prinz von Ehrenfeld

## Überblick

Das Spiel ist eine **React Native (Expo) Web-App** – ein 2D-Pixelart-Platformer, der im Browser läuft.  
Die Spiellogik läuft in einem einzigen `requestAnimationFrame`-Loop in `components/Player.tsx`.

```
app/index.tsx          ← Spielfeld: Plattformen, Hintergrund, <Player>-Einbindung
components/Player.tsx  ← Physik, Kollision, Eingabe, Animations-State-Machine
assets/sprites/        ← Kev_*.png und weitere Charakter-Sprites
scripts/               ← Python-Sprite-Generatoren (Pillow)
```

---

## Spielfläche

- **Canvas:** 960 × 600 px (fest)
- **Boden:** `groundY = 500`
- **Plattform-Koordinaten** (linke obere Ecke):

| Typ     | x   | y   | Breite | Höhe | Besonderheit               |
|---------|-----|-----|--------|------|----------------------------|
| Braun   | 100 | 390 | 150    | 20   | Einweg (Sprung von unten)  |
| Braun   | 650 | 390 | 150    | 20   | Einweg                     |
| Braun   | 280 | 280 | 150    | 20   | Einweg                     |
| Braun   | 520 | 280 | 150    | 20   | Einweg                     |
| Braun   | 150 | 170 | 150    | 20   | Einweg                     |
| Braun   | 620 | 170 | 150    | 20   | Einweg                     |
| Grau    | 390 | 360 | 130    | 20   | Solide (Kollision von oben & unten) |
| Grau    |  40 | 250 | 130    | 20   | Solide                     |
| Grau    | 760 | 250 | 130    | 20   | Solide                     |
| Grau    | 385 | 140 | 130    | 20   | Solide                     |

---

## Player-System (`components/Player.tsx`)

### Physik-Konstanten

| Konstante      | Wert       | Bedeutung                     |
|----------------|------------|-------------------------------|
| `GRAVITY`      | 1500 px/s² | Fallbeschleunigung            |
| `MOVE_SPEED`   | 300 px/s   | Laufgeschwindigkeit           |
| `JUMP_VELOCITY`| -650 px/s  | Initiale Sprunggeschwindigkeit |
| `SIZE`         | 64 px      | Sprite-Canvas (nur Rendering) |

### Hitbox-Konstanten

| Konstante       | Wert | Bedeutung                          |
|-----------------|------|------------------------------------|
| `HIT_OFFSET_X`  | 20   | Versatz links (Rucksack ausgenommen) |
| `HIT_OFFSET_Y`  | 12   | Versatz oben (Kopf)                |
| `HIT_W`         | 18   | Körperbreite                       |
| `HIT_H`         | 49   | Körperhöhe bis Schuhsohle          |

### Animations-State-Machine

`spriteFrame`-State-Werte:

| Wert    | Zustand  | Frames / FPS |
|---------|----------|--------------|
| 0 – 7   | Laufen   | 8 Frames, 12 FPS |
| 100–105 | Idle     | 6 Frames, 8 FPS  |
| -2      | Springen | 1 Frame (Kev_run_3) |

Links-Flip via `facingLeft` → `transform: [{scaleX: -1}]`

---

## Sprite-Generierung

| Script                              | Ausgabe                        | Besonderheit              |
|-------------------------------------|--------------------------------|---------------------------|
| `scripts/generate-run-animation.py` | `Kev_run_1–8.png` + Sheet      | 8 Frames, Lauf-Zyklus     |
| `scripts/generate-idle-animation.py`| `Kev_idle_1–6.png` + Sheet     | Atem-Bob, Blink Frame 3–4 |

### Farbpalette (Kev)

| Körperteil | Farbe      | Hex       |
|------------|------------|-----------|
| Hoodie     | Grau       | `#888888` |
| Jeans      | Dunkelblau | `#2a3a4a` |
| Sneaker    | Weiß       | `#f0f0f0` |
| Rucksack   | Braun      | `#8b6914` |
| Haare      | Dunkelbraun| `#2a1a0a` |
| Haut       | Beige      | `#d4956a` |

---

## Kollisions-Logik

1. Boden-Check: `feetY >= groundY` → snap auf Boden
2. Plattform-Top: Spieler fällt auf Plattform (vorherige `vy` > 0, Feet überschreiten Platform-Top)
3. Plattform-Bottom (nur `solid: true`): Spieler springt gegen Unterseite → `vy = 0`
4. X-Begrenzung: Hitbox bleibt im Canvas (`0` bis `960 - SIZE`)

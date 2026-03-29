# Isometrisches 3D-Straßen-Konzept – Venloer Straße

## Ziel
Der Bürgersteig und die Straße sollen nicht mehr flach (2D-Frontalansicht) aussehen,
sondern eine **isometrische Tiefe** suggerieren – ähnlich wie klassische SNES-Platformer
(z.B. Mode 7, Donkey Kong Country, Yoshi's Island).

Das Gameplay bleibt ein 2D-Sidescroller; der 3D-Effekt ist rein visuell im Hintergrundbild.

---

## Ansatz: Pseudo-Isometrie im Hintergrundbild

Das Spielfeld ist weiterhin `960×500px` flach. Die Illusion entsteht durch:

### 1. Straße mit Perspektiv-Fluchtpunkt
- Anstatt einer flachen Straße von links nach rechts zeichnen wir die Fahrbahn
  mit leicht divergierenden Linien nach unten (Vogelperspektive ~30°).
- Die Schienen und Fahrbahnmarkierungen laufen von einem Fluchtpunkt
  (Mitte oben, ~x=480, y=360) fächerartig auseinander.
- Je weiter unten (= je näher am Betrachter), desto breiter der Abstand der Linien.

```
         |   Fluchtpunkt y=360  |
        /  \                  /  \
       /    \________________/    \
      / Straße mit Perspektive     \
     /________________________________\  <- Bildunterkante y=500
```

### 2. Bürgersteig-Kante als Volumen
- Die Bordstein-Kante bekommt eine **sichtbare Seite** (Stirnfläche ca. 8px hoch,
  dunkler als die Gehwegfläche) → wirkt wie eine 3D-Kante.
- Die Gehwegplatten-Fugen laufen leicht schräg trapezförmig (Perspektive),
  nicht mehr rein horizontal.

### 3. Schienen-Perspektive
- Straßenbahnschienen starten schmal oben (bei y≈365) und werden breiter unten (y=500).
- Bolzen werden kleiner je höher (weiter weg).

### 4. Straßenmarkierungen
- Zebrastreifen und Randstreifen werden als trapezförmige Polygone gezeichnet,
  schmal oben, breit unten.

### 5. Gebäude-Sockel mit isometrischer Seitenansicht
- Die Gebäude-Unterseite (wo Wand auf Bürgersteig trifft) bekommt einen
  **Sockelblocker**: eine dunkle Schrägfläche (~15px), die die Gebäude
  aus dem Boden „herauswachsen" lässt.

---

## Technische Umsetzung im Python-Script

### Perspektive-Hilfsfunktionen

```python
# Fluchtpunkt
VP_X = 480   # horizontal mittig
VP_Y = 362   # genau auf Bordstein-Oberkante

def persp_x(world_x: float, world_y: float) -> int:
    """
    Gibt die tatsächliche Pixel-X-Koordinate für einen Punkt zurück,
    der in 'Weltkoordinaten' (world_x=0..960, world_y=0..138 relativ zum Bordstein)
    liegt. world_y=0 → Bordstein-Kante (hinten), world_y=138 → Bildunterkante (vorne).
    """
    t = world_y / 138.0          # 0 = hinten, 1 = vorne
    scale = 0.5 + 0.5 * t        # hinten: 0.5, vorne: 1.0
    return int(VP_X + (world_x - VP_X) * scale)

def persp_y(world_y: float) -> int:
    return int(VP_Y + world_y)
```

### Straße zeichnen (Trapez-Polygon)
```python
# Straße als Trapez: oben schmal, unten breit
road_poly = [
    (persp_x(0,   0),   VP_Y),       # links oben (Bordstein-Linie)
    (persp_x(W,   0),   VP_Y),       # rechts oben
    (W,                  H),          # rechts unten
    (0,                  H),          # links unten
]
d.polygon(road_poly, fill=ROAD)
```

### Schienen (Linien zum Fluchtpunkt)
```python
for rail_world_x in [240, 720]:
    for side in [-3, 3]:
        wx = rail_world_x + side
        # Schiene von Bordstein-Kante bis Bildunterkante
        x_top = persp_x(wx, 0)
        x_bot = wx  # bei y=138 (vorne) keine Verzerrung mehr nötig
        d.line([(x_top, VP_Y), (x_bot, H)], fill=TRAM_RAIL, width=2)
```

### Bürgersteig-Fugen (trapezförmig)
```python
# Horizontale "Reihen" des Pflasters als Trapeze
for row in range(0, 60, 12):
    y_world = row
    y1 = persp_y(y_world)
    y2 = persp_y(y_world + 12)
    x1_left  = persp_x(0, y_world)
    x1_right = persp_x(W, y_world)
    x2_left  = persp_x(0, y_world + 12)
    x2_right = persp_x(W, y_world + 12)
    # Fugenlinie
    d.line([(x1_left, y1), (x1_right, y1)], fill=SIDEWALK_LN, width=1)
```

---

## Änderungen gegenüber aktuellem Script

| Bereich | Aktuell | Neu |
|---|---|---|
| Straße | `rect(0, 422, W, H, ROAD)` | Trapez-Polygon mit Fluchtpunkt |
| Bürgersteig-Fugen | Horizontale Gitterlinien | Trapezförmige Perspektiv-Reihen |
| Bordstein | 4px dunkler Strich | 8px + 4px Stirnfläche (3D-Kante) |
| Schienen | Zwei vertikale Linien | Zum Fluchtpunkt laufende Linien |
| Zebrastreifen | Vertikale Streifen | Trapez-Polygone |
| Gebäude-Sockel | Keine | 15px isometrische Sockelfläche |

---

## Spiellogik-Auswirkung

**Keine Änderung nötig** — Plattformen, Kollision, Kev, Enemies bleiben unverändert.
Der Bürgersteig in `constants/level1.ts` liegt auf `y=500`. Das Hintergrundbild
ist rein dekorativ; `LEVEL1_GROUND_Y` bleibt bei `500`.

Der visuelle Bürgersteig im Bild startet bei `y=360` (Bordstein-Oberkante) und
geht bis `y=500` – das deckt sich genau mit `LEVEL1_GROUND_Y`.

---

## Nächster Schritt

Script `scripts/generate-bg-venloer.py` komplett neu schreiben:
- Abschnitt 4 (Bürgersteig & Straße) durch Perspektiv-Trapeze ersetzen
- Abschnitt 5 (Schienen) mit `persp_x`-Funktion neu berechnen
- Script ausführen → `assets/sprites/Bg_venloer.png` wird überschrieben
- Kein Änderungsbedarf in React-Code

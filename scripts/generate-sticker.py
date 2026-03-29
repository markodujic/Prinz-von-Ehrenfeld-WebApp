#!/usr/bin/env python3
"""
Generiert einen Veedel-Sticker (32x32, statisch).
Runder bunter Aufkleber mit 'V' im Zentrum und Kölner Dom-Silhouette.
Ausgabe: assets/sprites/Sticker.png
"""
import math
import os
from PIL import Image, ImageDraw

CANVAS  = 32
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'sprites')

TRANSPARENT  = (0,   0,   0,   0)
OUTLINE      = (30,  20,  15,  255)
BG_INNER     = (255, 240,  60, 255)   # gelber Hintergrund
BG_RIM       = (255, 140,   0, 255)   # oranger Rand
BG_RIM2      = (220,  80,   0, 255)   # dunklerer Rand-Akzent
LETTER       = ( 20,  80, 200, 255)   # blaues 'V'
DOM_SILH     = ( 80,  60,  30, 255)   # dunkle Dom-Silhouette
STAR         = (255, 255, 255, 255)   # weisse Sternchen
SHINE        = (255, 255, 200, 200)   # Glanzpunkt


def px(d, x, y, c):
    if 0 <= x < CANVAS and 0 <= y < CANVAS:
        d.point((x, y), fill=c)


def hline(d, x0, x1, y, c):
    for x in range(x0, x1 + 1):
        px(d, x, y, c)


def vline(d, x, y0, y1, c):
    for y in range(y0, y1 + 1):
        px(d, x, y, c)


def draw_sticker():
    img = Image.new('RGBA', (CANVAS, CANVAS), TRANSPARENT)
    d   = ImageDraw.Draw(img)

    cx = CANVAS // 2
    cy = CANVAS // 2
    r  = 14   # Kreis-Radius

    # Aeusserer Rand
    for y in range(CANVAS):
        for x in range(CANVAS):
            dist = math.hypot(x - cx, y - cy)
            if dist <= r + 1:
                if dist > r - 1:
                    d.point((x, y), fill=BG_RIM2)
                elif dist > r - 3:
                    d.point((x, y), fill=BG_RIM)
                else:
                    d.point((x, y), fill=BG_INNER)

    # Kleiner Dom oben (vereinfachte Dom-Silhouette)
    dom_base_y = cy - 2
    # Dom-Hauptturm links
    for dy in range(dom_base_y - 6, dom_base_y):
        w = max(1, 2 - abs(dy - dom_base_y + 3) // 2)
        for dx2 in range(cx - 7 - w, cx - 7 + w + 1):
            if math.hypot(dx2 - cx, dy - cy) < r - 2:
                px(d, dx2, dy, DOM_SILH)
    # Dom-Hauptturm rechts
    for dy in range(dom_base_y - 6, dom_base_y):
        w = max(1, 2 - abs(dy - dom_base_y + 3) // 2)
        for dx2 in range(cx + 5 - w, cx + 5 + w + 1):
            if math.hypot(dx2 - cx, dy - cy) < r - 2:
                px(d, dx2, dy, DOM_SILH)
    # Verbindungskoerper des Dom
    for dy in range(dom_base_y - 3, dom_base_y + 1):
        hline(d, cx - 7, cx + 6, dy, DOM_SILH)

    # Grosses 'V' in der Mitte (pixelig)
    # Linker Schenkel
    v_top_y = cy - 1
    v_bot_y = cy + 6
    for i, vy in enumerate(range(v_top_y, v_bot_y + 1)):
        frac = i / (v_bot_y - v_top_y)
        vx = int(cx - 5 + frac * 4.5)
        px(d, vx,     vy, LETTER)
        px(d, vx + 1, vy, LETTER)
    # Rechter Schenkel
    for i, vy in enumerate(range(v_top_y, v_bot_y + 1)):
        frac = i / (v_bot_y - v_top_y)
        vx = int(cx + 5 - frac * 4.5)
        px(d, vx,     vy, LETTER)
        px(d, vx - 1, vy, LETTER)

    # 3 kleine Sterne am Rand
    stars = [(cx - 9, cy + 5), (cx + 8, cy + 4), (cx, cy - 9)]
    for (sx, sy) in stars:
        if math.hypot(sx - cx, sy - cy) < r - 1:
            px(d, sx,     sy,     STAR)
            px(d, sx + 1, sy,     STAR)
            px(d, sx,     sy + 1, STAR)

    # Glanzpunkt oben-links
    for gx in range(cx - 8, cx - 4):
        for gy in range(cy - 9, cy - 5):
            if math.hypot(gx - cx, gy - cy) < r - 1:
                px(d, gx, gy, SHINE)

    return img


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    img = draw_sticker()
    path = os.path.join(OUT_DIR, 'Sticker.png')
    img.save(path)
    print(f'  OK  {os.path.basename(path)}')
    print('Fertig.')

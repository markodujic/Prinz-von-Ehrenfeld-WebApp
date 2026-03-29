#!/usr/bin/env python3
"""
Generiert 4 Pixel-Art-Frames einer rotierenden Koelsch-Krone (Muenzanimation).
Canvas: 32x32 pro Frame.
Ausgabe:
  assets/sprites/Krone_spin_1.png ... Krone_spin_4.png
  assets/sprites/Krone_spin_sheet.png (128x32)
"""
import math
import os
from PIL import Image, ImageDraw

CANVAS     = 32
NUM_FRAMES = 4
OUT_DIR    = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'sprites')

TRANSPARENT = (0,   0,   0,   0)
GOLD        = (255, 200,  30, 255)
GOLD_HLT    = (255, 235, 120, 255)
GOLD_SHD    = (180, 130,  10, 255)
OUTLINE     = ( 80,  50,   0, 255)
BEER_AMBER  = (200, 130,  20, 255)
FOAM        = (245, 240, 210, 255)

# Seitenbreiten je Frame (simuliert eine 3D-Rotation um Y-Achse)
# Frame 0: voll sichtbar (Vorderseite)
# Frame 1: halb
# Frame 2: schmal (Kante)
# Frame 3: halb (Rueckseite)
WIDTHS = [13, 7, 2, 7]


def px(d, x, y, c):
    if 0 <= x < CANVAS and 0 <= y < CANVAS:
        d.point((x, y), fill=c)


def hline(d, x0, x1, y, c):
    for x in range(x0, x1 + 1):
        px(d, x, y, c)


def draw_frame(idx):
    img = Image.new('RGBA', (CANVAS, CANVAS), TRANSPARENT)
    d   = ImageDraw.Draw(img)

    cx = CANVAS // 2
    w  = WIDTHS[idx]
    is_front = (idx in (0, 1))

    # Hauptkoerper der Krone: Trapez-Form (breiter oben)
    top_y    = 8
    bot_y    = 26
    coin_y   = 28  # Unterseite

    # Koerper
    for y in range(top_y + 3, bot_y):
        frac = (y - top_y) / (bot_y - top_y)
        # leicht trapezfoermig
        cur_w = max(1, int(w * (1.0 - frac * 0.1)))
        col = GOLD_HLT if (y < top_y + 6 and is_front) else GOLD
        if frac > 0.7:
            col = GOLD_SHD
        hline(d, cx - cur_w, cx + cur_w, y, col)

    # Zacken oben (Krone)
    if w >= 3:
        # 3 Zacken: links, mitte, rechts
        zacken = [cx - w + 1, cx, cx + w - 1]
        for zx in zacken:
            if 0 <= zx < CANVAS:
                px(d, zx, top_y + 2, GOLD_HLT)
                px(d, zx, top_y + 1, GOLD)
                px(d, zx, top_y,     GOLD_SHD)
    elif w >= 1:
        px(d, cx, top_y, GOLD)

    # Unterseite (Boden der Krone)
    hline(d, cx - w, cx + w, bot_y,     GOLD_SHD)
    hline(d, cx - w, cx + w, bot_y + 1, OUTLINE)

    # Detail: K-Gravur auf Vorderseite
    if is_front and w >= 5:
        mid_y = (top_y + bot_y) // 2
        # K-Form (grob pixelig)
        vline_x = cx - 2
        for vy in range(mid_y - 3, mid_y + 4):
            px(d, vline_x, vy, OUTLINE)
        # Oberer Arm
        px(d, vline_x + 1, mid_y - 2, OUTLINE)
        px(d, vline_x + 2, mid_y - 3, OUTLINE)
        # Unterer Arm
        px(d, vline_x + 1, mid_y + 2, OUTLINE)
        px(d, vline_x + 2, mid_y + 3, OUTLINE)

    # Glanzpunkt
    if is_front and w >= 4:
        px(d, cx - w + 2, top_y + 4, GOLD_HLT)
        px(d, cx - w + 3, top_y + 3, (255, 255, 200, 200))

    # Umriss
    for y in range(top_y, bot_y + 2):
        px(d, cx - w - 1, y, OUTLINE)
        px(d, cx + w + 1, y, OUTLINE)
    hline(d, cx - w - 1, cx + w + 1, top_y - 1, OUTLINE)
    hline(d, cx - w - 1, cx + w + 1, bot_y + 1, OUTLINE)

    # Kleiner Schimmer untern
    if w >= 2:
        for sx in range(cx - w + 1, cx + w):
            if (sx + idx) % 3 == 0:
                px(d, sx, bot_y - 1, (255, 240, 150, 160))

    return img


def build_sheet(frames):
    sheet = Image.new('RGBA', (CANVAS * NUM_FRAMES, CANVAS), TRANSPARENT)
    for i, f in enumerate(frames):
        sheet.paste(f, (i * CANVAS, 0))
    return sheet


def vline(d, x, y0, y1, c):
    for y in range(y0, y1 + 1):
        px(d, x, y, c)


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    frames = []
    for i in range(NUM_FRAMES):
        frame = draw_frame(i)
        path  = os.path.join(OUT_DIR, f'Krone_spin_{i + 1}.png')
        frame.save(path)
        print(f'  OK  {os.path.basename(path)}')
        frames.append(frame)
    sheet_path = os.path.join(OUT_DIR, 'Krone_spin_sheet.png')
    build_sheet(frames).save(sheet_path)
    print(f'\n  Sprite-Sheet -> {sheet_path}')
    print(f'\nFertig - {NUM_FRAMES} Frames generiert.')

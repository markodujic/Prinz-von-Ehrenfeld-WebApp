#!/usr/bin/env python3
"""
Generiert 4 Pixel-Art-Frames eines rotierenden Koelsch-Kronkorkens.
Canvas: 32x32 pro Frame.
Ausgabe:
    assets/sprites/Collectible_Koelsch.png
  assets/sprites/Krone_spin_1.png ... Krone_spin_4.png
  assets/sprites/Krone_spin_sheet.png (128x32)
"""
import os
from PIL import Image, ImageDraw

CANVAS     = 32
NUM_FRAMES = 4
OUT_DIR    = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'sprites')

TRANSPARENT = (0, 0, 0, 0)
GOLD = (224, 187, 56, 255)
GOLD_HLT = (255, 238, 150, 255)
GOLD_SHD = (164, 118, 22, 255)
OUTLINE = (90, 63, 14, 255)
RED = (202, 32, 34, 255)
RED_DARK = (128, 18, 22, 255)
WHITE = (246, 242, 236, 255)
WHITE_HLT = (255, 255, 255, 235)

# Seitenbreiten je Frame (simuliert eine 3D-Rotation um Y-Achse)
# Frame 0: voll sichtbar (Vorderseite)
# Frame 1: halb
# Frame 2: schmal (Kante)
# Frame 3: halb (Rueckseite)
WIDTHS = [13, 10, 4, 10]


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

    top_y = 6
    mid_y = 15
    bot_y = 25
    rim_y = 26

    # Runde Grundform des Kronkorkens
    outer_box = [cx - 12, top_y, cx + 12, bot_y]
    d.ellipse(outer_box, fill=GOLD_SHD, outline=OUTLINE)

    # Leicht hellere Oberseite für den metallischen Eindruck
    d.ellipse([cx - 11, top_y + 1, cx + 11, bot_y - 1], fill=GOLD, outline=None)

    # Crimped rim: kleine Zacken rund um die Unterkante und Seiten
    rim_points = [
        (cx - 11, 13), (cx - 12, 15), (cx - 11, 17), (cx - 12, 19),
        (cx - 10, 21), (cx - 11, 23), (cx - 9, 24), (cx - 7, 25),
        (cx - 4, 26), (cx, 27), (cx + 4, 26), (cx + 7, 25),
        (cx + 9, 24), (cx + 11, 23), (cx + 10, 21), (cx + 12, 19),
        (cx + 11, 17), (cx + 12, 15), (cx + 11, 13),
    ]
    for x, y in rim_points:
        px(d, x, y, OUTLINE)
        px(d, x, y + 1, GOLD_SHD)
        if x % 2 == 0:
            px(d, x, y - 1, GOLD_HLT)

    # Rote Deckfläche wie im Referenzfoto
    inner_box = [cx - 8, 9, cx + 8, 21]
    d.ellipse(inner_box, fill=RED, outline=WHITE)
    d.ellipse([cx - 7, 10, cx + 7, 20], fill=RED_DARK, outline=None)
    d.ellipse([cx - 6, 11, cx + 6, 19], fill=RED, outline=None)

    # Weißer Ring um das Logo-Feld
    ring_box = [cx - 8, 9, cx + 8, 21]
    d.ellipse(ring_box, outline=WHITE_HLT, width=1)
    d.ellipse([cx - 7, 10, cx + 7, 20], outline=WHITE, width=1)

    # Reduziertes Logo-Motiv als stilisierte Dom-Silhouette
    if is_front:
        px(d, cx - 1, 12, RED_DARK)
        px(d, cx, 11, RED_DARK)
        px(d, cx + 1, 12, RED_DARK)
        px(d, cx - 2, 13, RED_DARK)
        px(d, cx + 2, 13, RED_DARK)
        px(d, cx - 1, 14, RED_DARK)
        px(d, cx + 1, 14, RED_DARK)
        px(d, cx, 15, RED_DARK)
        hline(d, cx - 3, cx + 3, 16, WHITE)
        hline(d, cx - 2, cx + 2, 17, WHITE)

    # Metallfalten / Lichtkanten am unteren Rand
    for y in range(14, 26):
        px(d, cx - 12, y, OUTLINE)
        px(d, cx + 12, y, OUTLINE)
        if y % 2 == 0:
            px(d, cx - 11, y, GOLD_SHD)
            px(d, cx + 11, y, GOLD_SHD)

    # Dunkler Abschluss und Unterkante
    hline(d, cx - 9, cx + 9, rim_y, OUTLINE)
    hline(d, cx - 10, cx + 10, rim_y + 1, GOLD_SHD)

    # Glanz auf dem Metall
    if is_front:
        for x in range(cx - 7, cx + 2):
            if (x + idx) % 3 == 0:
                px(d, x, top_y + 4, WHITE_HLT)
        px(d, cx - 5, top_y + 5, WHITE_HLT)
        px(d, cx - 4, top_y + 4, GOLD_HLT)

    # Kleine Schattenpixel für Tiefe
    for x in range(cx - 9, cx + 10):
        if (x + idx) % 4 == 0:
            px(d, x, bot_y - 2, GOLD_SHD)

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
    collectible_path = os.path.join(OUT_DIR, 'Collectible_Koelsch.png')
    frames[0].save(collectible_path)
    print(f'  OK  {os.path.basename(collectible_path)}')
    sheet_path = os.path.join(OUT_DIR, 'Krone_spin_sheet.png')
    build_sheet(frames).save(sheet_path)
    print(f'\n  Sprite-Sheet -> {sheet_path}')
    print(f'\nFertig - {NUM_FRAMES} Frames generiert.')

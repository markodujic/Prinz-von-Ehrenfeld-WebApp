#!/usr/bin/env python3
"""
Generiert 6 Pixel-Art-Frames der Idle-Animation fuer Kev.
Gleiche Farbpalette wie generate-run-animation.py.
  - Atemschwung: Torso hebt sich 1-2 px
  - Arm haengt leicht, minimale Pendelbewegung
  - Augenblinzeln in Frame 4-5
  - Beisse stehen still, ein Fuss leicht vor

Ausgabe:
  assets/sprites/Kev_idle_1.png  ... Kev_idle_6.png   (64x64)
  assets/sprites/Kev_idle_sheet.png                    (384x64)
"""
import math
import os
from PIL import Image, ImageDraw

CANVAS     = 64
NUM_FRAMES = 6
OUT_DIR    = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'sprites')

TRANSPARENT = (0,   0,   0,   0)
OUTLINE     = (30,  20,  15,  255)
SKIN        = (198, 143, 100, 255)
SKIN_SHD    = (165, 108,  72, 255)
HAIR        = (42,  25,  14,  255)
HOODIE      = (162, 162, 166, 255)
HOODIE_SHD  = (118, 118, 124, 255)
HOODIE_HLT  = (208, 208, 212, 255)
JEANS       = (45,  55,  85,  255)
JEANS_SHD   = (28,  36,  60,  255)
SHOE_TOP    = (232, 230, 225, 255)
SHOE_SHD    = (185, 182, 176, 255)
SHOE_SOLE   = (48,  42,  38,  255)
SHOE_LACE   = (100, 100, 100, 255)
PACK_BODY   = (95,  75,  52,  255)
PACK_SHD    = (65,  50,  32,  255)
PACK_STRAP  = (75,  58,  38,  255)


def px(d, x, y, c):
    if 0 <= x < CANVAS and 0 <= y < CANVAS:
        d.point((x, y), fill=c)

def hline(d, x0, x1, y, c):
    for x in range(x0, x1 + 1): px(d, x, y, c)

def vline(d, x, y0, y1, c):
    for y in range(y0, y1 + 1): px(d, x, y, c)


def draw_frame(idx):
    img = Image.new('RGBA', (CANVAS, CANVAS), TRANSPARENT)
    d   = ImageDraw.Draw(img)

    # Atemschwung: 0 -> 1 -> 0 ueber alle Frames (eine halbe Sinus-Kurve)
    t        = (idx / NUM_FRAMES) * math.pi * 2
    breath   = math.sin(t)                         # -1 .. 1
    bob      = int(round((breath + 1) * 0.5))      # 0 oder 1 px nach oben
    arm_sway = breath * 1.5                        # mini Armpendel

    BASE_Y  = 61
    cx      = 30
    hip_y   = BASE_Y - 21 + bob
    chest_y = hip_y  - 13
    neck_y  = chest_y - 3
    head_cy = neck_y  - 6

    # Statische Beinpositionen (Idle - kein Swing)
    # Linkes Bein (hinter) leicht nach hinten
    lk_x = cx - 3; lk_y = hip_y + 10
    lf_x = cx - 5
    # Rechtes Bein (vorne) leicht nach vorne
    rk_x = cx + 3; rk_y = hip_y + 10
    rf_x = cx + 5

    # Arm-Positionen
    fa_x = cx + 10 + int(arm_sway); fa_y = chest_y + 14  # rechter haengender Arm
    ba_x = cx - 7  + int(arm_sway); ba_y = chest_y + 14  # linker

    blink = idx in (3, 4)   # Augen in Frame 3+4 geschlossen

    # ---- Rucksack -----------------------------------------------------------
    rx = cx - 9
    for ry in range(chest_y, hip_y + 1):
        shade = PACK_SHD if ry > chest_y + 5 else PACK_BODY
        hline(d, rx - 6, rx - 1, ry, shade)
    vline(d, rx - 2, chest_y + 1, hip_y - 1, PACK_BODY)
    for sy in range(chest_y - 1, chest_y + 5):
        px(d, cx - 5, sy, PACK_STRAP); px(d, cx - 7, sy, PACK_STRAP)

    # ---- Linkes Bein (hinten) -----------------------------------------------
    d.line([(cx, hip_y), (lk_x, lk_y)],        fill=JEANS_SHD, width=5)
    d.line([(lk_x, lk_y), (lf_x, BASE_Y - 2)], fill=JEANS_SHD, width=4)
    hline(d, lf_x - 5, lf_x + 4, BASE_Y - 2, SHOE_SHD)
    hline(d, lf_x - 5, lf_x + 4, BASE_Y - 1, SHOE_SHD)
    hline(d, lf_x - 5, lf_x + 4, BASE_Y,     SHOE_SOLE)

    # ---- Linker Arm (haengt hinter Torso) ------------------------------------
    d.line([(cx - 5, chest_y + 1), (ba_x, chest_y + 8)], fill=HOODIE_SHD, width=3)
    d.line([(ba_x, chest_y + 8), (ba_x - 1, ba_y)],      fill=SKIN_SHD,   width=2)

    # ---- Torso --------------------------------------------------------------
    for ty in range(chest_y, hip_y + 2):
        hw = 8 if ty < chest_y + 6 else 7
        hline(d, cx - hw + 1, cx + hw - 1, ty, HOODIE)
    vline(d, cx + 5, chest_y + 2, hip_y,     HOODIE_HLT)
    vline(d, cx - 7, chest_y + 2, hip_y,     HOODIE_SHD)
    d.rectangle([cx - 8, chest_y, cx + 8, hip_y + 1], outline=OUTLINE)
    hline(d, cx - 3, cx + 3, chest_y - 1, HOODIE)

    # ---- Rechter Arm (vorne, haengend) --------------------------------------
    d.line([(cx + 7, chest_y + 1), (cx + 9, chest_y + 8)], fill=HOODIE,   width=3)
    d.line([(cx + 9, chest_y + 8), (fa_x, fa_y)],          fill=SKIN,     width=2)
    for hx2 in range(fa_x - 2, fa_x + 3):
        px(d, hx2, fa_y,     SKIN)
        px(d, hx2, fa_y + 1, SKIN_SHD)

    # ---- Rechtes Bein (vorne) -----------------------------------------------
    d.line([(cx, hip_y), (rk_x, rk_y)],        fill=JEANS, width=5)
    d.line([(rk_x, rk_y), (rf_x, BASE_Y - 2)], fill=JEANS, width=4)
    hline(d, rf_x - 5, rf_x + 5, BASE_Y - 3, SHOE_TOP)
    hline(d, rf_x - 5, rf_x + 5, BASE_Y - 2, SHOE_TOP)
    hline(d, rf_x - 5, rf_x + 5, BASE_Y - 1, SHOE_SHD)
    hline(d, rf_x - 6, rf_x + 6, BASE_Y,     SHOE_SOLE)
    px(d, rf_x - 2, BASE_Y - 3, SHOE_LACE)
    px(d, rf_x + 1, BASE_Y - 3, SHOE_LACE)

    # ---- Kopf ---------------------------------------------------------------
    hline(d, cx, cx + 1, neck_y, SKIN); hline(d, cx, cx + 1, neck_y + 1, SKIN)

    for ky in range(head_cy - 4, head_cy + 5):
        dist = abs(ky - head_cy)
        w = {0: 5, 1: 5, 2: 4, 3: 3, 4: 2}.get(dist, 1)
        hline(d, cx - w + 2, cx + w + 1, ky, SKIN)

    px(d, cx - 3, head_cy, OUTLINE); px(d, cx + 7, head_cy, OUTLINE)

    # Auge (blinzeln = nur 1 px Schlitz)
    if blink:
        hline(d, cx + 4, cx + 6, head_cy, OUTLINE)         # geschlossenes Auge
    else:
        px(d, cx + 5, head_cy - 1, OUTLINE)
        px(d, cx + 5, head_cy,     OUTLINE)
        px(d, cx + 6, head_cy,     OUTLINE)

    # Braue
    hline(d, cx + 4, cx + 6, head_cy - 2, HAIR)

    # Nase
    px(d, cx + 6, head_cy + 1, SKIN_SHD)

    # Mund (ruhig)
    px(d, cx + 3, head_cy + 3, OUTLINE)
    px(d, cx + 4, head_cy + 3, OUTLINE)
    px(d, cx + 5, head_cy + 3, OUTLINE)

    # Haare
    hline(d, cx - 1, cx + 6, head_cy - 5, HAIR)
    hline(d, cx - 2, cx + 6, head_cy - 4, HAIR)
    hline(d, cx - 3, cx + 6, head_cy - 3, HAIR)
    hline(d, cx + 5, cx + 6, head_cy - 2, HAIR)

    return img


def build_sheet(frames):
    sheet = Image.new('RGBA', (CANVAS * NUM_FRAMES, CANVAS), TRANSPARENT)
    for i, f in enumerate(frames):
        sheet.paste(f, (i * CANVAS, 0))
    return sheet


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    frames = []
    for i in range(NUM_FRAMES):
        frame = draw_frame(i)
        path  = os.path.join(OUT_DIR, f'Kev_idle_{i + 1}.png')
        frame.save(path)
        print(f'  OK  {os.path.basename(path)}')
        frames.append(frame)
    sheet_path = os.path.join(OUT_DIR, 'Kev_idle_sheet.png')
    build_sheet(frames).save(sheet_path)
    print(f'\n  Sprite-Sheet -> {sheet_path}')
    print(f'\nFertig - {NUM_FRAMES} Frames generiert.')

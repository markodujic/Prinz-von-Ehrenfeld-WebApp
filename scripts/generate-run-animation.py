#!/usr/bin/env python3
"""
Generiert 8 Pixel-Art-Frames eines laufenden Kev.
Farben und Proportionen orientieren sich am Idle-Sprite (Player.png):
  grauer Hoodie, dunkle Jeans, weisse Sneaker, Rucksack, dunkles Haar.

Abhaengigkeit: pip install pillow

Ausgabe:
  assets/sprites/Player_run_1.png  ... Player_run_8.png   (64x64 je Frame)
  assets/sprites/Player_run_sheet.png                     (512x64 Sprite-Sheet)
"""
import math
import os
from PIL import Image, ImageDraw

CANVAS     = 64
NUM_FRAMES = 8
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
JEANS_HLT   = (60,  72, 108,  255)
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

    t     = (idx / NUM_FRAMES) * math.pi * 2
    bob   = int(round(abs(math.sin(t * 2)) * 2))

    BASE_Y  = 61
    cx      = 30
    hip_y   = BASE_Y - 21 + bob
    chest_y = hip_y  - 13
    neck_y  = chest_y - 3
    head_cy = neck_y  - 6

    swing = math.sin(t) * 12
    fk_x = cx + int(swing * 0.55); fk_y = hip_y + 10
    ff_x = cx + int(swing)
    bk_x = cx + int(-swing * 0.55); bk_y = hip_y + 10
    bf_x = cx + int(-swing)

    arm_s    = -math.sin(t) * 8
    fae_x = cx + 8 + int(arm_s * 0.55);  fae_y = chest_y + 6
    fah_x = cx + 7 + int(arm_s);         fah_y = chest_y + 13
    bae_x = cx - 6 + int(arm_s * 0.55);  bae_y = chest_y + 6
    bah_x = cx - 5 + int(arm_s);         bah_y = chest_y + 13

    # Rucksack
    rx = cx - 9
    for ry in range(chest_y, hip_y + 1):
        shade = PACK_SHD if ry > chest_y + 5 else PACK_BODY
        hline(d, rx - 6, rx - 1, ry, shade)
    vline(d, rx - 2, chest_y + 1, hip_y - 1, PACK_BODY)
    for sy in range(chest_y - 1, chest_y + 5):
        px(d, cx - 5, sy, PACK_STRAP); px(d, cx - 7, sy, PACK_STRAP)

    # Hinteres Bein
    d.line([(cx, hip_y), (bk_x, bk_y)],        fill=JEANS_SHD, width=5)
    d.line([(bk_x, bk_y), (bf_x, BASE_Y - 2)], fill=JEANS_SHD, width=4)
    hline(d, bf_x - 5, bf_x + 4, BASE_Y - 2, SHOE_SHD)
    hline(d, bf_x - 5, bf_x + 4, BASE_Y - 1, SHOE_SHD)
    hline(d, bf_x - 5, bf_x + 4, BASE_Y,     SHOE_SOLE)

    # Hinterer Arm
    d.line([(cx - 4, chest_y), (bae_x, bae_y)], fill=HOODIE_SHD, width=3)
    d.line([(bae_x, bae_y), (bah_x, bah_y)],    fill=SKIN_SHD,   width=2)

    # Torso
    for ty in range(chest_y, hip_y + 2):
        hw = 8 if ty < chest_y + 6 else 7
        hline(d, cx - hw + 1, cx + hw - 1, ty, HOODIE)
    vline(d, cx + 5, chest_y + 2, hip_y,     HOODIE_HLT)
    vline(d, cx - 7, chest_y + 2, hip_y,     HOODIE_SHD)
    d.rectangle([cx - 8, chest_y, cx + 8, hip_y + 1], outline=OUTLINE)
    hline(d, cx - 3, cx + 3, chest_y - 1, HOODIE)

    # Vorderer Arm
    d.line([(cx + 7, chest_y), (fae_x, fae_y)], fill=HOODIE, width=3)
    d.line([(fae_x, fae_y), (fah_x, fah_y)],    fill=SKIN,   width=2)
    for hx2 in range(fah_x - 2, fah_x + 3):
        px(d, hx2, fah_y, SKIN); px(d, hx2, fah_y + 1, SKIN_SHD)

    # Vorderes Bein
    d.line([(cx, hip_y), (fk_x, fk_y)],        fill=JEANS, width=5)
    d.line([(fk_x, fk_y), (ff_x, BASE_Y - 2)], fill=JEANS, width=4)
    hline(d, ff_x - 5, ff_x + 5, BASE_Y - 3, SHOE_TOP)
    hline(d, ff_x - 5, ff_x + 5, BASE_Y - 2, SHOE_TOP)
    hline(d, ff_x - 5, ff_x + 5, BASE_Y - 1, SHOE_SHD)
    hline(d, ff_x - 6, ff_x + 6, BASE_Y,     SHOE_SOLE)
    px(d, ff_x - 2, BASE_Y - 3, SHOE_LACE); px(d, ff_x + 1, BASE_Y - 3, SHOE_LACE)
    px(d, ff_x + 6, BASE_Y - 2, OUTLINE);   px(d, ff_x - 6, BASE_Y - 2, OUTLINE)

    # Hals
    hline(d, cx, cx + 1, neck_y, SKIN); hline(d, cx, cx + 1, neck_y + 1, SKIN)

    # Kopf (oval)
    for ky in range(head_cy - 4, head_cy + 5):
        dist = abs(ky - head_cy)
        w = {0: 5, 1: 5, 2: 4, 3: 3, 4: 2}.get(dist, 1)
        hline(d, cx - w + 2, cx + w + 1, ky, SKIN)
    px(d, cx - 3, head_cy, OUTLINE); px(d, cx + 7, head_cy, OUTLINE)

    # Auge
    px(d, cx + 5, head_cy - 1, OUTLINE)
    px(d, cx + 5, head_cy,     OUTLINE)
    px(d, cx + 6, head_cy,     OUTLINE)

    # Braue
    hline(d, cx + 4, cx + 6, head_cy - 2, HAIR)

    # Nase
    px(d, cx + 6, head_cy + 1, SKIN_SHD)

    # Mund
    px(d, cx + 3, head_cy + 3, OUTLINE); px(d, cx + 4, head_cy + 3, OUTLINE)
    if idx % 3 != 1:
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
        path  = os.path.join(OUT_DIR, f'Kev_run_{i + 1}.png')
        frame.save(path)
        print(f'  OK  {os.path.basename(path)}')
        frames.append(frame)
    sheet_path = os.path.join(OUT_DIR, 'Kev_run_sheet.png')
    build_sheet(frames).save(sheet_path)
    print(f'\n  Sprite-Sheet -> {sheet_path}')
    print(f'\nFertig - {NUM_FRAMES} Frames generiert.')

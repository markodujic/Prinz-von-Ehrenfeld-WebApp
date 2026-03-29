#!/usr/bin/env python3
"""
Generiert 6 Pixel-Art-Frames eines laufenden Touristen mit Selfie-Stick.
Canvas: 48x64 pro Frame.
Ausgabe:
  assets/sprites/Tourist_walk_1.png  ... Tourist_walk_6.png
  assets/sprites/Tourist_walk_sheet.png (288x64)
"""
import math
import os

from PIL import Image, ImageDraw

CANVAS_W   = 48
CANVAS_H   = 64
NUM_FRAMES = 6
OUT_DIR    = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'sprites')

TRANSPARENT = (0,   0,   0,   0)
OUTLINE     = (30,  20,  15,  255)
SKIN        = (230, 185, 140, 255)
SKIN_SHD    = (190, 145, 100, 255)
HAIR        = (200, 160,  80, 255)   # touristisches Sandblond
SHIRT       = (220,  80,  80, 255)   # rotes Touristenhemd
SHIRT_SHD   = (170,  55,  55, 255)
SHORTS      = (100, 160, 220, 255)   # blaue Bermuda-Shorts
SHORTS_SHD  = ( 70, 120, 175, 255)
SHOE_TOP    = (120,  80,  50, 255)
SHOE_SOLE   = ( 60,  40,  25, 255)
STICK       = (200, 200, 200, 255)   # Selfie-Stick (silber)
PHONE       = ( 50,  50,  50, 255)   # Handy am Stick
HAT         = (255, 220,  60, 255)   # gelbe Touristenmütze
HAT_SHD     = (200, 170,  40, 255)
BACKPACK    = ( 65, 160,  65, 255)   # grüner Touristenrucksack


def px(d, x, y, c):
    if 0 <= x < CANVAS_W and 0 <= y < CANVAS_H:
        d.point((x, y), fill=c)


def hline(d, x0, x1, y, c):
    for x in range(x0, x1 + 1):
        px(d, x, y, c)


def vline(d, x, y0, y1, c):
    for y in range(y0, y1 + 1):
        px(d, x, y, c)


def draw_frame(idx):
    img = Image.new('RGBA', (CANVAS_W, CANVAS_H), TRANSPARENT)
    d   = ImageDraw.Draw(img)

    t     = (idx / NUM_FRAMES) * math.pi * 2
    bob   = int(round(abs(math.sin(t * 2)) * 1.5))

    BASE_Y  = 61
    cx      = 22
    hip_y   = BASE_Y - 19 + bob
    chest_y = hip_y  - 12
    neck_y  = chest_y - 2
    head_cy = neck_y  - 6

    swing = math.sin(t) * 10
    fk_x = cx + int(swing * 0.5); fk_y = hip_y + 9
    ff_x = cx + int(swing)
    bk_x = cx - int(swing * 0.5); bk_y = hip_y + 9
    bf_x = cx - int(swing)

    # Selfie-Stick-Arm: immer ausgestreckt nach vorne-oben
    arm_swing_fwd = math.sin(t) * 4
    stick_base_x = cx + 8
    stick_base_y = chest_y + 4
    stick_tip_x  = stick_base_x + 10
    stick_tip_y  = chest_y - 8

    # Rueckwaertiger Arm schwingt
    bae_x = cx - 5 + int(-math.sin(t) * 6)
    bae_y = chest_y + 12

    # ---- Ruecksack ----------------------------------------------------------
    for ry in range(chest_y, hip_y + 1):
        shade = SHIRT_SHD if ry > chest_y + 4 else BACKPACK
        hline(d, cx - 9, cx - 2, ry, shade)

    # ---- Hinteres Bein ------------------------------------------------------
    d.line([(cx, hip_y), (bk_x, bk_y)],        fill=SHORTS_SHD, width=4)
    d.line([(bk_x, bk_y), (bf_x, BASE_Y - 2)], fill=SHORTS_SHD, width=3)
    hline(d, bf_x - 4, bf_x + 4, BASE_Y - 1, SHOE_TOP)
    hline(d, bf_x - 4, bf_x + 4, BASE_Y,     SHOE_SOLE)

    # ---- Hinterer Arm -------------------------------------------------------
    d.line([(cx - 4, chest_y + 2), (bae_x, bae_y)], fill=SHIRT_SHD, width=3)

    # ---- Torso --------------------------------------------------------------
    for ty in range(chest_y, hip_y + 2):
        hw = 7 if ty < chest_y + 5 else 6
        hline(d, cx - hw + 1, cx + hw - 1, ty, SHIRT)
    vline(d, cx + 4, chest_y + 2, hip_y, SHIRT_SHD)
    d.rectangle([cx - 7, chest_y, cx + 7, hip_y + 1], outline=OUTLINE)

    # ---- Selfie-Stick (vorderer Arm + Stick) --------------------------------
    # Arm
    d.line([(cx + 6, chest_y + 2), (stick_base_x, stick_base_y + 4)], fill=SKIN, width=2)
    # Stick-Stange
    d.line([(stick_base_x, stick_base_y + 4), (stick_tip_x, stick_tip_y)], fill=STICK, width=2)
    # Handy oben
    d.rectangle([stick_tip_x - 2, stick_tip_y - 4, stick_tip_x + 2, stick_tip_y], fill=PHONE, outline=OUTLINE)
    # Kleines Linsen-Detail
    px(d, stick_tip_x, stick_tip_y - 2, (100, 200, 255, 255))

    # ---- Vorderes Bein ------------------------------------------------------
    d.line([(cx, hip_y), (fk_x, fk_y)],        fill=SHORTS, width=4)
    d.line([(fk_x, fk_y), (ff_x, BASE_Y - 2)], fill=SHORTS, width=3)
    hline(d, ff_x - 4, ff_x + 5, BASE_Y - 2, SHOE_TOP)
    hline(d, ff_x - 5, ff_x + 5, BASE_Y,     SHOE_SOLE)

    # ---- Hals ---------------------------------------------------------------
    hline(d, cx, cx + 1, neck_y, SKIN)
    hline(d, cx, cx + 1, neck_y + 1, SKIN)

    # ---- Kopf ---------------------------------------------------------------
    for ky in range(head_cy - 4, head_cy + 5):
        dist = abs(ky - head_cy)
        w = {0: 5, 1: 5, 2: 4, 3: 3, 4: 2}.get(dist, 1)
        hline(d, cx - w + 1, cx + w, ky, SKIN)
    px(d, cx - 4, head_cy, OUTLINE)
    px(d, cx + 6, head_cy, OUTLINE)

    # Auge
    px(d, cx + 3, head_cy, OUTLINE)
    px(d, cx + 4, head_cy, OUTLINE)

    # Mund (leichtes Laecheln)
    hline(d, cx + 1, cx + 4, head_cy + 3, OUTLINE)
    px(d, cx + 4, head_cy + 2, OUTLINE)

    # Haare / Muetze
    hline(d, cx - 4, cx + 5, head_cy - 5, HAT)
    hline(d, cx - 5, cx + 6, head_cy - 4, HAT)
    hline(d, cx - 3, cx + 5, head_cy - 3, HAT_SHD)
    # Mutze-Schild vorne
    hline(d, cx + 3, cx + 7, head_cy - 4, HAT)

    return img


def build_sheet(frames):
    sheet = Image.new('RGBA', (CANVAS_W * NUM_FRAMES, CANVAS_H), TRANSPARENT)
    for i, f in enumerate(frames):
        sheet.paste(f, (i * CANVAS_W, 0))
    return sheet


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    frames = []
    for i in range(NUM_FRAMES):
        frame = draw_frame(i)
        path  = os.path.join(OUT_DIR, f'Tourist_walk_{i + 1}.png')
        frame.save(path)
        print(f'  OK  {os.path.basename(path)}')
        frames.append(frame)
    sheet_path = os.path.join(OUT_DIR, 'Tourist_walk_sheet.png')
    build_sheet(frames).save(sheet_path)
    print(f'\n  Sprite-Sheet -> {sheet_path}')
    print(f'\nFertig - {NUM_FRAMES} Frames generiert.')

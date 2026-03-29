#!/usr/bin/env python3
"""
Generiert 3 Pixel-Art-Frames der Tourist-Foto-Stop-Pose.
Frame 1: Kamera heben
Frame 2: Kamera-Klicken (Augen hinter Handy-Screen, breites Laecheln)
Frame 3: Kamera senken / kurz danach
Canvas: 48x64 pro Frame.
Ausgabe:
  assets/sprites/Tourist_foto_1.png ... Tourist_foto_3.png
  assets/sprites/Tourist_foto_sheet.png (144x64)
"""
import os

from PIL import Image, ImageDraw

CANVAS_W   = 48
CANVAS_H   = 64
NUM_FRAMES = 3
OUT_DIR    = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'sprites')

TRANSPARENT = (0,   0,   0,   0)
OUTLINE     = (30,  20,  15,  255)
SKIN        = (230, 185, 140, 255)
SKIN_SHD    = (190, 145, 100, 255)
SHIRT       = (220,  80,  80, 255)
SHIRT_SHD   = (170,  55,  55, 255)
SHORTS      = (100, 160, 220, 255)
SHORTS_SHD  = ( 70, 120, 175, 255)
SHOE_TOP    = (120,  80,  50, 255)
SHOE_SOLE   = ( 60,  40,  25, 255)
STICK       = (200, 200, 200, 255)
PHONE       = ( 50,  50,  50, 255)
PHONE_SCR   = (100, 200, 255, 255)   # Handy-Display leuchtet
HAT         = (255, 220,  60, 255)
HAT_SHD     = (200, 170,  40, 255)
FLASH       = (255, 255, 180, 255)   # Blitz-Effekt

RAISED_HEIGHTS  = [0, -4, -2]     # Stick-Arm pro Frame (negativ = hoeher)
STICK_ANGLES    = [30, 10, 25]    # Grad von senkrecht

def px(d, x, y, c):
    if 0 <= x < CANVAS_W and 0 <= y < CANVAS_H:
        d.point((x, y), fill=c)

def hline(d, x0, x1, y, c):
    for x in range(x0, x1 + 1):
        px(d, x, y, c)

def draw_frame(idx):
    img = Image.new('RGBA', (CANVAS_W, CANVAS_H), TRANSPARENT)
    d   = ImageDraw.Draw(img)

    BASE_Y  = 61
    cx      = 22
    hip_y   = BASE_Y - 19
    chest_y = hip_y  - 12
    neck_y  = chest_y - 2
    head_cy = neck_y  - 6

    # Statische Beinposition (stehend, leicht gespreizt)
    lf_x = cx - 4
    rf_x = cx + 5

    # Stick-Arm-Position basierend auf Frame
    arm_lift = RAISED_HEIGHTS[idx]
    stick_base_x = cx + 7
    stick_base_y = chest_y + 4
    stick_len    = 14
    stick_tip_x  = stick_base_x + stick_len - 4
    stick_tip_y  = chest_y + arm_lift - 6

    is_flash = (idx == 1)

    # ---- Ruecksack ----------------------------------------------------------
    for ry in range(chest_y, hip_y + 1):
        hline(d, cx - 9, cx - 2, ry, SHIRT_SHD)

    # ---- Linkes Bein --------------------------------------------------------
    d.line([(cx - 1, hip_y), (cx - 3, hip_y + 9)],   fill=SHORTS_SHD, width=4)
    d.line([(cx - 3, hip_y + 9), (lf_x, BASE_Y - 2)], fill=SHORTS_SHD, width=3)
    hline(d, lf_x - 4, lf_x + 4, BASE_Y - 1, SHOE_TOP)
    hline(d, lf_x - 4, lf_x + 4, BASE_Y,     SHOE_SOLE)

    # ---- Linker Arm (haengt leicht nach vorne) ------------------------------
    ba_x = cx - 3
    ba_y = chest_y + 13
    d.line([(cx - 4, chest_y + 2), (ba_x, ba_y)], fill=SHIRT_SHD, width=3)

    # ---- Torso --------------------------------------------------------------
    for ty in range(chest_y, hip_y + 2):
        hw = 7 if ty < chest_y + 5 else 6
        hline(d, cx - hw + 1, cx + hw - 1, ty, SHIRT)
    d.rectangle([cx - 7, chest_y, cx + 7, hip_y + 1], outline=OUTLINE)

    # ---- Selfie-Stick-Arm (angehoben) ---------------------------------------
    d.line([(cx + 5, chest_y + 2), (stick_base_x, stick_base_y)], fill=SKIN, width=2)
    d.line([(stick_base_x, stick_base_y), (stick_tip_x, stick_tip_y)], fill=STICK, width=2)
    # Handy-Bildschirm
    phone_col = PHONE_SCR if is_flash else PHONE
    d.rectangle([stick_tip_x - 3, stick_tip_y - 5, stick_tip_x + 3, stick_tip_y], fill=phone_col, outline=OUTLINE)

    # Blitz-Pixel
    if is_flash:
        for dx2 in range(-2, 3):
            for dy2 in range(-2, 3):
                px(d, stick_tip_x + dx2, stick_tip_y - 6 + dy2, FLASH)

    # ---- Rechtes Bein -------------------------------------------------------
    d.line([(cx + 1, hip_y), (cx + 3, hip_y + 9)],   fill=SHORTS, width=4)
    d.line([(cx + 3, hip_y + 9), (rf_x, BASE_Y - 2)], fill=SHORTS, width=3)
    hline(d, rf_x - 4, rf_x + 5, BASE_Y - 2, SHOE_TOP)
    hline(d, rf_x - 4, rf_x + 5, BASE_Y,     SHOE_SOLE)

    # ---- Hals ---------------------------------------------------------------
    hline(d, cx, cx + 1, neck_y, SKIN)
    hline(d, cx, cx + 1, neck_y + 1, SKIN)

    # ---- Kopf ---------------------------------------------------------------
    for ky in range(head_cy - 4, head_cy + 5):
        dist = abs(ky - head_cy)
        w = {0: 5, 1: 5, 2: 4, 3: 3, 4: 2}.get(dist, 1)
        hline(d, cx - w + 1, cx + w, ky, SKIN)

    # Auge (Frame 1: offen; Frame 2: leicht gekniffn/Staunen; Frame 3: blinzelt)
    if idx == 0:
        px(d, cx + 3, head_cy, OUTLINE)
        px(d, cx + 4, head_cy, OUTLINE)
        hline(d, cx + 2, cx + 5, head_cy - 3, (50, 50, 200, 255))  # Augenbraue gespannt
    elif idx == 1:
        # Grosse Augen (Klick-Moment)
        px(d, cx + 2, head_cy - 1, OUTLINE)
        px(d, cx + 3, head_cy - 1, OUTLINE)
        px(d, cx + 4, head_cy - 1, OUTLINE)
        px(d, cx + 2, head_cy,     OUTLINE)
        px(d, cx + 4, head_cy,     OUTLINE)
    else:
        # Blinzeln
        hline(d, cx + 2, cx + 5, head_cy, OUTLINE)

    # Mund – breites Grinsen bei Frame 2
    if idx == 1:
        hline(d, cx - 1, cx + 5, head_cy + 3, OUTLINE)
        px(d, cx - 1, head_cy + 2, OUTLINE)
        px(d, cx + 5, head_cy + 2, OUTLINE)
    else:
        hline(d, cx + 1, cx + 4, head_cy + 3, OUTLINE)

    # Muetze
    hline(d, cx - 4, cx + 5, head_cy - 5, HAT)
    hline(d, cx - 5, cx + 6, head_cy - 4, HAT)
    hline(d, cx - 3, cx + 5, head_cy - 3, HAT_SHD)
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
        path  = os.path.join(OUT_DIR, f'Tourist_foto_{i + 1}.png')
        frame.save(path)
        print(f'  OK  {os.path.basename(path)}')
        frames.append(frame)
    sheet_path = os.path.join(OUT_DIR, 'Tourist_foto_sheet.png')
    build_sheet(frames).save(sheet_path)
    print(f'\n  Sprite-Sheet -> {sheet_path}')
    print(f'\nFertig - {NUM_FRAMES} Frames generiert.')

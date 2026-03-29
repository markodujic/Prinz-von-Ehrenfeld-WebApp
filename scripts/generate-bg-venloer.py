#!/usr/bin/env python3
"""
Generiert den Hintergrund fuer Level 1 – Venloer Strasse.
960x500 Pixel, Pixel-Art-Stil (16-bit SNES).
Schichten (hinten nach vorne):
  1. Himmel (hellblau mit Wolken)
  2. Gebaeude-Silhouetten (hinten, dunkel)
  3. Gebaeude vorne: Doenerladen, Graffiti-Wand, Wohnhaus
  4. Strassenebene: Buergersteig + Strassen-Schiene

Ausgabe: assets/sprites/Bg_venloer.png
"""
import os
import random
from PIL import Image, ImageDraw

W = 960
H = 500
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'sprites')

# Farben
SKY_TOP     = ( 90, 160, 220, 255)
SKY_BOT     = (160, 210, 240, 255)
CLOUD       = (240, 245, 255, 255)
CLOUD_SHD   = (200, 215, 235, 255)

BG_BLDG     = ( 80,  80, 100, 255)   # Hintergrundgebaeude (weit weg)
BG_BLDG2    = ( 60,  60,  80, 255)

WALL_BEIGE  = (220, 200, 170, 255)   # Putzfassade
WALL_SHD    = (185, 165, 138, 255)
WALL_DARK   = (150, 130, 110, 255)

DONER_SIGN  = (200,  30,  30, 255)   # Doenerladen-Schild (rot)
DONER_TEXT  = (255, 220,  50, 255)   # gelbe Schrift
DONER_AWNING= (180,  25,  25, 255)   # Vordach
DONER_STRIP = (255, 200,  40, 255)   # Vordach-Streifen

WINDOW      = (100, 160, 200, 255)   # Fenster
WINDOW_FRAME= (100,  80,  60, 255)
WINDOW_HLT  = (200, 230, 255, 180)   # Fensterglanz

GRAFFITI_1  = (255,  80,  80, 255)
GRAFFITI_2  = ( 80, 200,  80, 255)
GRAFFITI_3  = ( 80,  80, 255, 255)
GRAFFITI_4  = (255, 180,   0, 255)
GRAFFITI_BG = (170, 165, 155, 255)   # Betonwand

SIDEWALK    = (180, 175, 168, 255)   # Buergersteig
SIDEWALK_LN = (160, 155, 148, 255)   # Buergersteig-Fuge
ROAD        = (100,  98,  95, 255)   # Strasse
ROAD_LINE   = (200, 195, 180, 255)   # Randstreifen
TRAM_RAIL   = (140, 120, 100, 255)   # Strassenbahnschiene
TRAM_BOLT   = (100,  90,  80, 255)

OUTLINE     = ( 30,  20,  15, 255)

random.seed(42)


def px(d, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        d.point((x, y), fill=c)


def hline(d, x0, x1, y, c):
    for x in range(max(0, x0), min(W, x1 + 1)):
        px(d, x, y, c)


def vline(d, x, y0, y1, c):
    for y in range(max(0, y0), min(H, y1 + 1)):
        px(d, x, y, c)


def rect(d, x0, y0, x1, y1, fill, outline=None):
    d.rectangle([x0, y0, x1, y1], fill=fill)
    if outline:
        d.rectangle([x0, y0, x1, y1], outline=outline)


def draw_window(d, x, y, w=12, h=14):
    rect(d, x, y, x + w, y + h, WINDOW, WINDOW_FRAME)
    # Kreuzrahmen
    vline(d, x + w // 2, y, y + h, WINDOW_FRAME)
    hline(d, x, x + w, y + h // 2, WINDOW_FRAME)
    # Glanzstreifen
    for gx in range(x + 1, x + w // 2):
        px(d, gx, y + 1, WINDOW_HLT)
        px(d, gx, y + 2, WINDOW_HLT)


def draw_cloud(d, cx, cy, r=18):
    # Blockige Pixel-Art-Wolke
    for ox, oy, cr in [(0, 0, r), (-r + 4, 6, r - 6), (r - 4, 4, r - 7)]:
        for y in range(cy + oy - cr, cy + oy + cr // 2 + 1):
            for x in range(cx + ox - cr, cx + ox + cr + 1):
                if 0 <= x < W and 0 <= y < H:
                    dist = abs(x - (cx + ox)) + abs(y - (cy + oy)) * 1.5
                    if dist < cr:
                        col = CLOUD_SHD if y > cy + oy else CLOUD
                        d.point((x, y), fill=col)


def draw_graffiti_tag(d, x, y, color, size=12):
    """Einfaches pixeliges Graffiti-Tag (abstrakt)."""
    # zufaellige geschwungene Linien simulieren
    rng = random.Random(x + y)
    pts = [(x + rng.randint(0, size), y + rng.randint(0, size)) for _ in range(5)]
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=color, width=2)
    # Aussenrand
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=OUTLINE, width=1)


def draw_image():
    img = Image.new('RGBA', (W, H), SKY_TOP)
    d   = ImageDraw.Draw(img)

    # =========================================================
    # 1. HIMMEL – linearer Farbverlauf (pixelig in Stufen)
    # =========================================================
    sky_h = 200
    for y in range(sky_h):
        t   = y / sky_h
        r_c = int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t)
        g_c = int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t)
        b_c = int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t)
        hline(d, 0, W - 1, y, (r_c, g_c, b_c, 255))

    # Wolken
    draw_cloud(d, 120, 55, 22)
    draw_cloud(d, 380, 40, 18)
    draw_cloud(d, 650, 70, 25)
    draw_cloud(d, 870, 35, 15)

    # =========================================================
    # 2. GEBAEUDE HINTEN (Silhouetten)
    # =========================================================
    bldg_back = [
        (0,   160, 110, 360),
        (100, 130, 200, 360),
        (190, 150, 130, 360),
        (310, 120, 170, 360),
        (470, 140, 90,  360),
        (550, 110, 200, 360),
        (740, 135, 150, 360),
        (880, 155, 80,  360),
    ]
    for (bx, by, bw, bbot) in bldg_back:
        col = BG_BLDG if (bx // 100) % 2 == 0 else BG_BLDG2
        rect(d, bx, by, bx + bw, bbot, col)
        # Einfache Fenster-Reihen
        for wy in range(by + 10, bbot - 20, 20):
            for wx in range(bx + 8, bx + bw - 10, 18):
                w_col = WINDOW if random.random() > 0.3 else (40, 30, 10, 255)
                rect(d, wx, wy, wx + 8, wy + 10, w_col)

    # =========================================================
    # 3. GEBAEUDE VORNE – 3 Hauptbloecke
    # =========================================================
    GND = 360   # Gebaeude-Unterseite

    # --- Block A: Doenerladen (x=0..310) ---
    rect(d, 0, 180, 310, GND, WALL_BEIGE)
    vline(d, 310, 180, GND, WALL_DARK)

    # Doenerladen-Schild (rot, x=10..200, y=182..230)
    rect(d, 10, 182, 290, 230, DONER_SIGN, OUTLINE)

    # Schrift "DÖNER & MEHR" – Pixel-Buchstaben (stilisiert)
    letter_y = 196
    letter_x = 30
    # D
    for ly in range(letter_y, letter_y + 15):
        px(d, letter_x, ly, DONER_TEXT)
    for lx in range(letter_x, letter_x + 8):
        px(d, lx, letter_y, DONER_TEXT)
        px(d, lx, letter_y + 14, DONER_TEXT)
    for ly in range(letter_y, letter_y + 15):
        px(d, letter_x + 9, ly, DONER_TEXT) if abs(ly - (letter_y + 7)) < 6 else None

    # "&"
    for lp in [(letter_x + 18, letter_y + 3), (letter_x + 19, letter_y + 4),
               (letter_x + 17, letter_y + 8), (letter_x + 20, letter_y + 8),
               (letter_x + 18, letter_y + 12), (letter_x + 19, letter_y + 11)]:
        px(d, lp[0], lp[1], DONER_TEXT)

    # Vordach mit Streifen
    rect(d, 0, 232, 310, 250, DONER_AWNING, OUTLINE)
    for sx in range(0, 310, 16):
        rect(d, sx, 232, sx + 8, 250, DONER_STRIP)

    # Schaufenster
    draw_window(d, 20, 262, 60, 80)
    draw_window(d, 100, 262, 60, 80)
    draw_window(d, 180, 262, 60, 80)
    draw_window(d, 255, 262, 40, 80)

    # Tuer
    rect(d, 270, 300, 305, GND, WALL_DARK, OUTLINE)
    px(d, 272, 335, (180, 140, 60, 255))  # Tuerknauf

    # Fenster obere Etage (Doenerladen hat auch Obergeschoss)
    for wx in range(20, 290, 50):
        draw_window(d, wx, 188 + 50 - 40, 35, 25) if wx < 270 else None

    # --- Block B: Graffiti-Wand (x=315..620) ---
    rect(d, 315, 160, 620, GND, GRAFFITI_BG)
    vline(d, 620, 160, GND, WALL_DARK)

    # Betonstruktur (horizontale Fugen)
    for fy in range(180, GND, 15):
        hline(d, 315, 620, fy, WALL_SHD)

    # Graffiti-Tags und -Pieces
    draw_graffiti_tag(d, 330, 180, GRAFFITI_1, 30)
    draw_graffiti_tag(d, 390, 200, GRAFFITI_3, 40)
    draw_graffiti_tag(d, 460, 175, GRAFFITI_2, 50)
    draw_graffiti_tag(d, 530, 220, GRAFFITI_4, 35)

    # Grosses Graffiti-Style-Buchstabe "E" (wie Ehrenfeld)
    gy = 240
    gx = 340
    gs = 3  # pixel-scale
    e_shape = [
        "XXXXX",
        "X    ",
        "XXX  ",
        "X    ",
        "XXXXX",
    ]
    for row, line in enumerate(e_shape):
        for col, ch in enumerate(line):
            if ch == 'X':
                rect(d, gx + col * gs * 2, gy + row * gs * 2,
                        gx + col * gs * 2 + gs + 2, gy + row * gs * 2 + gs,
                        GRAFFITI_1, OUTLINE)

    # Noch ein paar zufaellige Pixel-Punkte als Spray-Dots
    rng2 = random.Random(77)
    for _ in range(200):
        sx = rng2.randint(315, 619)
        sy = rng2.randint(165, GND - 5)
        col = [GRAFFITI_1, GRAFFITI_2, GRAFFITI_3, GRAFFITI_4][rng2.randint(0, 3)]
        px(d, sx, sy, (*col[:3], rng2.randint(80, 180)))

    # Fenster in Graffiti-Wand (zugemauert / verbarrikadiert)
    for wx in range(335, 600, 80):
        rect(d, wx, 175, wx + 40, 215, WALL_DARK)
        # Bretter
        for bx in range(wx, wx + 40, 8):
            vline(d, bx, 175, 215, OUTLINE)

    # --- Block C: Wohnhaus (x=625..960) ---
    rect(d, 625, 170, 960, GND, WALL_BEIGE)

    # Fenster-Raster
    for wy in range(192, GND - 30, 38):
        for wx in range(645, 950, 55):
            draw_window(d, wx, wy, 32, 28)

    # Tuerkis-Highlight-Streife an Hausfassade
    rect(d, 625, 170, 640, GND, WALL_SHD)

    # Hausnummer-Schild
    rect(d, 700, 182, 740, 202, WALL_DARK, OUTLINE)
    # "17" – stilisiert
    vline(d, 712, 186, 198, DONER_TEXT)
    vline(d, 720, 186, 198, DONER_TEXT)
    hline(d, 720, 724, 186, DONER_TEXT)
    hline(d, 720, 724, 192, DONER_TEXT)
    hline(d, 720, 724, 198, DONER_TEXT)

    # Tuer
    rect(d, 820, 305, 860, GND, WALL_SHD, OUTLINE)
    px(d, 857, 335, (180, 140, 60, 255))

    # =========================================================
    # 4. BUERGERSTEIG & STRASSE (Vordergrund)
    # =========================================================
    # Buergersteig (y=360..420)
    rect(d, 0, 360, W, 420, SIDEWALK)
    # Pflasterfugen (horizontal)
    for gy2 in range(368, 420, 12):
        hline(d, 0, W - 1, gy2, SIDEWALK_LN)
    # Vertikale Fugen (versetzt)
    for fx in range(0, W, 40):
        offset = 6 if (fx // 40) % 2 else 0
        vline(d, fx + offset, 360, 420, SIDEWALK_LN)

    # Bordstein
    rect(d, 0, 418, W, 422, WALL_DARK, None)

    # Strasse (y=422..500)
    rect(d, 0, 422, W, H, ROAD)
    # Strassenrand-Linie
    hline(d, 0, W - 1, 422, ROAD_LINE)
    hline(d, 0, W - 1, 423, ROAD_LINE)

    # Strassenbahnschiene (2 Schienen)
    for rail_x_center in [240, 720]:
        for side in [-4, 4]:
            rx = rail_x_center + side
            # Schiene-Koerper
            vline(d, rx, 425, H - 1, TRAM_RAIL)
            vline(d, rx + 1, 425, H - 1, TRAM_RAIL)
            # Befestigungs-Bolzen alle 20px
            for by in range(430, H, 20):
                for bx2 in range(rx - 2, rx + 4):
                    px(d, bx2, by, TRAM_BOLT)

    # Querstreifen-Zebrastreifen (bei x=500)
    for zx in range(485, 535, 8):
        rect(d, zx, 425, zx + 4, H - 1, (200, 198, 190, 255))

    # =========================================================
    # 5. DETAILS: Laternenpfahl, Muelltonnen, Hinweisschilder
    # =========================================================

    # Laternenpfahl bei x=305 und x=615 und x=920
    for lx in [305, 615, 920]:
        vline(d, lx, 250, 360, WALL_DARK)
        vline(d, lx + 1, 250, 360, (80, 80, 80, 255))
        # Arm
        for arm_len in range(0, 18):
            px(d, lx - arm_len, 250 + arm_len // 3, WALL_DARK)
        # Lampe (gelb-weiss)
        rect(d, lx - 18, 248, lx - 12, 254, (255, 240, 100, 255), OUTLINE)
        # Lichtschein
        for ly2 in range(254, 275):
            frac = (ly2 - 254) / 20
            alpha = int(80 * (1 - frac))
            hw = int(10 * (1 - frac * 0.3))
            for glx in range(lx - 18 - hw // 2, lx - 12 + hw // 2):
                if 0 <= glx < W:
                    existing = img.getpixel((glx, ly2))
                    blend = tuple(min(255, existing[i] + (255 - existing[i]) * alpha // 255)
                                  for i in range(3)) + (255,)
                    px(d, glx, ly2, blend)

    # Muelltonnen bei x=440 und x=540
    for tx in [440, 540]:
        rect(d, tx, 338, tx + 20, 362, (70, 70, 70, 255), OUTLINE)
        rect(d, tx - 1, 336, tx + 21, 340, (50, 50, 50, 255), OUTLINE)
        # Deckel
        hline(d, tx, tx + 20, 336, (90, 90, 90, 255))
        # Recycling-Symbol (vereinfacht)
        px(d, tx + 9, 346, (100, 200, 100, 255))
        px(d, tx + 10, 346, (100, 200, 100, 255))
        px(d, tx + 10, 347, (100, 200, 100, 255))

    return img


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    img = draw_image()
    path = os.path.join(OUT_DIR, 'Bg_venloer.png')
    img.save(path)
    print(f'  OK  {os.path.basename(path)}  ({W}x{H}px)')
    print('Fertig.')

#!/usr/bin/env python3
"""
Generiert Pixel-Art-Sprites für die Bierflasche:
 - Bottle_throw.png: intakte Flasche als Projektil
 - Bottle_shatter.png: zerbrochene Flasche als Treffer-Effekt
"""

import os

from PIL import Image, ImageDraw

CANVAS = 32
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'sprites')

TRANSPARENT = (0, 0, 0, 0)
GLASS = (42, 141, 61, 255)
GLASS_DARK = (28, 98, 46, 255)
GLASS_HIGHLIGHT = (165, 232, 170, 180)
CAP = (246, 233, 165, 255)
CAP_DARK = (197, 174, 94, 255)
LABEL = (245, 232, 197, 255)
LABEL_STRIPE = (168, 128, 36, 255)
OUTLINE = (28, 36, 22, 255)
AMBER = (212, 143, 34, 255)
AMBER_DARK = (164, 96, 20, 255)
FOAM = (248, 244, 220, 255)


def px(draw, x, y, color):
    if 0 <= x < CANVAS and 0 <= y < CANVAS:
        draw.point((x, y), fill=color)


def hline(draw, x0, x1, y, color):
    for x in range(x0, x1 + 1):
        px(draw, x, y, color)


def vline(draw, x, y0, y1, color):
    for y in range(y0, y1 + 1):
        px(draw, x, y, color)


def draw_bottle():
    img = Image.new('RGBA', (CANVAS, CANVAS), TRANSPARENT)
    d = ImageDraw.Draw(img)

    hline(d, 12, 18, 2, CAP_DARK)
    hline(d, 12, 18, 3, CAP)
    hline(d, 13, 17, 4, CAP)

    hline(d, 13, 17, 5, GLASS_DARK)
    hline(d, 13, 17, 6, GLASS)
    hline(d, 13, 17, 7, GLASS)

    hline(d, 11, 19, 8, GLASS_DARK)
    hline(d, 10, 20, 9, GLASS)

    for y in range(10, 21):
        hline(d, 10, 20, y, GLASS)
    for y in range(11, 20):
        hline(d, 11, 19, y, GLASS_DARK)

    vline(d, 9, 9, 20, OUTLINE)
    vline(d, 21, 9, 20, OUTLINE)
    hline(d, 10, 20, 21, OUTLINE)
    px(d, 12, 1, OUTLINE)
    px(d, 13, 1, OUTLINE)
    px(d, 18, 2, OUTLINE)
    px(d, 19, 3, OUTLINE)

    hline(d, 12, 18, 14, LABEL)
    hline(d, 12, 18, 15, LABEL)
    hline(d, 12, 18, 16, LABEL)
    hline(d, 12, 18, 17, LABEL)
    hline(d, 12, 18, 18, LABEL)
    hline(d, 13, 17, 15, LABEL_STRIPE)
    hline(d, 13, 17, 17, LABEL_STRIPE)

    px(d, 12, 11, GLASS_HIGHLIGHT)
    px(d, 13, 10, GLASS_HIGHLIGHT)
    px(d, 14, 12, GLASS_HIGHLIGHT)
    px(d, 11, 12, GLASS_HIGHLIGHT)

    hline(d, 12, 18, 22, GLASS_DARK)
    hline(d, 11, 19, 23, OUTLINE)

    return img


def draw_shatter():
    img = Image.new('RGBA', (CANVAS, CANVAS), TRANSPARENT)
    d = ImageDraw.Draw(img)

    shards = [
        [(16, 4), (14, 8), (17, 10), (19, 7)],
        [(12, 9), (10, 13), (13, 14), (15, 11)],
        [(18, 9), (20, 13), (17, 14), (15, 11)],
        [(14, 15), (12, 20), (16, 22), (19, 19)],
        [(20, 16), (23, 19), (21, 23), (18, 19)],
    ]

    for shard in shards:
        d.polygon(shard, fill=GLASS, outline=OUTLINE)

    for p in [(9, 12), (24, 12), (8, 18), (25, 17), (15, 24), (18, 24)]:
        px(d, p[0], p[1], GLASS_HIGHLIGHT)
        px(d, p[0] + 1, p[1], GLASS_HIGHLIGHT)

    for x in range(11, 22):
        if x % 2 == 0:
            px(d, x, 25, AMBER)
            px(d, x, 26, AMBER_DARK)
        else:
            px(d, x, 25, FOAM)
    hline(d, 12, 20, 24, AMBER)
    hline(d, 13, 19, 23, FOAM)

    return img


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    bottle_path = os.path.join(OUT_DIR, 'Bottle_throw.png')
    shatter_path = os.path.join(OUT_DIR, 'Bottle_shatter.png')
    draw_bottle().save(bottle_path)
    draw_shatter().save(shatter_path)
    print(f'  OK  {os.path.basename(bottle_path)}')
    print(f'  OK  {os.path.basename(shatter_path)}')


if __name__ == '__main__':
    main()
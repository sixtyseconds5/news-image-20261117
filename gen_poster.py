#!/usr/bin/env python3
"""Draw THE WORLD IN ONE DAY — a 1024x1024 newspaper poster for 17 Nov 2026.

Run:  python3 gen_poster.py
Writes: entry.png  (1024x1024) in this directory.
Everything is drawn with Pillow shapes and DejaVu fonts; no network, no photos.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
W, H = 1024, 1024

PAPER = (247, 243, 234)
INK = (20, 24, 34)
NAVY = (18, 33, 61)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
SKY = (168, 205, 226)
SEA = (38, 84, 124)
GREY = (90, 96, 104)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)     # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)            # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap using measured text length; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- lead art
def lead_art(d, x, y, w, h):
    """Bridge over a strait, deck broken at a blast; fallen arch in the water."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # sun + clouds
    d.ellipse([x + 18, y + 14, x + 62, y + 58], fill=(245, 205, 92))
    for cx, cy in ((130, 34), (300, 28)):
        d.ellipse([x + cx, y + cy, x + cx + 52, y + cy + 18], fill=(255, 255, 255))
        d.ellipse([x + cx + 12, y + cy - 8, x + cx + 44, y + cy + 8], fill=(255, 255, 255))
    # sea
    sea_y = y + h - 96
    d.rectangle([x, sea_y, x + w, y + h], fill=SEA)
    d.rectangle([x, sea_y, x + w, sea_y + 8], fill=(120, 170, 200))
    # bridge pylons
    for px in (x + 78, x + w - 92):
        d.rectangle([px, y + 62, px + 12, sea_y + 4], fill=(52, 60, 72))
    # cables from pylons toward the gap
    for px, sign in ((x + 84, 1), (x + w - 86, -1)):
        for k in range(3):
            d.line([(px, y + 66 + k * 10),
                    (px + sign * (118 - k * 26), sea_y - 6)],
                   fill=(70, 78, 88), width=2)
    # deck: left span and right span, gap in the middle
    d.rectangle([x, sea_y - 14, x + 168, sea_y + 2], fill=(44, 50, 62))
    d.rectangle([x + w - 168, sea_y - 14, x + w, sea_y + 2], fill=(44, 50, 62))
    # blast plume over the gap
    cx, cy = x + w // 2, y + 88
    d.ellipse([cx - 52, cy - 44, cx + 52, cy + 44], fill=(232, 110, 32))
    d.ellipse([cx - 36, cy - 30, cx + 36, cy + 30], fill=(244, 160, 60))
    d.ellipse([cx - 20, cy - 18, cx + 20, cy + 18], fill=(250, 214, 120))
    for ang in range(0, 360, 45):
        r = 58
        ex = cx + int(r * math.cos(math.radians(ang)))
        ey = cy + int(r * math.sin(math.radians(ang)) * 0.8)
        d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(120, 124, 128))
    # fallen arch segment, tilted, half-submerged in the gap
    seg = [(x + 196, sea_y + 6), (x + 238, sea_y - 2),
           (x + 258, sea_y + 52), (x + 216, sea_y + 60)]
    d.polygon(seg, fill=(52, 60, 72))
    d.line(seg + [seg[0]], fill=(30, 34, 42), width=2)
    # wave lines
    for row, wy in enumerate((sea_y + 26, sea_y + 52, sea_y + 76)):
        for k in range(6):
            wx = x + 14 + k * 70 + (row % 2) * 20
            d.arc([wx, wy, wx + 34, wy + 18], 180, 360, fill=(220, 235, 245), width=2)
    # small boat held back from the gap, bottom left
    bx, by = x + 34, sea_y + 62
    d.polygon([(bx, by), (bx + 64, by), (bx + 54, by + 14), (bx + 10, by + 14)],
              fill=(24, 28, 36))
    d.line([(bx + 32, by), (bx + 32, by - 18)], fill=(24, 28, 36), width=2)
    d.polygon([(bx + 32, by - 18), (bx + 32, by - 2), (bx + 50, by - 2)],
              fill=(240, 240, 235))


# ---------------------------------------------------------------- grid art
def art_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(31, 58, 74))
    # radar dome, top left
    d.arc([x + 8, y + 6, x + 88, y + 86], 180, 360, fill=(240, 200, 80), width=3)
    d.ellipse([x + 26, y + 42, x + 70, y + 66], fill=(240, 244, 246))
    d.rectangle([x + 26, y + 60, x + 70, y + 66], fill=(240, 244, 246))
    # tanker hull + superstructure
    d.rectangle([x + 18, y + h - 26, x + w - 18, y + h - 12], fill=(16, 18, 22))
    d.rectangle([x + w - 78, y + h - 52, x + w - 34, y + h - 26], fill=(235, 238, 240))
    d.rectangle([x + w - 78, y + h - 58, x + w - 34, y + h - 52], fill=(178, 34, 34))
    # drones: small yellow diamonds with rotor ticks
    for dx, dy in ((150, 34), (196, 58), (128, 62)):
        d.polygon([(x + dx, y + dy - 6), (x + dx + 7, y + dy),
                   (x + dx, y + dy + 6), (x + dx - 7, y + dy)], fill=(245, 205, 92))
        d.line([(x + dx - 10, y + dy - 9), (x + dx + 10, y + dy - 9)],
               fill=(245, 205, 92), width=2)


def art_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 216))
    fw, fh = 88, 52
    # US flag
    fx, fy = x + 10, y + 14
    for s in range(7):
        d.rectangle([fx, fy + s * 7, fx + fw, fy + s * 7 + 7],
                    fill=(178, 34, 34) if s % 2 == 0 else (255, 255, 255))
    d.rectangle([fx, fy, fx + 36, fy + 28], fill=(40, 60, 120))
    # China flag
    fx = x + 110
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 50, 38))
    d.ellipse([fx + 14, fy + 10, fx + 34, fy + 30], fill=(250, 210, 60))
    # Russia flag
    fx = x + 210
    for s, col in enumerate(((255, 255, 255), (40, 80, 180), (200, 40, 40))):
        d.rectangle([fx, fy + s * 17, fx + fw, fy + (s + 1) * 17], fill=col)
    # summit table + microphones
    d.rectangle([x + 10, y + h - 22, x + w - 10, y + h - 12], fill=(120, 82, 44))
    for mx in (54, 154, 254):
        d.line([(x + mx, y + h - 22), (x + mx, y + h - 44)], fill=(30, 30, 30), width=2)
        d.ellipse([x + mx - 6, y + h - 52, x + mx + 6, y + h - 40], fill=(30, 30, 30))


def art_jets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(186, 214, 235))
    d.ellipse([x + w - 62, y + 18, x + w - 14, y + 66], fill=(245, 205, 92))
    d.line([(x + 10, y + h - 22), (x + w - 10, y + h - 22)],
           fill=(255, 255, 255), width=2)
    for jx, jy, sc in ((30, 42, 1.0), (168, 22, 0.72)):
        s = sc
        body = [(x + jx, y + jy), (x + jx + 74 * s, y + jy - 6 * s),
                (x + jx + 92 * s, y + jy + 2 * s), (x + jx + 74 * s, y + jy + 10 * s),
                (x + jx + 20 * s, y + jy + 8 * s)]
        d.polygon(body, fill=(96, 102, 110))
        d.polygon([(x + jx + 34 * s, y + jy - 2 * s), (x + jx + 52 * s, y + jy - 22 * s),
                   (x + jx + 62 * s, y + jy - 2 * s)], fill=(80, 86, 94))
        d.polygon([(x + jx + 44 * s, y + jy + 6 * s), (x + jx + 58 * s, y + jy + 24 * s),
                   (x + jx + 68 * s, y + jy + 6 * s)], fill=(80, 86, 94))


def art_globe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 234, 222))
    cx, cy, r = x + w // 2, y + h // 2 + 4, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 150, 200))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    d.ellipse([cx - 14, cy - r, cx + 14, cy + r], outline=(255, 255, 255), width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=2)
    d.arc([cx - r, cy - 22, cx + r, cy + 22], 0, 360, fill=(255, 255, 255), width=2)
    d.ellipse([cx - 30, cy - 22, cx - 8, cy - 2], fill=(110, 180, 110))
    d.ellipse([cx + 2, cy + 8, cx + 26, cy + 30], fill=(110, 180, 110))
    # red pin
    px, py = cx + 26, cy - 34
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=(200, 40, 40))
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
    d.polygon([(px - 6, py + 4), (px + 6, py + 4), (px, py + 16)], fill=(200, 40, 40))


def art_pentagon(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 234, 222))
    d.text((x + 10, y + 8), "AUDIT: 9TH FAIL", font=SANS_B(15), fill=RED)
    cx, cy, r = x + w // 2, y + h // 2 + 12, 42
    pts = []
    for k in range(5):
        ang = math.radians(-90 + k * 72)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=(150, 156, 162))
    inner = []
    for k in range(5):
        ang = math.radians(-90 + k * 72)
        inner.append((cx + r * 0.45 * math.cos(ang), cy + r * 0.45 * math.sin(ang)))
    d.polygon(inner, fill=(222, 234, 222))


def art_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 22, 44))
    cx, cy = x + w // 2, y + h // 2
    # gold dashed frame
    for k in range(9):
        d.rectangle([x + 96 + k * 13, y + 10, x + 96 + k * 13 + 8, y + 16], fill=GOLD)
        d.rectangle([x + 96 + k * 13, y + h - 16, x + 96 + k * 13 + 8, y + h - 10], fill=GOLD)
    for k in range(5):
        d.rectangle([x + 96, y + 20 + k * 13, x + 102, y + 20 + k * 13 + 8], fill=GOLD)
        d.rectangle([x + w - 102, y + 20 + k * 13, x + w - 96, y + 20 + k * 13 + 8], fill=GOLD)
    d.rectangle([cx - 34, cy - 34, cx + 34, cy + 34], fill=(38, 52, 92),
                outline=GOLD, width=3)
    d.text((cx - 22, cy - 18), "AI", font=SANS_B(30), fill=(255, 255, 255))
    d.line([(x + 14, y + h - 18), (x + w - 14, y + h - 18)], fill=(120, 140, 180), width=2)


# ---------------------------------------------------------------- stories
LEAD = ("UKRAINE · RUSSIA",
        "Ukraine hits Crimea bridge again as Russia strikes Kyiv crossings",
        "Kyiv says the road arch collapsed, blocking shipping; "
        "Russia hit Kyiv's two bridges.")

GRID = [
    ("MIDDLE EAST",
     "Iran fires drones at a US base in Bahrain",
     "Tehran says it hit a US radar; Bahrain says intercepted.",
     art_tanker),
    ("ASIA · DIPLOMACY",
     "Xi-Trump-Putin summit confirmed",
     "Thursday in Shenzhen, a first: nuclear arms and Iran.",
     art_flags),
    ("ASIA · SECURITY",
     "Japan scrambles jets over Russian planes",
     "First breach since Sept 2024; Tokyo protested to Moscow.",
     art_jets),
    ("EUROPE · MIGRATION",
     "Five states plan a Rwanda migrant hub",
     "Pilot hub for 100 rejected asylum seekers, from 2027.",
     art_globe),
    ("UNITED STATES",
     "Pentagon fails its audit for a ninth year",
     "Auditors still cannot verify $4.8 trillion in books.",
     art_pentagon),
    ("TECHNOLOGY",
     "US moves to close the AI-chip loophole",
     "Renting AI compute to China now needs a license.",
     art_chip),
]

STRIP = ("UN: 128 states in Geneva weigh binding killer-robot rules · "
         "UK sanctions eight West Bank settlement firms · "
         "Measles: US loses elimination status; 13 babies born with it")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 118], fill=NAVY)
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_B(54)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 12), title, font=tf, fill=(247, 243, 234))
    hline(d, 36, W - 36, 84, GOLD, width=2)
    date = "TUESDAY · 17 NOVEMBER 2026"
    df = SANS_B(24)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 90), date, font=df, fill=GOLD)

    # --- lead story ---
    lead_art(d, 36, 130, 430, 268)
    tx = 486
    twidth = W - 36 - tx
    d.text((tx, 132), LEAD[0], font=SANS_B(16), fill=RED)
    head_lines = wrap(d, LEAD[1], SERIF_B(33), twidth)
    y = draw_lines(d, head_lines, tx, 156, SERIF_B(33), INK, 40)
    deck_lines = wrap(d, LEAD[2], SANS(23), twidth)
    draw_lines(d, deck_lines, tx, y + 8, SANS(23), (60, 64, 72), 29)
    hline(d, 36, W - 36, 412, (150, 144, 132), width=2)

    # --- grid: 2 rows x 3 columns ---
    col_w, gap = 308, 12
    cols = [36, 36 + col_w + gap, 36 + 2 * (col_w + gap)]
    rows_y = [426, 682]
    for i, (kicker, headline, deck, art) in enumerate(GRID):
        x = cols[i % 3]
        iy = rows_y[i // 3]
        art(d, x, iy, col_w, 108)
        d.text((x, iy + 116), kicker, font=SANS_B(16), fill=RED)
        hl = wrap(d, headline, SERIF_B(25), col_w)
        y = draw_lines(d, hl, x, iy + 138, SERIF_B(25), INK, 30)
        dl = wrap(d, deck, SANS(20), col_w)[:2]
        draw_lines(d, dl, x, y + 4, SANS(20), (60, 64, 72), 25)

    # --- also-today strip ---
    hline(d, 36, W - 36, 938, (150, 144, 132), width=2)
    label = "ALSO TODAY"
    lf = SANS_B(18)
    lw = d.textlength(label, font=lf)
    d.text((36, 952), label, font=lf, fill=RED)
    strip_lines = wrap(d, STRIP, SANS(18), W - 36 - (36 + lw + 14))[:2]
    draw_lines(d, strip_lines, 36 + lw + 14, 952, SANS(18), INK, 24)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print(f"wrote {out} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    build()

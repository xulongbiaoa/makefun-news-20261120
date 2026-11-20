#!/usr/bin/env python3
"""Render the make.fun news-image-20261120 entry: a newspaper front page
summing up Friday 20 November 2026. Dev-only script (PIL); the submitted
program is main.py, which copies the rendered entry.png.

All facts were verified against Reuters / Bloomberg / AP / AFP / UN News /
SCMP coverage of 20 November 2026 before rendering.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 250, 246)
INK = (22, 20, 18)
RED = (178, 34, 24)
GREY = (105, 100, 92)
LIGHT = (235, 232, 224)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def tracked(draw, xy, text, font, fill, tracking=3):
    """Draw text with manual letter spacing."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x


def wrap(draw, text, font, width):
    """Greedy word wrap to a pixel width."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# --- Continents as (lon, lat) outlines, plotted equirectangularly. ---
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-75, 62), (-65, 60), (-55, 52), (-60, 47), (-70, 44), (-75, 40),
     (-80, 32), (-81, 26), (-84, 30), (-90, 29), (-97, 26), (-105, 22),
     (-110, 24), (-115, 30), (-120, 34), (-125, 40), (-125, 49), (-130, 55),
     (-140, 60), (-155, 58), (-165, 60), (-168, 66)],
    [(-58, 64), (-45, 60), (-40, 64), (-30, 68), (-22, 70), (-25, 76),
     (-40, 80), (-55, 76), (-60, 74), (-58, 64)],
    [(-80, 10), (-75, 12), (-70, 12), (-62, 10), (-55, 6), (-50, 0),
     (-44, -3), (-38, -5), (-35, -9), (-40, -15), (-42, -22), (-48, -28),
     (-52, -33), (-58, -38), (-65, -41), (-68, -47), (-70, -52), (-73, -53),
     (-74, -48), (-73, -40), (-72, -30), (-70, -20), (-75, -15), (-80, -6),
     (-81, 0), (-80, 10)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (3, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (32, 66),
     (40, 68), (45, 66), (40, 60), (35, 55), (30, 50), (28, 45), (23, 40),
     (20, 40), (15, 38), (12, 44), (8, 44), (3, 43), (-2, 37), (-6, 36),
     (-10, 36)],
    [(-17, 15), (-10, 30), (-5, 35), (10, 37), (20, 32), (30, 31),
     (35, 28), (37, 22), (40, 15), (43, 11), (48, 11), (51, 10), (46, 5),
     (42, 0), (40, -5), (36, -10), (35, -18), (32, -26), (28, -33),
     (20, -35), (16, -30), (12, -18), (9, -1), (9, 4), (-8, 5), (-13, 8),
     (-17, 15)],
    [(40, 68), (50, 70), (60, 72), (70, 73), (80, 73), (90, 75), (100, 77),
     (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 70),
     (170, 67), (178, 65), (170, 60), (162, 58), (158, 52), (150, 60),
     (142, 55), (140, 45), (135, 43), (130, 38), (127, 35), (122, 32),
     (120, 28), (115, 23), (110, 20), (108, 12), (105, 9), (100, 8),
     (98, 12), (95, 16), (92, 21), (88, 22), (85, 19), (80, 15), (77, 8),
     (75, 12), (72, 20), (68, 23), (66, 25), (62, 25), (58, 26), (56, 27),
     (52, 28), (50, 30), (48, 30), (44, 29), (42, 20), (40, 15), (43, 12),
     (45, 12), (50, 15), (55, 17), (58, 22), (60, 25), (58, 28), (54, 26),
     (50, 26), (48, 24), (45, 25), (42, 27), (40, 30), (38, 32), (36, 36),
     (40, 40), (42, 45), (40, 50), (38, 55), (40, 60), (40, 68)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20), (113, -22)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (141, 42), (143, 44),
     (145, 44), (142, 40), (140, 36), (137, 34), (132, 33), (130, 31)],
]
# Cities of the day's stories: (lon, lat)
CITIES = [(114.1, 22.5), (30.5, 50.4), (46.7, 24.7),
          (4.3, 52.1), (-74.0, 40.7), (30.7, 36.9)]


def draw_world(draw, box):
    """Dot-grid world map inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    mask = Image.new("L", (360, 135), 0)
    md = ImageDraw.Draw(mask)
    for poly in CONTINENTS:
        pts = [(lon + 180, 78 - lat) for lon, lat in poly]
        md.polygon(pts, fill=255)
    lon_step, lat_step = 5, 5
    for lon in range(-180, 180, lon_step):
        for lat in range(78, -57, -lat_step):
            if mask.getpixel((lon + 180, 78 - lat)):
                px = x0 + (lon + 180) / 360 * (x1 - x0)
                py = y0 + (78 - lat) / 134 * (y1 - y0)
                r = 2.0
                draw.ellipse([px - r, py - r, px + r, py + r], fill=(60, 55, 48))
    for lon, lat in CITIES:
        px = x0 + (lon + 180) / 360 * (x1 - x0)
        py = y0 + (78 - lat) / 134 * (y1 - y0)
        draw.ellipse([px - 4.5, py - 4.5, px + 4.5, py + 4.5], fill=RED)
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], outline=RED, width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36                      # side margin
    CW = 952                    # content width
    X1 = M + CW

    # ---- Masthead ----
    d.text((M, 24), "THE WORLD IN ONE DAY", font=f(FONTB, 21), fill=RED)
    # DATE CHECKED box, top right
    box = (X1 - 218, 20, X1, 52)
    d.rectangle(box, fill=RED)
    d.text((box[0] + 14, 27), "DATE CHECKED", font=f(FONTB, 19), fill=(255, 255, 255))
    d.text((M, 48), "Friday 20 November 2026", font=f(FONTB, 56), fill=INK)
    d.text((M, 116), "Shenzhen  ·  Kyiv  ·  New York  ·  Riyadh  ·  The Hague  ·  Antalya",
           font=f(FONT, 19), fill=GREY)
    d.rectangle([M, 142, X1, 146], fill=INK)
    d.rectangle([M, 150, X1, 151], fill=INK)

    # ---- Three lead columns ----
    cols = [
        ("SHENZHEN  ·  DIPLOMACY",
         "TRUMP, XI, PUTIN SIGN \u2018PEACE DECLARATION\u2019",
         "First-ever three-way summit: 80 minutes at Kylin Villa. The trio "
         "vow a nuclear war \u2018cannot be won and must never be fought\u2019, "
         "pledge UN reform and more oil supply, and curb the ICC. "
         "Trump calls it \u2018momentous\u2019."),
        ("KYIV  ·  WAR",
         "RUSSIA\u2019S BIGGEST AIR ASSAULT ON KYIV",
         "404 drones and 111 missiles overnight: at least 9 killed, 30 hurt, "
         "three bridges over the Dnipro hit, and power, heating and water cut. "
         "A day earlier, strikes damaged embassies and St Volodymyr Cathedral."),
        ("WALL STREET  ·  MARKETS",
         "AI ROUT: NASDAQ \u22125.3%, S&P IN CORRECTION",
         "Nvidia \u221214% as Reuters reports the SEC is probing its accounts. "
         "The S&P 500 falls a seventh straight day; Asia follows \u2014 Nikkei "
         "\u22124.8%, KOSPI \u22125.2%, Taiwan \u22126.6%. Bitcoin slips below $60,000."),
    ]
    col_w, gap = 300, 26
    y = 160
    for i, (kicker, head, body) in enumerate(cols):
        x = M + i * (col_w + gap)
        d.text((x, y), kicker, font=f(FONTB, 16), fill=RED)
        hy = y + 26
        for line in wrap(d, head, f(FONTB, 29), col_w):
            d.text((x, hy), line, font=f(FONTB, 29), fill=INK)
            hy += 36
        d.rectangle([x, hy + 4, x + 64, hy + 7], fill=RED)
        by = hy + 18
        for line in wrap(d, body, f(FONT, 20), col_w):
            d.text((x, by), line, font=f(FONT, 20), fill=INK)
            by += 27

    # ---- Markets strip ----
    sy = 568
    d.rectangle([M, sy, X1, sy + 84], fill=INK)
    d.text((M + 16, sy + 12), "MARKETS \u2014 FRIDAY\u2019S CLOSE",
           font=f(FONTB, 17), fill=(255, 255, 255))
    strip = [("NASDAQ", "\u22125.3%"), ("S&P 500", "\u22123.7%"),
             ("NASDAQ 100", "\u22125.6%"), ("DOW", "\u22121.9%"),
             ("NIKKEI", "\u22124.8%"), ("KOSPI", "\u22125.2%"),
             ("TAIEX", "\u22126.6%"), ("BITCOIN LOW", "$58.8K"),
             ("GOLD LOW", "$3,515"), ("VIX", "37")]
    sx, sw = M + 16, 186
    for i, (name, val) in enumerate(strip):
        x = sx + (i % 5) * sw
        yy = sy + 38 + (i // 5) * 22
        d.text((x, yy), name, font=f(FONTB, 13), fill=(170, 165, 155))
        vw = d.textlength(val, font=f(FONTB, 14))
        d.text((x + 168 - vw, yy - 1), val, font=f(FONTB, 14), fill=(255, 120, 100))

    # ---- World map ----
    my = 662
    d.text((M, my), "WHERE IT HAPPENED", font=f(FONTB, 17), fill=INK)
    d.text((M + 240, my), "Red dots: Shenzhen, Kyiv, Riyadh, The Hague, New York, Antalya",
           font=f(FONT, 15), fill=GREY)
    draw_world(d, (M, my + 24, X1, my + 134))

    # ---- Also on Friday (single column, one line each) ----
    ly = 806
    d.rectangle([M, ly, X1, ly + 2], fill=INK)
    d.text((M, ly + 10), "ALSO ON FRIDAY 20 NOVEMBER \u2014 8 MORE STORIES",
           font=f(FONTB, 19), fill=INK)
    items = [
        ("THE HAGUE", "World court rules Myanmar committed genocide against the "
         "Rohingya \u2014 a first for any state (9\u20136)."),
        ("RIYADH", "Houthi missile hits the PIF Tower, the capital\u2019s tallest; "
         "windows blown out over 7\u20138 floors, no injuries."),
        ("WASHINGTON", "White House fires cyber chief Sean Cairncross after a week "
         "of tech outages."),
        ("WASHINGTON", "Trump disclosed buying up to $265,000 of Nvidia stock "
         "in September."),
        ("WASHINGTON", "Fed: a December rate hike is priced at about 95%; "
         "Waller floats 50bp."),
        ("ANTALYA", "COP31 runs into overtime as the draft drops any "
         "fossil-fuel phase-out."),
        ("BRUSSELS", "EU and UK sign a post-Brexit reset deal on food, carbon "
         "markets and youth mobility."),
        ("NEW YORK", "Anthropic falls 9% a day after its blockbuster "
         "stock-market debut."),
    ]
    iy = ly + 40
    for i, (place, text) in enumerate(items):
        yy = iy + i * 22
        d.text((M, yy), place + " \u2014 ", font=f(FONTB, 15), fill=RED)
        pw = d.textlength(place + " \u2014 ", font=f(FONTB, 15))
        d.text((M + pw, yy), text, font=f(FONT, 15), fill=INK)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()

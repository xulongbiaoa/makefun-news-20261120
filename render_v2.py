#!/usr/bin/env python3
"""Render v2 of the make.fun news-image-20261120 entry: a newspaper front
page summing up Friday 20 November 2026 — 35 stories, 7 regions, four
illustrated leads, a UTC timeline and the full day in a regional grid.

Dev-only script (PIL); the submitted program is main.py, which copies the
rendered entry.png. Facts: all items were verified in-session on
2026-11-21 against Reuters / AP / AFP / IMD / Al Jazeera / RNZ and other
named outlets before rendering (see the goal's v2 story list).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 250, 246)
INK = (22, 20, 18)
RED = (178, 34, 24)
GREY = (105, 100, 92)
PALE = (243, 240, 232)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


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


# ---------------------------------------------------------------- stories
LEADS = [
    ("SHENZHEN \u00b7 DIPLOMACY", "summit",
     "TRUMP, XI, PUTIN SIGN \u2018PEACE DECLARATION\u2019",
     "First three-way summit: 80 minutes at Kylin Villa. Nuclear war "
     "\u2018cannot be won and must never be fought\u2019; UN reform, oil supply "
     "and ICC curbs pledged."),  # AP / Reuters / AFP
    ("KYIV \u00b7 WAR", "kyiv",
     "404 DRONES, 111 MISSILES: BIGGEST ASSAULT ON KYIV",
     "At least 9 killed, 30 hurt; three bridges over the Dnipro hit; "
     "power, heat and water cut across the capital."),  # Reuters / AP
    ("ODISHA \u00b7 WEATHER", "akvan",
     "CYCLONE AKVAN MAKES LANDFALL IN INDIA",
     "Crossed the coast at Gopalpur at 07:30 IST, winds 70\u201380 km/h. "
     "440,000 people moved to safety; no major damage. Odisha\u2019s first "
     "November landfall since 1995."),  # IMD / The Hindu
    ("MARKETS \u00b7 TECH", "selloff",
     "AI ROUT: NASDAQ \u22125.3%, NVIDIA \u221214%",
     "An SEC-probe report sinks Nvidia; the S&P 500 enters correction. "
     "Nikkei \u22124.8%, KOSPI \u22125.2%, Taiwan \u22126.6%. Bitcoin below $60,000."),
    # Reuters closing data
]

GRID = [
    ("NORTH AMERICA", [
        "White House fires cyber chief Sean Cairncross after a week of tech outages",
        "Trump disclosed buying up to $265,000 of Nvidia stock in September",
        "Markets price a December Fed hike at about 95%; Waller floats 50bp",
        "Anthropic falls 9% a day after its blockbuster market debut",
        "Mamdani plan: close Rikers Island by 2032; inmates 6,600 to 4,100",
        "Voyager 1\u2019s signal now takes a full light-day to reach Earth",
    ]),
    ("LATIN AMERICA", [
        "Haiti police raid in Martissant, Port-au-Prince kills 34+ gang members",
        "Tesla opens its first Argentine store, in Buenos Aires",
        "CONMEBOL unanimously backs Infantino for another FIFA term",
    ]),
    ("EUROPE", [
        "World Court: Myanmar committed genocide against the Rohingya, 9\u20136",
        "Merz warns a \u2018new Yalta\u2019 will not bring peace; calls Shenzhen a photo-op",
        "EU and UK sign post-Brexit reset on food, carbon and youth mobility",
        "Denmark\u2019s parliament approves the US\u2013Greenland security deal 109\u20130",
        "Poland: two Russian Kh-101s and a drone fell on our soil \u2014 \u2018provocation\u2019",
        "Estonia to close its border with Russia for at least six months",
        "Georgia declares Nov 22 a day of mourning after Tbilisi gas blast kills 6",
        "Ukrainian drones reportedly strike Russia\u2019s Dorogobuzh chemical plant",
    ]),
    ("MIDDLE EAST", [
        "Houthi missile hits Riyadh\u2019s PIF Tower (floors 7\u20138); no injuries",
        "Trump defers a decision on striking Iran until after New Year",
        "Tanker ablaze after projectile hit off Khasab, Hormuz; crew safe",
        "Iraqi forces deploy in Jurf al-Sakhar against Kataib Hezbollah",
    ]),
    ("AFRICA", [
        "Angola to pay about $1.8bn for a 10% stake in De Beers",
        "Funeral barge capsizes in Nigeria\u2019s Bayelsa; rescue under way Friday",
        "Congo\u2019s Bundibugyo Ebola outbreak passes 11,000 cases, 5,500 dead",
    ]),
    ("ASIA", [
        "COP31 in Antalya runs overtime; the draft drops any fossil-fuel phase-out",
        "IMF chief in Shenzhen: public debt to top 100% of GDP, highest since WWII",
    ]),
    ("OCEANIA", [
        "Tonga declares a 27-day national emergency over El Ni\u00f1o drought",
        "Fiji declares a state of disaster over the El Ni\u00f1o drought",
        "Cyclone Xavier weakens to category 4 in the Pacific",
        "World Rugby suspends Oceania Rugby\u2019s council membership",
    ]),
]

TIMELINE = [
    ("00:40", "Kyiv barrage alerts"),
    ("02:00", "Akvan landfall, Odisha"),
    ("04:50", "Shenzhen summit opens"),
    ("15:00", "Tanker hit in Hormuz"),
    ("19:38", "GTA VI record"),
    ("21:00", "US close \u22125.3%"),
]

MARKETS = [("NASDAQ", "\u22125.3%"), ("S&P 500", "\u22123.7%"),
           ("NASDAQ 100", "\u22125.6%"), ("DOW", "\u22121.9%"),
           ("NIKKEI", "\u22124.8%"), ("KOSPI", "\u22125.2%"),
           ("TAIEX", "\u22126.6%"), ("BITCOIN LOW", "$58.8K"),
           ("GOLD LOW", "$3,515"), ("VIX", "37")]


# ------------------------------------------------------------ illustrations
def illo_summit(d, x, y, w, h):
    """Three flags over a summit table line."""
    base = y + h - 4
    d.line([x + 6, base, x + w - 6, base], fill=INK, width=2)
    for i in range(3):
        px = x + 30 + i * (w - 60) // 2
        d.line([px, y + 4, px, base], fill=INK, width=2)
        if i == 0:
            d.rectangle([px, y + 4, px + 28, y + 18], fill=(200, 40, 30), outline=INK)
        elif i == 1:
            d.rectangle([px, y + 4, px + 28, y + 18], fill=(40, 70, 160), outline=INK)
        else:
            d.rectangle([px, y + 4, px + 28, y + 18], outline=INK)
            d.rectangle([px, y + 9, px + 28, y + 13], fill=(40, 70, 160))
            d.rectangle([px, y + 13, px + 28, y + 18], fill=(200, 40, 30))


def illo_kyiv(d, x, y, w, h):
    """Bridge silhouette with missile streaks."""
    base = y + h - 6
    d.line([x + 4, base - 12, x + w - 4, base - 12], fill=INK, width=3)
    for tx in (x + 38, x + w - 38):
        d.line([tx, y + 12, tx, base - 12], fill=INK, width=3)
    d.arc([x + 28, base - 38, x + w - 28, base + 6], 180, 360, fill=INK, width=2)
    d.line([x + 10, base, x + w - 10, base], fill=INK, width=2)
    for sx, sy in ((x + 28, y + 2), (x + 82, y + 0), (x + 136, y + 4)):
        d.line([sx, sy, sx + 20, sy + 14], fill=RED, width=3)
        d.ellipse([sx + 18, sy + 12, sx + 25, sy + 19], fill=RED)


def illo_akvan(d, x, y, w, h):
    """Cyclone spiral over wavy sea."""
    cx, cy = x + w // 2, y + h // 2 - 5
    for r, a0 in ((9, 20), (17, 200), (25, 30), (33, 210)):
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 250, fill=INK, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    for i in range(2):
        wy = y + h - 10 + i * 5
        for sx in range(x + 14, x + w - 26, 24):
            d.arc([sx, wy - 4, sx + 16, wy + 4], 0, 180, fill=GREY, width=2)


def illo_selloff(d, x, y, w, h):
    """Jagged falling chart line with a red arrow."""
    d.line([x + 10, y + 4, x + 10, y + h - 8], fill=GREY, width=2)
    d.line([x + 10, y + h - 8, x + w - 6, y + h - 8], fill=GREY, width=2)
    pts = [(x + 16, y + 10), (x + 52, y + 7), (x + 82, y + 20),
           (x + 112, y + 15), (x + 142, y + 30), (x + 172, y + 27),
           (x + w - 18, y + h - 14)]
    d.line(pts, fill=RED, width=3)
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 12, ey - 1), (ex - 2, ey - 11)], fill=RED)


ILLOS = {"summit": illo_summit, "kyiv": illo_kyiv,
         "akvan": illo_akvan, "selloff": illo_selloff}


# ------------------------------------------------------------------- grid
def grid_columns():
    return [[GRID[0], GRID[1]], [GRID[2], GRID[3]], [GRID[4], GRID[5], GRID[6]]]


def column_height(draw, col, col_w, font, lh):
    hgt = 0
    for name, items in col:
        hgt += 22
        for it in items:
            hgt += len(wrap(draw, it, font, col_w)) * lh + 2
        hgt += 6
    return hgt


def draw_grid(draw, x, y, col_w, font, lh):
    head_font = f(FONTB, 13)
    for ci, col in enumerate(grid_columns()):
        cx = x + ci * (col_w + 24)
        cy = y
        for name, items in col:
            draw.text((cx, cy), name, font=head_font, fill=RED)
            cy += 22
            for it in items:
                for line in wrap(draw, it, font, col_w):
                    draw.text((cx, cy), line, font=font, fill=INK)
                    cy += lh
                cy += 2
            cy += 6


# ------------------------------------------------------------------- main
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36
    CW = 952
    X1 = M + CW

    # ---- Masthead ----
    d.text((M, 16), "THE WORLD IN ONE DAY", font=f(FONTB, 20), fill=RED)
    box = (X1 - 218, 12, X1, 44)
    d.rectangle(box, fill=RED)
    d.text((box[0] + 14, 19), "DATE CHECKED", font=f(FONTB, 18), fill=(255, 255, 255))
    d.text((M, 32), "Friday 20 November 2026", font=f(FONTB, 48), fill=INK)
    d.text((M, 90), "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY STORY DATED 20 NOVEMBER 2026",
           font=f(FONTB, 16), fill=INK)
    d.rectangle([M, 112, X1, 116], fill=INK)
    d.rectangle([M, 120, X1, 121], fill=INK)

    # ---- Four illustrated leads (flow layout) ----
    y = 130
    col_w = (CW - 3 * 18) // 4  # 224
    lead_bottom = y
    for i, (kicker, illo, head, body) in enumerate(LEADS):
        x = M + i * (col_w + 18)
        ILLOS[illo](d, x, y, col_w, 44)
        ky = y + 50
        d.text((x, ky), kicker, font=f(FONTB, 12), fill=RED)
        hy = ky + 18
        for line in wrap(d, head, f(FONTB, 18), col_w):
            d.text((x, hy), line, font=f(FONTB, 18), fill=INK)
            hy += 21
        d.rectangle([x, hy + 2, x + 52, hy + 5], fill=RED)
        by = hy + 11
        for line in wrap(d, body, f(FONT, 11), col_w):
            d.text((x, by), line, font=f(FONT, 11), fill=INK)
            by += 14
        lead_bottom = max(lead_bottom, by)

    # ---- GTA VI culture band ----
    gy = int(lead_bottom) + 6
    d.rectangle([M, gy, X1, gy + 40], fill=PALE)
    d.rectangle([M, gy, M + 5, gy + 40], fill=RED)
    d.text((M + 18, gy + 4), "CULTURE \u00b7 GAMES", font=f(FONTB, 11), fill=RED)
    d.text((M + 18, gy + 19),
           "GTA VI TAKES $3.79 BILLION IN ONE DAY \u2014 BIGGEST ENTERTAINMENT LAUNCH IN HISTORY",
           font=f(FONTB, 15), fill=INK)
    gta_note = "32.5M pre-sold \u00b7 Metacritic 99 \u00b7 announced Friday"
    nw = d.textlength(gta_note, font=f(FONT, 11))
    d.text((X1 - nw - 12, gy + 5), gta_note, font=f(FONT, 11), fill=GREY)

    # ---- Markets strip ----
    sy = gy + 46
    d.rectangle([M, sy, X1, sy + 50], fill=INK)
    d.text((M + 14, sy + 6), "MARKETS \u2014 FRIDAY\u2019S CLOSE", font=f(FONTB, 12),
           fill=(255, 255, 255))
    sx, sw = M + 14, 187
    for i, (name, val) in enumerate(MARKETS):
        x = sx + (i % 5) * sw
        yy = sy + 22 + (i // 5) * 15
        d.text((x, yy), name, font=f(FONTB, 10), fill=(170, 165, 155))
        vw = d.textlength(val, font=f(FONTB, 11))
        d.text((x + 172 - vw, yy - 1), val, font=f(FONTB, 11), fill=(255, 120, 100))

    # ---- UTC timeline ----
    ty = sy + 58
    d.text((M, ty), "THE DAY IN UTC", font=f(FONTB, 14), fill=INK)
    line_y = ty + 38
    d.line([M + 8, line_y, X1 - 8, line_y], fill=GREY, width=2)
    n = len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        px = M + 8 + i * (CW - 16) // (n - 1)
        d.ellipse([px - 4, line_y - 4, px + 4, line_y + 4], fill=RED)
        tw = d.textlength(t, font=f(FONTB, 13))
        tx = min(max(px - tw / 2, M), X1 - tw)
        d.text((tx, line_y - 22), t, font=f(FONTB, 13), fill=INK)
        ly = line_y + 8
        for j, part in enumerate(label.split("\n")):
            lw = d.textlength(part, font=f(FONT, 11))
            lx = min(max(px - lw / 2, M), X1 - lw)
            d.text((lx, ly + j * 13), part, font=f(FONT, 11), fill=GREY)

    # ---- The day in full ----
    gy2 = ty + 68
    d.rectangle([M, gy2, X1, gy2 + 2], fill=INK)
    d.text((M, gy2 + 7), "THE DAY IN FULL \u2014 30 MORE STORIES, BY REGION",
           font=f(FONTB, 15), fill=INK)
    grid_y = gy2 + 28
    col_w3 = (CW - 2 * 24) // 3  # 301
    avail = 998 - grid_y
    chosen = None
    for size, lh in ((12.5, 15.5), (12, 15), (11.5, 14.5), (11, 14), (10.5, 13.5)):
        bf = f(FONT, size)
        tallest = max(column_height(d, col, col_w3, bf, lh)
                      for col in grid_columns())
        if tallest <= avail:
            chosen = (bf, lh)
            break
    if chosen is None:
        raise SystemExit("grid does not fit at any size")
    draw_grid(d, M, grid_y, col_w3, chosen[0], chosen[1])

    # ---- Footer ----
    d.text((M, 1004),
           "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 IMD \u00b7 Al Jazeera \u00b7 RNZ \u00b7 The Hindu \u00b7 IMF \u00b7 UKMTO",
           font=f(FONT, 10), fill=GREY)
    note = "One image \u00b7 one day \u00b7 drawn by program"
    nw = d.textlength(note, font=f(FONT, 10))
    d.text((X1 - nw, 1004), note, font=f(FONT, 10), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()

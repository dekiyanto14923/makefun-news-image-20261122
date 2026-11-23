#!/usr/bin/env python3
"""Render the news-image entry: a one-page newspaper front page summing up
Sunday 22 November 2026, drawn with Pillow. Output: entry.png, 1024x1024.

Run: python3 generate.py   (writes entry.png next to this file)
The stories below were researched from Reuters / AP / AFP / Al Jazeera /
One Turn round-ups of 22 November 2026 on 2026-11-23.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (26, 26, 26)
RED = (179, 39, 30)
NAVY = (22, 40, 63)
NAVY_LIGHT = (38, 62, 94)
GOLD = (201, 162, 39)
GREY = (90, 86, 76)
TILE_BG = (255, 255, 255)
TILE_BORDER = (216, 210, 196)
MUTED_BLUE = (220, 228, 238)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_icon(d, kind, x, y, s, color):
    """Draw a small pictogram of side s at (x, y) in the given color."""
    if kind == "rocket":  # Gulf: missile strike
        d.polygon([(x + s * 0.50, y + s * 0.05), (x + s * 0.68, y + s * 0.45),
                   (x + s * 0.50, y + s * 0.62), (x + s * 0.32, y + s * 0.45)],
                  fill=color)
        d.polygon([(x + s * 0.32, y + s * 0.45), (x + s * 0.14, y + s * 0.78),
                   (x + s * 0.38, y + s * 0.62)], fill=color)
        d.polygon([(x + s * 0.68, y + s * 0.45), (x + s * 0.86, y + s * 0.78),
                   (x + s * 0.62, y + s * 0.62)], fill=color)
        d.polygon([(x + s * 0.42, y + s * 0.66), (x + s * 0.58, y + s * 0.66),
                   (x + s * 0.50, y + s * 0.95)], fill=(232, 120, 40))
    elif kind == "burst":  # Ukraine: drone strike
        cx, cy = x + s / 2, y + s / 2
        for k in range(8):
            import math
            a = math.pi * k / 4
            a2 = a + math.pi / 8
            d.polygon([(cx + 0.10 * s * math.cos(a), cy + 0.10 * s * math.sin(a)),
                       (cx + 0.48 * s * math.cos(a2), cy + 0.48 * s * math.sin(a2)),
                       (cx + 0.10 * s * math.cos(a + math.pi / 4),
                        cy + 0.10 * s * math.sin(a + math.pi / 4))], fill=color)
        d.ellipse([cx - 0.13 * s, cy - 0.13 * s, cx + 0.13 * s, cy + 0.13 * s],
                  fill=(255, 255, 255))
    elif kind == "cuffs":  # Mexico: capture
        r = s * 0.20
        d.ellipse([x + s * 0.06, y + s * 0.30, x + s * 0.06 + 2 * r, y + s * 0.30 + 2 * r],
                  outline=color, width=max(3, s // 12))
        d.ellipse([x + s * 0.54, y + s * 0.30, x + s * 0.54 + 2 * r, y + s * 0.30 + 2 * r],
                  outline=color, width=max(3, s // 12))
        d.line([x + s * 0.26, y + s * 0.50, x + s * 0.74, y + s * 0.50],
               fill=color, width=max(3, s // 12))
        d.ellipse([x + s * 0.44, y + s * 0.42, x + s * 0.56, y + s * 0.58], fill=color)
    elif kind == "triad":  # Diplomacy: three-way summit
        r = s * 0.17
        pts = [(x + s * 0.50, y + s * 0.16), (x + s * 0.18, y + s * 0.72),
               (x + s * 0.82, y + s * 0.72)]
        d.line([pts[0], pts[1]], fill=color, width=max(3, s // 14))
        d.line([pts[1], pts[2]], fill=color, width=max(3, s // 14))
        d.line([pts[2], pts[0]], fill=color, width=max(3, s // 14))
        for (cx, cy) in pts:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    elif kind == "chart":  # Markets: falling chart
        d.line([x + s * 0.10, y + s * 0.88, x + s * 0.10, y + s * 0.12],
               fill=color, width=max(3, s // 14))
        d.line([x + s * 0.10, y + s * 0.88, x + s * 0.92, y + s * 0.88],
               fill=color, width=max(3, s // 14))
        d.line([(x + s * 0.16, y + s * 0.30), (x + s * 0.38, y + s * 0.48),
                (x + s * 0.55, y + s * 0.40), (x + s * 0.86, y + s * 0.78)],
               fill=(179, 39, 30), width=max(4, s // 10))
        d.polygon([(x + s * 0.86, y + s * 0.78), (x + s * 0.70, y + s * 0.76),
                   (x + s * 0.84, y + s * 0.62)], fill=(179, 39, 30))
    elif kind == "scales":  # Trade: balance
        d.line([x + s * 0.50, y + s * 0.12, x + s * 0.50, y + s * 0.82],
               fill=color, width=max(3, s // 14))
        d.line([x + s * 0.16, y + s * 0.30, x + s * 0.84, y + s * 0.30],
               fill=color, width=max(3, s // 14))
        d.line([x + s * 0.16, y + s * 0.30, x + s * 0.16, y + s * 0.58],
               fill=color, width=max(2, s // 18))
        d.line([x + s * 0.84, y + s * 0.30, x + s * 0.84, y + s * 0.58],
               fill=color, width=max(2, s // 18))
        d.polygon([(x + s * 0.04, y + s * 0.58), (x + s * 0.28, y + s * 0.58),
                   (x + s * 0.16, y + s * 0.76)], fill=color)
        d.polygon([(x + s * 0.72, y + s * 0.58), (x + s * 0.96, y + s * 0.58),
                   (x + s * 0.84, y + s * 0.76)], fill=color)
        d.line([x + s * 0.34, y + s * 0.88, x + s * 0.66, y + s * 0.88],
               fill=color, width=max(3, s // 14))
    elif kind == "flame":  # Indonesia: fire
        d.polygon([(x + s * 0.50, y + s * 0.04), (x + s * 0.72, y + s * 0.34),
                   (x + s * 0.86, y + s * 0.60), (x + s * 0.74, y + s * 0.86),
                   (x + s * 0.26, y + s * 0.86), (x + s * 0.14, y + s * 0.60),
                   (x + s * 0.30, y + s * 0.34)], fill=color)
        d.polygon([(x + s * 0.50, y + s * 0.42), (x + s * 0.64, y + s * 0.60),
                   (x + s * 0.60, y + s * 0.80), (x + s * 0.40, y + s * 0.80),
                   (x + s * 0.36, y + s * 0.60)], fill=(255, 214, 90))
    elif kind == "planet":  # Space: Mercury orbit
        cx, cy, r = x + s * 0.50, y + s * 0.52, s * 0.26
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
        d.ellipse([x + s * 0.02, y + s * 0.34, x + s * 0.98, y + s * 0.66],
                  outline=(201, 162, 39), width=max(3, s // 12))
        d.ellipse([x + s * 0.72, y + s * 0.10, x + s * 0.84, y + s * 0.22],
                  fill=(201, 162, 39))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- Masthead ----------
    d.text((W // 2, 4), "THE WORLD", font=font(SERIF_B, 92), fill=INK, anchor="ma")
    d.line([28, 104, W - 28, 104], fill=INK, width=3)
    d.line([28, 110, W - 28, 110], fill=INK, width=1)
    d.text((W // 2, 118), "SUNDAY 22 NOVEMBER 2026",
           font=font(SANS_B, 34), fill=RED, anchor="ma")
    d.text((W // 2, 156), "THE DAY'S NEWS, IN ONE IMAGE",
           font=font(SANS_B, 17), fill=GREY, anchor="ma")

    # ---------- Hero: COP31 ----------
    hx0, hy0, hx1, hy1 = 28, 178, W - 28, 430
    d.rounded_rectangle([hx0, hy0, hx1, hy1], radius=10, fill=NAVY)
    # globe pictogram, right side
    gx, gy, gr = 838, 304, 82
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=GOLD, width=5)
    d.ellipse([gx - gr * 0.55, gy - gr, gx + gr * 0.55, gy + gr],
              outline=GOLD, width=3)
    d.line([gx - gr, gy, gx + gr, gy], fill=GOLD, width=3)
    d.arc([gx - gr, gy - gr * 0.55, gx + gr, gy + gr * 0.55], 200, 340,
          fill=GOLD, width=3)
    # crack through the globe
    d.line([(gx - 30, gy - 78), (gx - 8, gy - 30), (gx - 34, gy + 6),
            (gx + 2, gy + 52), (gx - 12, gy + 80)], fill=RED, width=6)
    d.text((hx0 + 26, hy0 + 18), "CLIMATE  ·  ANTALYA, TURKEY",
           font=font(SANS_B, 19), fill=GOLD)
    d.text((hx0 + 26, hy0 + 48), "CLIMATE TALKS",
           font=font(SERIF_B, 62), fill=(255, 255, 255))
    d.text((hx0 + 26, hy0 + 112), "COLLAPSE",
           font=font(SERIF_B, 62), fill=(255, 255, 255))
    d.text((hx0 + 26, hy0 + 186),
           "COP31 ends with no deal — the EU rejects a final draft",
           font=font(SANS, 23), fill=(225, 230, 238))
    d.text((hx0 + 26, hy0 + 216),
           "that never mentions fossil fuels, two days past deadline.",
           font=font(SANS, 23), fill=(225, 230, 238))

    # ---------- Story tiles ----------
    stories = [
        ("GULF", (179, 39, 30), "rocket",
         "Iran strikes US bases in Bahrain",
         "Missiles and drones hit an industrial site; two people hurt. "
         "Tehran claims two Patriot radars destroyed."),
        ("UKRAINE", (29, 78, 137), "burst",
         "Russian drone hits Kyiv flats; 14 missing",
         "A five-storey block in Dymer is struck; a missile kills two in "
         "Kryvyi Rih, Zelenskyy's home city."),
        ("MEXICO", (15, 118, 110), "cuffs",
         "\u2018El Chapo Isidro\u2019 captured in Sinaloa",
         "Special forces seize cartel boss Fausto Isidro Meza Flores; "
         "11 killed in the raid, including four soldiers."),
        ("DIPLOMACY", (109, 40, 217), "triad",
         "Trump, Xi and Putin meet in Shenzhen",
         "First-ever trilateral summit ends with a joint declaration on "
         "nuclear risks — but no Ukraine breakthrough."),
        ("MARKETS", (194, 65, 12), "chart",
         "Stocks slide into correction",
         "S&P 500 falls 3.7% and Nasdaq 5.3% on Friday as the AI sell-off "
         "spreads to Japan and Korea."),
        ("TRADE", (21, 128, 61), "scales",
         "EU and Indonesia sign landmark deal",
         "After almost 10 years of talks, tariffs scrapped on up to "
         "98.5% of goods."),
        ("INDONESIA", (146, 64, 14), "flame",
         "Factory fire kills 3; 36 missing",
         "Blaze rips through a candy factory in Cikande, Banten, as a "
         "7.2-magnitude quake shakes the country."),
        ("SPACE", (71, 85, 105), "planet",
         "BepiColombo reaches Mercury",
         "After eight years and six billion miles, the ESA\u2013JAXA probe "
         "slips into orbit around Mercury."),
    ]
    tx0, ty0 = 28, 442
    tw, th, gap = 478, 116, 10
    for i, (kicker, color, icon, head, body) in enumerate(stories):
        col, row = i % 2, i // 2
        x0 = tx0 + col * (tw + gap)
        y0 = ty0 + row * (th + gap)
        x1, y1 = x0 + tw, y0 + th
        d.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=TILE_BG,
                            outline=TILE_BORDER, width=1)
        d.rectangle([x0, y0 + 6, x0 + 6, y1 - 6], fill=color)
        d.text((x0 + 18, y0 + 8), kicker, font=font(SANS_B, 15), fill=color)
        draw_icon(d, icon, x1 - 52, y0 + 7, 38, color)
        head_lines = wrap(d, head, font(SERIF_B, 21), tw - 36)[:2]
        hy = y0 + 28
        for line in head_lines:
            d.text((x0 + 18, hy), line, font=font(SERIF_B, 21), fill=INK)
            hy += 24
        body_lines = wrap(d, body, font(SANS, 15), tw - 36)[:2]
        by = y0 + 28 + 24 * len(head_lines) + 3
        for line in body_lines:
            d.text((x0 + 18, by), line, font=font(SANS, 15), fill=(64, 60, 52))
            by += 18

    # ---------- Also strip ----------
    ay = 442 + 4 * 116 + 3 * 10 + 8  # 944
    d.line([28, ay, W - 28, ay], fill=INK, width=2)
    also = ("ALSO:  FBI crime database reportedly hacked  ·  Settlers torch "
            "vehicles in West Bank villages  ·  S. Korea\u2019s education "
            "minister quits over AI cheating  ·  Boat capsizes in Nigeria, "
            "24 dead")
    also_lines = wrap(d, also, font(SANS_B, 15), W - 56)
    yy = ay + 8
    for line in also_lines:
        d.text((28, yy), line, font=font(SANS_B, 15), fill=INK)
        yy += 20
    d.text((W // 2, yy + 4),
           "Sources: Reuters · AP · AFP · Al Jazeera · One Turn — Sunday 22 November 2026",
           font=font(SANS, 12), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()

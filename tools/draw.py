#!/usr/bin/env python3
"""Draw the Broadsheet front page for Saturday 21 November 2026.

A single 1024x1024 PNG summing up the day's world news, drawn with PIL
from scratch: masthead, dateline, lead story with illustration, two
second-row stories, three third-row stories and an "also today" strip.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (17, 17, 17)
INK_SOFT = (58, 58, 58)
RED = (176, 42, 32)
RED_DARK = (140, 28, 22)
NAVY = (28, 44, 66)
GOLD = (198, 148, 52)
RULE = (120, 110, 95)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def centered(draw, text, fnt, cx, y, fill=INK, tracking=0):
    if tracking:
        # draw letter by letter with extra spacing
        widths = [draw.textlength(ch, font=fnt) for ch in text]
        total = sum(widths) + tracking * (len(text) - 1)
        x = cx - total / 2
        for ch, w in zip(text, widths):
            draw.text((x, y), ch, font=fnt, fill=fill)
            x += w + tracking
        return total
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w


def kicker(draw, text, x, y, color=RED):
    f = font(SANS_B, 17)
    draw.text((x, y), text, font=f, fill=color)
    return f


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- lead art
def lead_art(draw, box):
    """Night sky over south-east Poland: missile trails, blasts, map inset."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # night sky
    draw.rectangle(box, fill=(24, 36, 54))
    # stars
    import random
    rnd = random.Random(7)
    for _ in range(46):
        sx = x0 + rnd.randint(6, w - 6)
        sy = y0 + rnd.randint(6, int(h * 0.55))
        r = rnd.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(200, 205, 215))
    # distant tree line / ground
    gy = y0 + int(h * 0.82)
    draw.rectangle([x0, gy, x1, y1], fill=(16, 24, 20))
    # trees
    for tx in range(x0 + 14, x1 - 10, 26):
        th = rnd.randint(14, 30)
        draw.polygon([(tx, gy), (tx + 9, gy - th), (tx + 18, gy)], fill=(10, 18, 14))
    # missile trails arcing down to the ground
    def trail(sx, sy, ex, ey, color=(255, 176, 66)):
        steps = 26
        pts = []
        for i in range(steps + 1):
            t = i / steps
            px = sx + (ex - sx) * t
            py = sy + (ey - sy) * t - math.sin(t * math.pi) * 26
            pts.append((px, py))
        draw.line(pts, fill=color, width=3)
        # fireball at the end
        for rr, col in [(16, (255, 120, 40)), (10, (255, 190, 80)), (5, (255, 240, 170))]:
            draw.ellipse([ex - rr, ey - rr, ex + rr, ey + rr], fill=col)
    trail(x0 + int(w * 0.16), y0 + 8, x0 + int(w * 0.30), gy - 6)
    trail(x0 + int(w * 0.52), y0 + 4, x0 + int(w * 0.62), gy - 2)
    trail(x0 + int(w * 0.86), y0 + 10, x0 + int(w * 0.78), gy - 8)
    # blast glow on the horizon
    for cx, cy in [(x0 + int(w * 0.30), gy - 6), (x0 + int(w * 0.62), gy - 2)]:
        for rr, col in [(46, (255, 120, 40, 90)), (30, (255, 170, 60, 140))]:
            draw.ellipse([cx - rr, cy - rr // 2, cx + rr, cy + rr // 2], fill=col)
    # location pin + label
    px, py = x0 + int(w * 0.62), gy - 58
    draw.ellipse([px - 13, py - 13, px + 13, py + 13], fill=RED)
    draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(255, 255, 255))
    draw.polygon([(px - 9, py + 8), (px + 9, py + 8), (px, py + 24)], fill=RED)
    lab = "NOWY LIPOWIEC, POLAND"
    lf = font(SANS_B, 17)
    lw = draw.textlength(lab, font=lf)
    draw.rectangle([x0 + w - lw - 34, y0 + 12, x0 + w - 14, y0 + 40], fill=(246, 241, 231))
    draw.text((x0 + w - lw - 24, y0 + 16), lab, font=lf, fill=RED_DARK)
    # caption strip at bottom of the art
    cap = "A Kh-101 cruise missile came down about 50 km from the Ukrainian border."
    cf = font(SERIF_I, 17)
    draw.rectangle([x0, y1 - 30, x1, y1], fill=(10, 14, 18))
    draw.text((x0 + 12, y1 - 26), cap, font=cf, fill=(225, 225, 210))


def chart_art(draw, box):
    """Plunging red market chart on a white panel."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=(255, 255, 255), outline=(150, 140, 125), width=1)
    # grid
    for i in range(1, 4):
        gy = y0 + h * i / 4
        draw.line([(x0 + 8, gy), (x1 - 8, gy)], fill=(225, 220, 205), width=1)
    pts = []
    n = 24
    for i in range(n + 1):
        t = i / n
        px = x0 + 12 + (w - 24) * t
        # jagged decline, steeper at the end
        py = y0 + 30 + (h - 58) * (t ** 1.25) + math.sin(i * 1.7) * 4 * (1 - t * 0.5)
        pts.append((px, py))
    draw.line(pts, fill=RED, width=4)
    # end dot + label
    ex, ey = pts[-1]
    draw.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=RED_DARK)
    bf = font(SANS_B, 26)
    draw.rectangle([x0 + 10, y0 + 6, x0 + 216, y0 + 36], fill=(255, 255, 255))
    draw.text((x0 + 14, y0 + 8), "S&P 500  -3.7%", font=bf, fill=RED_DARK)
    sf = font(SANS_B, 15)
    draw.text((x0 + 14, y1 - 24), "NASDAQ  -5.3%   •   DOW  -950 pts", font=sf, fill=INK_SOFT)


def globe_art(draw, box):
    """Globe with sun and clock: climate talks running into overtime."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=(232, 240, 244), outline=(150, 140, 125), width=1)
    cx, cy = x0 + int(w * 0.30), y0 + int(h * 0.46)
    r = int(h * 0.27)
    # sun
    sx, sy = x0 + int(w * 0.80), y0 + int(h * 0.26)
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        draw.line([(sx + math.cos(a) * 20, sy + math.sin(a) * 20),
                   (sx + math.cos(a) * 30, sy + math.sin(a) * 30)], fill=GOLD, width=3)
    draw.ellipse([sx - 16, sy - 16, sx + 16, sy + 16], fill=GOLD)
    # globe
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 110, 150))
    for k in range(1, 3):
        off = int(r * 0.45 * k)
        draw.ellipse([cx - r, cy - r + off, cx + r, cy + r - off],
                     outline=(140, 190, 220), width=1)
    draw.ellipse([cx - r, cy - 4, cx + r, cy + 4], outline=(140, 190, 220), width=1)
    # land blobs
    draw.ellipse([cx - r + 6, cy - r + 8, cx - 4, cy - 6], fill=(96, 150, 84))
    draw.ellipse([cx + 2, cy + 2, cx + r - 8, cy + r - 6], fill=(96, 150, 84))
    draw.ellipse([cx - r + 16, cy + 10, cx - r + 32, cy + 24], fill=(96, 150, 84))
    sf = font(SANS_B, 15)
    draw.text((x0 + 14, y1 - 24), "TALKS IN OVERTIME", font=sf, fill=INK_SOFT)


def icon_strip(draw, box, kind):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(238, 232, 218), outline=(150, 140, 125), width=1)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "riemann":
        f = font(SERIF_B, 34)
        draw.text((cx - 52, cy - 20), "ζ(s) = 0", font=f, fill=NAVY)
    elif kind == "summit":
        # three small flags: US, China, Russia
        fw, fh = 34, 22
        flags = [("us", x0 + 26), ("cn", cx - fw // 2), ("ru", x1 - 26 - fw)]
        for name, fx in flags:
            fy = cy - fh // 2
            if name == "us":
                draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(178, 34, 52))
                for i in range(4):
                    draw.rectangle([fx, fy + i * 6, fx + fw, fy + i * 6 + 3], fill=(255, 255, 255))
                draw.rectangle([fx, fy, fx + 14, fy + 12], fill=(28, 44, 96))
            elif name == "cn":
                draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
                draw.ellipse([fx + 6, fy + 5, fx + 13, fy + 12], fill=(255, 222, 0))
            else:
                draw.rectangle([fx, fy, fx + fw, fy + 8], fill=(255, 255, 255))
                draw.rectangle([fx, fy + 8, fx + fw, fy + 15], fill=(0, 57, 166))
                draw.rectangle([fx, fy + 15, fx + fw, fy + fh], fill=(213, 0, 50))
    elif kind == "drone":
        # drone silhouette over waves
        draw.ellipse([cx - 34, cy - 8, cx + 34, cy + 8], fill=INK)
        draw.rectangle([cx - 4, cy - 14, cx + 4, cy + 14], fill=INK)
        for dx in (-40, 40):
            draw.ellipse([cx + dx - 12, cy - 16, cx + dx + 12, cy - 8], fill=INK_SOFT)
            draw.line([(cx + dx, cy - 12), (cx + dx - 26, cy - 12)], fill=INK_SOFT, width=2)
            draw.line([(cx + dx, cy - 12), (cx + dx + 26, cy - 12)], fill=INK_SOFT, width=2)
        for i, wy in enumerate([y1 - 12, y1 - 6]):
            draw.arc([x0 + 10, wy - 8, x1 - 10, wy + 8], 0, 180, fill=(58, 110, 150), width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 30  # margin
    X1 = W - M

    # outer frame
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    d.rectangle([16, 16, W - 17, H - 17], outline=RULE, width=1)

    # ---- masthead
    mast = font(SERIF_B, 84)
    centered(d, "BROADSHEET", mast, W // 2, 22, fill=INK, tracking=6)
    # thin rules under masthead
    rule(d, M, 120, X1, 3)
    rule(d, M, 126, X1, 1)

    # ---- dateline
    date_f = font(SERIF_B, 36)
    centered(d, "SATURDAY 21 NOVEMBER 2026", date_f, W // 2, 134, fill=RED_DARK)
    sub_f = font(SANS_B, 15)
    centered(d, "THE WORLD IN ONE DAY  •  ONE PAGE, EVERY STORY THAT MATTERED", sub_f,
             W // 2, 176, fill=INK_SOFT, tracking=1)
    rule(d, M, 200, X1, 3)
    rule(d, M, 206, X1, 1)

    # ---- lead story
    y = 220
    kicker(d, "WAR IN UKRAINE SPILLS OVER THE BORDER", M, y)
    y += 24
    head_f = font(SERIF_B, 46)
    lines = wrap(d, "RUSSIAN MISSILES LAND IN POLAND", head_f, X1 - M)
    for ln in lines:
        d.text((M, y), ln, font=head_f, fill=INK)
        y += 52
    y += 4
    lead_art(d, (M, y, X1, y + 130))
    y += 130 + 10
    deck_f = font(SERIF, 20)
    y = draw_wrapped(d,
        "Two Russian cruise missiles and a suspected drone came down in south-east Poland "
        "during a huge overnight barrage on Ukraine. Prime Minister Donald Tusk calls it an "
        "intentional provocation. NATO chief Mark Rutte flies to Warsaw: \u201cAll allies stand "
        "in full solidarity.\u201d",
        deck_f, M, y, X1 - M, leading=25)
    y += 8
    rule(d, M, y, X1, 2)
    y += 12

    # ---- row 2: markets + climate
    row2_y = y
    col_w = (X1 - M - 24) // 2
    col2_x = M + col_w + 24
    # left: markets
    kicker(d, "MARKETS", M, row2_y)
    h2 = font(SERIF_B, 26)
    yy = row2_y + 24
    for ln in wrap(d, "WALL STREET IN CORRECTION", h2, col_w):
        d.text((M, yy), ln, font=h2, fill=INK)
        yy += 30
    chart_art(d, (M, yy + 4, M + col_w, yy + 4 + 96))
    yy += 104
    draw_wrapped(d,
        "The S&P 500 falls 3.7% and the Nasdaq 5.3% as the AI sell-off deepens. "
        "Nvidia tumbles 14% as US regulators probe its accounts; Bitcoin drops below $60,000.",
        font(SERIF, 17), M, yy, col_w, leading=20)
    # divider between columns
    d.line([(col2_x - 12, row2_y), (col2_x - 12, row2_y + 224)], fill=RULE, width=1)
    # right: climate
    kicker(d, "CLIMATE", col2_x, row2_y)
    yy = row2_y + 24
    for ln in wrap(d, "COP31 DEADLOCKED IN ANTALYA", h2, col_w):
        d.text((col2_x, yy), ln, font=h2, fill=INK)
        yy += 30
    globe_art(d, (col2_x, yy + 4, col2_x + col_w, yy + 4 + 96))
    yy += 104
    draw_wrapped(d,
        "Climate talks run into overtime as the draft deal drops all mention of fossil fuels "
        "and a $120bn fund for poorer nations. The EU warns of a \u201cfossil summit\u201d.",
        font(SERIF, 17), col2_x, yy, col_w, leading=20)

    y = row2_y + 224
    rule(d, M, y, X1, 2)
    y += 12

    # ---- row 3: three small stories
    row3_y = y
    col3_w = (X1 - M - 48) // 3
    stories = [
        ("SCIENCE", "A PROOF FOR RIEMANN?",
         "An Anthropic researcher says the firm\u2019s Claude AI has proved maths\u2019 greatest "
         "riddle, unsolved for over 160 years. Experts urge caution.",
         "riemann"),
        ("DIPLOMACY", "SUMMIT IN SHENZHEN",
         "Trump, Xi and Putin meet on the APEC sidelines. Zelenskyy calls it \u201cvery "
         "unsuccessful\u201d for Russia; Trump tells Europe to stop funding Ukraine.",
         "summit"),
        ("MIDDLE EAST", "IRAN SAYS IT DOWNED US DRONE",
         "Tehran claims it shot down an American MQ-9 drone over the Strait of Hormuz as "
         "US\u2013Iran nuclear talks stall.",
         "drone"),
    ]
    h3 = font(SERIF_B, 22)
    for i, (kick, head, deck, kind) in enumerate(stories):
        cx = M + i * (col3_w + 24)
        kicker(d, kick, cx, row3_y)
        yy = row3_y + 22
        for ln in wrap(d, head, h3, col3_w):
            d.text((cx, yy), ln, font=h3, fill=INK)
            yy += 26
        icon_strip(d, (cx, yy + 2, cx + col3_w, yy + 2 + 40), kind)
        yy += 48
        draw_wrapped(d, deck, font(SERIF, 16), cx, yy, col3_w, leading=20)
        if i < 2:
            d.line([(cx + col3_w + 12, row3_y), (cx + col3_w + 12, row3_y + 168)],
                   fill=RULE, width=1)

    y = row3_y + 176
    rule(d, M, y, X1, 2)
    y += 10

    # ---- also today strip (single line, doubles as footer)
    also_f = font(SANS_B, 15)
    d.text((M, y), "ALSO TODAY:", font=also_f, fill=RED)
    ax = M + d.textlength("ALSO TODAY:  ", font=also_f)
    d.text((ax, y + 1),
        "Princess Catherine speaks of her cancer journey  •  EU plans a Big Tech tax  •  "
        "GTA VI launch beats expectations",
        font=font(SERIF, 16), fill=INK)
    print("layout bottom y:", y + 22, "of", H)

    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()

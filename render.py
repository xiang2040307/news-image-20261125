#!/usr/bin/env python3
"""Render the news-image-20261125 entry: one 1024x1024 infographic summing up
Wednesday 25 November 2026's world news. Pure PIL, deterministic output.

Stories verified 25 Nov 2026 (Beijing evening) against Just Security Early
Edition 25 Nov 2026, SCMP world headlines and AP/Reuters wires:
- Hormuz: IRGC says two oil tankers struck naval mines and caught fire.
- Gaza: Israeli strike kills Hamas security chief Mohammad Abuelouf, his wife
  and two children, per Gaza medics / Hamas-run interior ministry.
- Ukraine: Russian strikes kill two in Odesa region, hit Kyiv; Ukrainian
  drones set two Rosneft refineries (Syzran, Kuibyshev) ablaze.
- Markets: KOSPI -6.2%, Nikkei -2.8%; Dow closes above 50,000 first time.
- Huawei: Brooklyn jury convicts on 10 of 12 counts (bank fraud, wire fraud,
  sanctions violations, trade-secret theft conspiracy).
- Sudan: RSF drone strikes kill 19 civilians, wound 20 in two cities.
Also: Houthi drone hits Riyadh tower (11 injured); Australia-Solomon Islands
treaty signed; Colombia supermarket hostages freed; Shenzhou-24 docks.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (12, 27, 46)
GOLD = (212, 175, 105)
PAPER = (251, 249, 244)
INK = (18, 30, 44)
GREY = (74, 88, 102)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_KICKER = font("LiberationSans-Bold.ttf", 25)
F_TITLE = font("LiberationSans-Bold.ttf", 62)
F_TAG = font("LiberationSans-Bold.ttf", 19)
F_HEAD = font("LiberationSans-Bold.ttf", 30)
F_BODY = font("LiberationSans-Regular.ttf", 21)
F_FOOT = font("LiberationSans-Regular.ttf", 19)
F_FOOT_B = font("LiberationSans-Bold.ttf", 19)

STORIES = [
    ("HORMUZ", (192, 57, 43),
     "Two tankers hit by mines in the Strait of Hormuz",
     "Iran's Revolutionary Guard says two oil tankers struck naval mines, "
     "exploded and caught fire in the world's key oil chokepoint."),
    ("GAZA", (108, 52, 131),
     "Israeli strike kills Hamas security chief",
     "Mohammad Abuelouf, his wife and two children are killed in Gaza City, "
     "medics and Hamas officials say."),
    ("UKRAINE", (31, 97, 141),
     "Strikes hit Odesa and Kyiv; refineries burn in Russia",
     "Russian attacks kill two in Odesa region; Ukrainian drones set two "
     "Rosneft refineries ablaze in Samara."),
    ("MARKETS", (185, 119, 14),
     "Asian stocks plunge; Dow tops 50,000",
     "South Korea's KOSPI falls 6.2% and Japan's Nikkei 2.8%; the Dow closes "
     "above 50,000 for the first time."),
    ("TECH", (14, 124, 123),
     "Huawei convicted in US fraud trial",
     "A New York jury finds the Chinese tech giant guilty on 10 of 12 counts, "
     "including bank fraud and trade-secret theft."),
    ("SUDAN", (30, 132, 73),
     "Drone strikes kill 19 civilians in Sudan",
     "Paramilitary RSF drones hit two cities, killing 19 and wounding 20, "
     "Sudanese lawyers say."),
]

ALSO = ("Also today:  Houthi drone hits a Riyadh tower, injuring 11  •  "
        "Australia and Solomon Islands sign a treaty barring foreign "
        "military bases  •  Colombia police free supermarket hostages  •  "
        "China's Shenzhou-24 docks with Tiangong")


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
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


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # Header (title auto-fitted to the full width)
    d.text((28, 26), "THE WORLD IN ONE IMAGE", font=F_KICKER, fill=GOLD)
    title = "WEDNESDAY 25 NOVEMBER 2026"
    tsize = 62
    while True:
        tf = font("LiberationSans-Bold.ttf", tsize)
        if d.textlength(title, font=tf) <= 968 or tsize <= 40:
            break
        tsize -= 2
    d.text((28, 58), title, font=tf, fill=WHITE)
    d.line([(28, 148), (996, 148)], fill=GOLD, width=3)

    # Story cards: 2 columns x 3 rows
    x0, y0, cw, ch, gap = 28, 170, 476, 224, 16
    for i, (tag, color, head, body) in enumerate(STORIES):
        x = x0 + (i % 2) * (cw + gap)
        y = y0 + (i // 2) * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=14, fill=PAPER)
        d.rounded_rectangle([x, y, x + cw, y + 8], radius=4, fill=color)
        # tag chip
        tw = d.textlength(tag, font=F_TAG) + 20
        d.rounded_rectangle([x + 16, y + 22, x + 16 + tw, y + 50],
                            radius=6, fill=color)
        d.text((x + 26, y + 26), tag, font=F_TAG, fill=WHITE)
        # headline (max 2 lines)
        lines = wrap(d, head, F_HEAD, cw - 32)[:2]
        yy = y + 62
        for ln in lines:
            d.text((x + 16, yy), ln, font=F_HEAD, fill=INK)
            yy += 36
        # body (max 3 lines)
        blines = wrap(d, body, F_BODY, cw - 32)[:3]
        yy = y + 62 + 2 * 36 + 8
        for ln in blines:
            d.text((x + 16, yy), ln, font=F_BODY, fill=GREY)
            yy += 27

    # Footer
    fy = 170 + 3 * ch + 2 * gap + 14  # 892
    d.line([(28, fy), (996, fy)], fill=(58, 79, 102), width=2)
    flines = wrap(d, ALSO, F_FOOT, 968)[:2]
    yy = fy + 12
    for ln in flines:
        d.text((28, yy), ln, font=F_FOOT, fill=(205, 214, 224))
        yy += 26
    d.text((28, fy + 72), "Events of 25 November 2026  ·  Sources: AP, Reuters, "
           "Just Security, SCMP", font=F_FOOT_B, fill=GOLD)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

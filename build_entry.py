#!/usr/bin/env python3
"""news-image-20261121-cand-b — "SATURDAY GAZETTE".

A cream broadsheet front page summing up Saturday 21 November 2026 in
35 stories, all first reported that day. Masthead + giant date + italic
headline strip + 7-number strip + region bar + date-check strip near the
top + 3 big illustrated leads + 9 small cards + 23 one-liners.

Every headline and number is exact programmatic text; all illustrations
are flat vector-style drawings made with PIL shapes (no photos).
Deterministic: no network, no randomness, no timestamps in the image.
Paths resolve from this script's own directory; output defaults to
/output (or MAKEFUN_OUTPUT_DIR / argv[1]).
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W = 1600
MARGIN = 60
COLW = (W - 2 * MARGIN - 2 * 26) // 3  # 3 columns, 26px gutters

CREAM = (250, 244, 230)
PAPER = (253, 248, 238)
INK = (22, 28, 38)
NAVY = (20, 36, 61)
RED = (158, 32, 32)
GOLD = (176, 132, 52)
RULE = (120, 110, 95)
MUTED = (90, 84, 72)
TEAL = (24, 96, 96)
SKY = (168, 205, 225)
SAGE = (139, 168, 118)


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


def draw_centered(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 6


# ---------------------------------------------------------------- stories
# (region, place, headline, deck, source)
LEADS = [
    ("Global", "Antalya, Türkiye",
     "COP31 runs into overtime with no deal yet",
     "Talks run past their deadline as negotiators haggle over finance "
     "and fossil fuels into the night, with no agreement in sight.",
     "Guardian / AP"),
    ("Europe", "Kryvyi Rih, Ukraine",
     "Russian strikes kill 12 and wound 82",
     "The latest blow in a week of attacks on Ukrainian cities and "
     "power, as rescuers pull survivors from the wreckage.",
     "AP"),
    ("Americas", "Washington, US",
     "US clears 900,000 AI chips for China",
     "Washington approves licences for advanced chips bound for China, "
     "redrawing the year's fiercest technology fight.",
     "Reports"),
]

CARDS = [
    ("Middle East", "Sana'a, Yemen",
     "Coalition destroys six Houthi workshops",
     "Alliance strikes hit weapons workshops in the capital.",
     "Alliance"),
    ("Global", "United States",
     "Bayer's $7.25B Roundup settlement approved",
     "A court signs off on the multi-billion-dollar deal over claims.",
     "AP"),
    ("Europe", "Eastern Poland",
     "Russian missile lands in Poland",
     "A missile comes down across the border, raising the alarm in Warsaw.",
     "Reports"),
    ("Americas", "California, US",
     "California subpoenas Nvidia",
     "The state demands documents in its inquiry into the chipmaker.",
     "Reuters"),
    ("Asia", "New Delhi, India",
     "India launches first H3N1 vaccine",
     "A home-grown shot against the new flu strain goes into use.",
     "PR"),
    ("Asia", "Jakarta, Indonesia",
     "Jakarta asks Google: why 19,000 accounts gone?",
     "The ministry wants answers after thousands of accounts vanish.",
     "Ministry"),
    ("Europe", "London, UK",
     "Britain hits Moscow with cyberattacks",
     "London confirms offensive cyber operations against Russia.",
     "UK"),
    ("Americas", "Washington, US",
     "Trump: Iran wants a deal",
     "The president says Tehran is ready to talk as pressure builds.",
     "AP"),
    ("Oceania", "Melbourne, Australia",
     "Australia v England open T20 series at the MCG",
     "The rivals meet under lights tonight to start the series.",
     "Reports"),
]

# (region, place, headline, source) — one-liners 13..35
LINERS = [
    ("Europe", "The Hague", "China calls Myanmar genocide ruling \u201cunjust\u201d", "AP"),
    ("Asia", "New Delhi", "Modi opens SCO dialogue forum in New Delhi", "PR"),
    ("Europe", "Sumy", "HIMARS strike wipes out 20 Russian commanders", "Reports"),
    ("Americas", "Los Angeles", "Jury convicts man who started deadly 2025 Palisades Fire", "AP"),
    ("Americas", "Washington", "AP fact-checks false claims at Trump's post-Asia news conference", "AP"),
    ("Americas", "Ottawa", "World can no longer count on US leadership, forum chief warns", "Forum"),
    ("Africa", "Johannesburg", "Murder rate falls, but homicides still average 60 a day", "Stats"),
    ("Americas", "Southern Mexico", "Caravan of about 500 migrants crosses into Mexico", "Reports"),
    ("Africa", "West Kordofan", "Sudanese army says it cleared RSF strongholds in 10 areas", "Army"),
    ("Europe", "Brussels", "Rare EU-UK summit as Burnham seeks to mend Brexit's effects", "Reports"),
    ("Asia", "Tokyo", "China warns on climbing Mount Fuji; family offers reward for missing climber", "Reports"),
    ("Middle East", "Kabul", "UN warns ISIS-K is gaining drones and its threat is rising", "UN"),
    ("Europe", "Berlin", "Students march against rearmament and mandatory service", "Reports"),
    ("Europe", "Berlin", "\u201cCoalition of the willing\u201d meets on Ukraine with Zelenskyy in Berlin", "Reports"),
    ("Americas", "Washington", "Second judge blocks Trump's triumphal arch", "Court"),
    ("Americas", "Brasilia", "Brazil advances Indigenous land bill as leader meets Amazon chief Raoni", "Reports"),
    ("Middle East", "Baghdad", "Pipeline chief arrested over illicit oil trading accusations", "Reports"),
    ("Middle East", "Strait of Hormuz", "Iran claims waters 500 km beyond the strait, IRGC chief says", "IRGC"),
    ("Asia", "Mumbai", "IndusInd ends ex-CEO Kathpalia's job and seeks to recover his pay", "Reports"),
    ("Americas", "Washington", "SpaceX floats NATO membership for Ukraine in a post", "Report"),
    ("Europe", "Podgorica", "Montenegro rejects land concessions to Croatia in EU bid row", "Reports"),
    ("Americas", "Washington", "US engagement against Iran has cost $48.3B, Pentagon official says", "Reports"),
    ("Asia", "Tokyo", "Japan will buy up to 8m barrels of Saudi crude", "Reports"),
]

NUMBERS = [
    ("12", "killed in Russian strikes on Kryvyi Rih"),
    ("82", "wounded in the same attacks"),
    ("900,000", "AI chips cleared for China"),
    ("$7.25B", "Bayer Roundup settlement approved"),
    ("6", "Houthi workshops destroyed"),
    ("500", "migrants cross into Mexico"),
    ("60", "homicides a day in South Africa"),
]

EXCLUDED = ("Kyiv bridges hit", "Trump\u2013Xi summit in Shenzhen",
            "COP31 Friday closing session", "Senate 62\u201333 vote",
            "Anthropic IPO (19 Nov)", "Mexico Revolution Day parade",
            "GTA VI first-day sales")

ALL = LEADS + CARDS + [(r, p, h, "", s) for (r, p, h, s) in LINERS]
REGIONS = ["Europe", "Americas", "Asia", "Middle East", "Africa", "Global", "Oceania"]


def region_counts():
    counts = {r: 0 for r in REGIONS}
    for (r, *_rest) in ALL:
        counts[r] += 1
    return counts


# ---------------------------------------------------------------- illustrations
def illo_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 222))
    d.ellipse([x + w - 150, y + 18, x + w - 30, y + 138], fill=(232, 178, 74))
    d.ellipse([x + 60, y + h - 190, x + 250, y + h], fill=(52, 110, 168))
    d.ellipse([x + 95, y + h - 168, x + 150, y + h - 118], fill=(88, 150, 88))
    d.ellipse([x + 165, y + h - 140, x + 225, y + h - 88], fill=(88, 150, 88))
    d.ellipse([x + 120, y + h - 120, x + 190, y + h - 60], fill=(52, 110, 168))
    for i in range(5):
        d.rectangle([x + 300 + i * 34, y + h - 90, x + 326 + i * 34, y + h - 30],
                    fill=(20, 36, 61))
    d.polygon([(x + 300, y + h - 90), (x + 470, y + h - 90), (x + 385, y + h - 150)],
              fill=(158, 32, 32))
    d.rectangle([x, y + h - 28, x + w, y + h], fill=(139, 168, 118))


def illo_kryvyi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 58, 74))
    for bx, bw, bh in [(0, 90, 150), (100, 70, 210), (180, 110, 170),
                       (300, 80, 230), (390, 90, 160)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(30, 34, 46))
        for wy in range(y + h - bh + 18, y + h - 12, 30):
            d.rectangle([x + bx + 14, wy, x + bx + 30, wy + 16], fill=(232, 178, 74))
    d.ellipse([x + 330, y + 20, x + 430, y + 120], fill=(232, 120, 60))
    for sx, sy, r in [(120, 60, 26), (150, 40, 20), (95, 95, 18)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r], fill=(120, 120, 128))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(158, 32, 32))


def illo_chips(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(224, 232, 240))
    cx, cy = x + w // 2 - 40, y + 40
    d.rectangle([cx - 12, cy, cx + 172, cy + 130], fill=(176, 132, 52))
    d.rectangle([cx, cy + 12, cx + 160, cy + 118], fill=(20, 36, 61))
    d.rectangle([cx + 45, cy + 42, cx + 115, cy + 88], fill=(232, 178, 74))
    for i in range(5):
        d.rectangle([cx + 18 + i * 30, cy - 14, cx + 30 + i * 30, cy + 12], fill=(176, 132, 52))
        d.rectangle([cx + 18 + i * 30, cy + 118, cx + 30 + i * 30, cy + 144], fill=(176, 132, 52))
    d.line([x + 40, y + h - 40, x + w - 40, y + h - 40], fill=(158, 32, 32), width=6)
    d.polygon([(x + w - 60, y + h - 52), (x + w - 60, y + h - 28), (x + w - 30, y + h - 40)],
              fill=(158, 32, 32))
    d.text((x + 40, y + h - 78), "WASHINGTON  \u2192  BEIJING", font=font(SANS_B, 24), fill=INK)


def mini_factory(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 178))
    d.rectangle([x + 30, y + h - 70, x + w - 30, y + h - 20], fill=(120, 110, 95))
    d.polygon([(x + 40, y + h - 70), (x + 90, y + h - 110), (x + 140, y + h - 70)], fill=(158, 32, 32))
    d.rectangle([x + w - 90, y + 20, x + w - 70, y + h - 70], fill=(90, 84, 72))
    d.ellipse([x + w - 110, y + 8, x + w - 50, y + 55], fill=(150, 150, 150))


def mini_scales(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 232))
    cx = x + w // 2
    d.line([cx, y + 20, cx, y + h - 25], fill=INK, width=5)
    d.line([x + 60, y + 35, x + w - 60, y + 35], fill=INK, width=5)
    for sx in (x + 60, x + w - 60):
        d.line([sx, y + 35, sx, y + 75], fill=INK, width=3)
        d.polygon([(sx - 42, y + 78), (sx + 42, y + 78), (sx, y + 108)], fill=GOLD)
    d.rectangle([x + 40, y + h - 22, x + w - 40, y + h - 12], fill=INK)


def mini_missile(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(168, 205, 225))
    d.rectangle([x, y + h - 46, x + w, y + h], fill=(88, 150, 88))
    d.polygon([(x + 120, y + 30), (x + 190, y + 30), (x + 230, y + 60),
               (x + 190, y + 90), (x + 120, y + 90)], fill=(220, 220, 220))
    d.polygon([(x + 230, y + 60), (x + 280, y + 45), (x + 280, y + 75)], fill=RED)
    d.ellipse([x + 300, y + 45, x + 340, y + 75], fill=(232, 178, 74))
    d.rectangle([x + w - 130, y + 18, x + w - 30, y + 58], fill=(255, 255, 255))
    d.rectangle([x + w - 130, y + 38, x + w - 30, y + 58], fill=(200, 40, 40))


def mini_chip_doc(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 214))
    d.rectangle([x + 40, y + 25, x + 220, y + h - 20], fill=(255, 255, 255), outline=INK, width=3)
    for i in range(4):
        d.line([x + 60, y + 55 + i * 22, x + 200, y + 55 + i * 22], fill=MUTED, width=4)
    d.rectangle([x + w - 170, y + 30, x + w - 60, y + 90], fill=NAVY)
    d.rectangle([x + w - 140, y + 48, x + w - 90, y + 72], fill=GOLD)
    d.ellipse([x + w - 130, y + h - 90, x + w - 40, y + h - 10], fill=RED)
    d.text((x + w - 112, y + h - 68), "!", font=font(SANS_B, 44), fill=(255, 255, 255))


def mini_vaccine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 222))
    d.polygon([(x + 60, y + 40), (x + 130, y + 40), (x + 130, y + 95),
               (x + 60, y + 95)], fill=(255, 255, 255), outline=INK)
    d.polygon([(x + 130, y + 52), (x + 200, y + 52), (x + 200, y + 82),
               (x + 130, y + 82)], fill=(52, 110, 168))
    d.line([x + 200, y + 67, x + 260, y + 67], fill=INK, width=5)
    d.line([x + 60, y + 55, x + 60, y + 80], fill=RED, width=5)
    d.ellipse([x + w - 160, y + 15, x + w - 30, y + h - 15], fill=(24, 96, 96))
    d.text((x + w - 122, y + 42), "+", font=font(SANS_B, 52), fill=(255, 255, 255))


def mini_search(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(224, 232, 240))
    for i in range(3):
        d.rectangle([x + 40, y + 25 + i * 32, x + w - 120, y + 47 + i * 32],
                    fill=(255, 255, 255), outline=MUTED, width=2)
    d.ellipse([x + w - 110, y + 25, x + w - 30, y + 105], outline=NAVY, width=8)
    d.line([x + w - 45, y + 95, x + w - 10, y + 125], fill=NAVY, width=8)
    d.text((x + w - 92, y + 48), "?", font=font(SANS_B, 40), fill=NAVY)


def mini_cyber(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 36, 61))
    cx, cy = x + w // 2, y + h // 2
    d.polygon([(cx, cy - 55), (cx + 80, cy - 30), (cx + 80, cy + 20),
               (cx, cy + 60), (cx - 80, cy + 20), (cx - 80, cy - 30)], fill=(52, 110, 168))
    d.polygon([(cx + 12, cy - 35), (cx - 18, cy + 2), (cx + 6, cy + 2),
               (cx - 12, cy + 38), (cx + 20, cy - 6), (cx - 4, cy - 6)],
              fill=(232, 178, 74))


def mini_handshake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 178))
    d.rectangle([x + 40, y + 25, x + 200, y + 80], fill=(158, 32, 32))
    d.rectangle([x + w - 200, y + 55, x + w - 40, y + 110], fill=(20, 36, 61))
    d.ellipse([x + w // 2 - 90, y + 45, x + w // 2 + 90, y + 115], fill=(232, 178, 74))
    d.arc([x + w // 2 - 90, y + 45, x + w // 2 + 90, y + 115], 0, 180, fill=INK, width=4)


def mini_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(139, 168, 118))
    d.rectangle([x + w // 2 - 60, y + 20, x + w // 2 + 60, y + 60], fill=(232, 214, 178))
    d.rectangle([x + 90, y + 30, x + 130, y + 110], fill=(176, 132, 52))
    for i, sx in enumerate((x + 300, x + 330, x + 360)):
        d.rectangle([sx, y + h - 70, sx + 12, y + h - 15], fill=(232, 178, 74))
    d.ellipse([x + 130, y + 45, x + 175, y + 90], fill=RED)


CARD_ILLOS = [mini_factory, mini_scales, mini_missile, mini_chip_doc,
              mini_vaccine, mini_search, mini_cyber, mini_handshake, mini_cricket]
LEAD_ILLOS = [illo_cop31, illo_kryvyi, illo_chips]

# ---------------------------------------------------------------- render
def render(out_path):
    counts = region_counts()
    total = sum(counts.values())
    assert total == 35, f"story total {total} != 35"
    assert len(LEADS) == 3 and len(CARDS) == 9 and len(LINERS) == 23

    H = 4200
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 0

    # ---- masthead
    d.rectangle([0, y, W, y + 150], fill=NAVY)
    d.text((MARGIN, y + 18), "SATURDAY GAZETTE",
           font=font(SERIF_B, 84), fill=CREAM)
    d.text((W - MARGIN - 330, y + 62), "No. 325  \u00b7  ONE DAY, IN FULL",
           font=font(SANS, 24), fill=(200, 205, 215))
    y += 150
    d.rectangle([0, y, W, y + 46], fill=RED)
    draw_centered(d, y + 7,
                  "THE WORLD IN ONE DAY  \u00b7  35 STORIES  \u00b7  7 REGIONS  \u00b7  "
                  "EVERY ONE DATED SATURDAY 21 NOVEMBER 2026",
                  font(SANS_B, 22), CREAM)
    y += 46 + 26

    # ---- giant date
    draw_centered(d, y, "Saturday 21 November 2026", font(SERIF_B, 92), INK)
    y += 118
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=3)
    y += 14
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=1)
    y += 26

    # ---- italic headline strip
    strip = ("COP31 runs into overtime  \u00b7  Russian strikes kill 12 in Ukraine  "
             "\u00b7  US clears 900,000 AI chips for China")
    for line in wrap(d, strip, font(SERIF_I, 36), W - 2 * MARGIN):
        draw_centered(d, y, line, font(SERIF_I, 36), INK)
        y += 48
    y += 18
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=1)
    y += 22

    # ---- 7-number strip
    nbox = (W - 2 * MARGIN - 6 * 14) // 7
    strip_h = 196
    for i, (num, cap) in enumerate(NUMBERS):
        x0 = MARGIN + i * (nbox + 14)
        d.rectangle([x0, y, x0 + nbox, y + strip_h], outline=NAVY, width=3)
        d.rectangle([x0, y, x0 + nbox, y + 8], fill=NAVY)
        nsize = 46
        while nsize > 24 and d.textlength(num, font=font(SERIF_B, nsize)) > nbox - 16:
            nsize -= 2
        tw = d.textlength(num, font=font(SERIF_B, nsize))
        d.text((x0 + (nbox - tw) / 2, y + 20), num, font=font(SERIF_B, nsize), fill=RED)
        cy = y + 20 + nsize + 12
        for line in wrap(d, cap, font(SANS, 20), nbox - 18):
            tw = d.textlength(line, font=font(SANS, 20))
            d.text((x0 + (nbox - tw) / 2, cy), line, font=font(SANS, 20), fill=INK)
            cy += 25
    y += strip_h + 26

    # ---- region bar
    d.rectangle([0, y, W, y + 64], fill=NAVY)
    parts = [f"{r.upper()} {counts[r]}" for r in REGIONS]
    bar = "   \u00b7   ".join(parts) + f"   \u2014   TOTAL {total}"
    bsize = 26
    while bsize > 16 and d.textlength(bar, font=font(SANS_B, bsize)) > W - 120:
        bsize -= 1
    draw_centered(d, y + (64 - bsize) // 2 - 2, bar, font(SANS_B, bsize), CREAM)
    y += 64 + 22

    # ---- date-check strip near top
    box_h = 96
    d.rectangle([MARGIN, y, W - MARGIN, y + box_h], outline=RED, width=3)
    d.rectangle([MARGIN, y, MARGIN + 14, y + box_h], fill=RED)
    d.text((MARGIN + 30, y + 10), "DATE CHECK \u2014 WHAT WE LEFT OUT",
           font=font(SANS_B, 24), fill=RED)
    excl = "Left out on purpose \u2014 all dated 20 Nov or earlier: " + ";  ".join(EXCLUDED) + "."
    cy = y + 44
    for line in wrap(d, excl, font(SANS, 21), W - 2 * MARGIN - 60):
        d.text((MARGIN + 30, cy), line, font=font(SANS, 21), fill=INK)
        cy += 26
    y += box_h + 30

    # ---- section header
    d.text((MARGIN, y), "THE LEADS", font=font(SANS_B, 26), fill=RED)
    d.line([MARGIN + 170, y + 16, W - MARGIN, y + 16], fill=RULE, width=2)
    y += 44

    # ---- 3 big leads
    lead_top = y
    for i, (region, place, head, deck, src) in enumerate(LEADS):
        x0 = MARGIN + i * (COLW + 26)
        LEAD_ILLOS[i](d, x0, y, COLW, 270)
        ly = y + 270 + 16
        d.text((x0, ly), f"{region.upper()}  \u00b7  {place.upper()}",
               font=font(SANS_B, 20), fill=RED)
        ly += 30
        for line in wrap(d, head, font(SERIF_B, 38), COLW):
            d.text((x0, ly), line, font=font(SERIF_B, 38), fill=INK)
            ly += 46
        ly += 4
        for line in wrap(d, deck, font(SANS, 23), COLW):
            d.text((x0, ly), line, font=font(SANS, 23), fill=MUTED)
            ly += 30
        ly += 6
        d.text((x0, ly), f"Source: {src}", font=font(SANS_B, 20), fill=INK)
    y = lead_top + 270 + 16 + 30 + 3 * 46 + 4 + 3 * 30 + 6 + 26 + 34

    # ---- 9 small cards
    d.text((MARGIN, y), "NINE MORE", font=font(SANS_B, 26), fill=RED)
    d.line([MARGIN + 175, y + 16, W - MARGIN, y + 16], fill=RULE, width=2)
    y += 44
    card_top = y
    for i, (region, place, head, deck, src) in enumerate(CARDS):
        row, col = divmod(i, 3)
        x0 = MARGIN + col * (COLW + 26)
        cy0 = card_top + row * 330
        CARD_ILLOS[i](d, x0, cy0, COLW, 130)
        ly = cy0 + 130 + 12
        d.text((x0, ly), f"{region.upper()}  \u00b7  {place.upper()}",
               font=font(SANS_B, 18), fill=RED)
        ly += 26
        for line in wrap(d, head, font(SERIF_B, 29), COLW):
            d.text((x0, ly), line, font=font(SERIF_B, 29), fill=INK)
            ly += 36
        ly += 2
        for line in wrap(d, deck, font(SANS, 21), COLW):
            d.text((x0, ly), line, font=font(SANS, 21), fill=MUTED)
            ly += 27
        ly += 4
        d.text((x0, ly), f"Source: {src}", font=font(SANS_B, 18), fill=INK)
    y = card_top + 3 * 330 + 30

    # ---- 23 one-liners
    hdr = "ALSO ON SATURDAY 21 NOVEMBER \u2014 23 MORE STORIES"
    d.text((MARGIN, y), hdr, font=font(SANS_B, 26), fill=RED)
    hw = d.textlength(hdr, font=font(SANS_B, 26))
    d.line([MARGIN + hw + 20, y + 16, W - MARGIN, y + 16], fill=RULE, width=2)
    y += 44
    for n, (region, place, head, src) in enumerate(LINERS, start=13):
        prefix = f"{n}. "
        full = f"{head} \u2014 {place} \u00b7 {src}"
        lines = wrap(d, full, font(SERIF, 27), W - 2 * MARGIN - 70)
        d.text((MARGIN, y), prefix, font=font(SERIF_B, 27), fill=RED)
        ly = y
        for line in lines:
            d.text((MARGIN + 70, ly), line, font=font(SERIF, 27), fill=INK)
            ly += 36
        y = ly + 8
    y += 18

    # ---- footer
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=3)
    y += 16
    foot = ("Every story here happened, or was first reported, on Saturday "
            "21 November 2026  \u00b7  Sources named beside each story  \u00b7  "
            "Drawn illustrations, not photographs")
    for line in wrap(d, foot, font(SANS, 22), W - 2 * MARGIN):
        draw_centered(d, y, line, font(SANS, 22), MUTED)
        y += 30
    y += 8
    draw_centered(d, y, "SATURDAY GAZETTE  \u00b7  21 NOVEMBER 2026  \u00b7  35 STORIES",
                  font(SANS_B, 22), INK)
    y += 34

    img = img.crop((0, 0, W, y + MARGIN))
    img.save(out_path, "PNG", optimize=True)
    print(f"wrote {out_path} {img.size[0]}x{img.size[1]}")
    print(f"stories: {total} (leads 3, cards 9, one-liners 23)")
    print("regions: " + ", ".join(f"{r} {counts[r]}" for r in REGIONS)
          + f" = {total}")
    return img.size


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or (sys.argv[1] if len(sys.argv) > 1 else "/output")
    os.makedirs(out_dir, exist_ok=True)
    render(os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()

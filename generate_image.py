#!/usr/bin/env python3
"""Draw the 25 Nov 2026 newspaper front page (1024x1024) with PIL only.

The Daily Globe: a one-image summary of the world news of Wednesday
25 November 2026, laid out as a newspaper front page. Every story was
compiled from Reuters, AP and AFP reporting of 24-25 November 2026,
and every picture on the page is drawn here, in code.
"""
from PIL import Image, ImageDraw, ImageFont
import os

F = "/usr/share/fonts/truetype/liberation/"
SERIF_B = F + "LiberationSerif-Bold.ttf"
SERIF = F + "LiberationSerif-Regular.ttf"
SERIF_I = F + "LiberationSerif-Italic.ttf"
SANS_B = F + "LiberationSans-Bold.ttf"
SANS = F + "LiberationSans-Regular.ttf"

W = H = 1024
PAPER = (250, 247, 238)
INK = (18, 18, 18)
RED = (163, 22, 33)
GRAY = (90, 88, 82)
RULE = (30, 30, 30)
FAINT = (178, 174, 164)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def font(path, size):
    return ImageFont.truetype(path, size)

def text_w(s, f):
    return d.textlength(s, font=f)

def center(s, y, f, fill=INK):
    d.text(((W - text_w(s, f)) / 2, y), s, font=f, fill=fill)

def wrap(s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(t, f) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def para(s, x, y, f, maxw, lh, fill=INK):
    for ln in wrap(s, f, maxw):
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y

M = 36
d.rectangle([14, 14, W - 14, H - 14], outline=RULE, width=3)
d.rectangle([20, 20, W - 20, H - 20], outline=RULE, width=1)

f_small = font(SANS, 15)
d.text((M, 30), "Vol. I · No. 25", font=f_small, fill=GRAY)
r = "WORLD EDITION"
d.text((W - M - text_w(r, f_small), 30), r, font=f_small, fill=GRAY)
c = "ONE PAGE · THE WHOLE WORLD"
d.text(((W - text_w(c, f_small)) / 2, 30), c, font=f_small, fill=GRAY)
d.line([M, 56, W - M, 56], fill=RULE, width=2)

center("THE DAILY GLOBE", 58, font(SERIF_B, 88))
d.line([M, 156, W - M, 156], fill=RULE, width=4)
d.line([M, 164, W - M, 164], fill=RULE, width=1)

f_date = font(SANS_B, 20)
d.text((M, 175), "Wednesday, 25 November 2026", font=f_date, fill=INK)
f_motto = font(SERIF_I, 17)
m2 = "The day's world news, summed up on a single page"
d.text((W - M - text_w(m2, f_motto), 176), m2, font=f_motto, fill=GRAY)
d.line([M, 206, W - M, 206], fill=RULE, width=2)

# ---------- LEAD ----------
y = 218
f_kick = font(SANS_B, 17)
d.text((M, y), "NEW YORK  ·  FEDERAL COURT", font=f_kick, fill=RED)
y += 28
f_head = font(SERIF_B, 57)
for ln in ["HUAWEI CONVICTED IN U.S.", "CRIMINAL TRIAL"]:
    assert text_w(ln, f_head) <= W - 2 * M, ln
    d.text((M, y), ln, font=f_head, fill=INK)
    y += 57
y += 4
f_deck = font(SERIF_I, 21)
y = para("Jury finds the Chinese tech giant guilty on 10 of 12 counts — bank fraud and conspiring "
         "to steal trade secrets — after a three-month trial. Huawei rejects the verdict.",
         M, y, f_deck, W - 2 * M, 27)
y += 8

# body (left) + visual (right)
row_y = y
f_body = font(SERIF, 18)
para("A federal jury in New York convicted Huawei, the world's biggest maker of telecom "
     "equipment, after a sprawling trial over its Iran business and the theft of trade "
     "secrets. The company, long accused by Washington of posing a security risk, said "
     "the verdicts lacked legal or factual basis. Sentencing follows; the case caps "
     "years of U.S.–China technology tension.", M, row_y, f_body, 540, 24)

vx0, vy0, vx1, vy1 = 612, row_y, W - M, row_y + 168
d.rectangle([vx0, vy0, vx1, vy1], outline=RULE, width=2)
cx = (vx0 + vx1) / 2
d.polygon([(cx - 118, vy0 + 62), (cx + 118, vy0 + 62), (cx, vy0 + 18)], outline=INK, fill=(238, 233, 219))
d.line([cx - 130, vy0 + 68, cx + 130, vy0 + 68], fill=INK, width=4)
for i in range(5):
    x = cx - 94 + i * 47
    d.rectangle([x, vy0 + 76, x + 15, vy0 + 138], outline=INK, width=2, fill=(244, 240, 228))
d.rectangle([cx - 11, vy0 + 108, cx + 11, vy0 + 138], fill=INK)
d.line([cx - 116, vy0 + 146, cx + 116, vy0 + 146], fill=INK, width=4)
d.line([cx - 128, vy0 + 155, cx + 128, vy0 + 155], fill=INK, width=3)

stamp = Image.new("RGBA", (260, 80), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rounded_rectangle([4, 4, 256, 76], radius=8, outline=(163, 22, 33, 255), width=5)
sf = font(SANS_B, 46)
sd.text(((260 - sd.textlength("GUILTY", font=sf)) / 2, 13), "GUILTY", font=sf, fill=(163, 22, 33, 255))
stamp = stamp.rotate(13, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (706, row_y + 62), stamp)
d = ImageDraw.Draw(img)

y = row_y + 178
d.line([M, y, W - M, y], fill=RULE, width=3)
y += 10

# ---------- SUB-STORY GRID ----------
col_w = (W - 2 * M - 24) / 2
f_k2 = font(SANS_B, 15)
f_h2 = font(SERIF_B, 26)
f_b2 = font(SERIF, 16)

stories = [
    ("WASHINGTON · SECURITY", "CIA Hit by Cyber Breach",
     "Attackers breached an unclassified system at the CIA and the office of the Director "
     "of National Intelligence, a source said — the latest intrusion to rock U.S. agencies."),
    ("KYIV · WAR AT SEA", "Ukraine Strikes Russian Ships",
     "Zelenskiy confirms Ukrainian drones sank a Russian warship in Benghazi harbour, "
     "Libya, and hit a cargo ship in the Gulf of Finland. Norway urges caution."),
    ("ITURI, CONGO · HEALTH", "WHO Evacuates Ebola Hospital",
     "Health workers sheltered three days from fierce fighting before evacuation from a "
     "hospital in Ituri. The record outbreak: 11,762 cases and 5,775 deaths."),
    ("PARIS · JUSTICE", "Sarkozy Case Sent to Trial",
     "French officials order ex-president Nicolas Sarkozy and his wife Carla Bruni to "
     "stand trial for corruption. First hearing: 1 April 2027."),
]
gy = y
row_h = 108
for i, (kick, head, body) in enumerate(stories):
    cx0 = M + (i % 2) * (col_w + 24)
    cy0 = gy + (i // 2) * row_h
    d.text((cx0, cy0), kick, font=f_k2, fill=RED)
    d.text((cx0, cy0 + 20), head, font=f_h2, fill=INK)
    para(body, cx0, cy0 + 50, f_b2, col_w, 18)
    if i % 2 == 0:
        d.line([cx0 + col_w + 12, cy0 + 2, cx0 + col_w + 12, cy0 + row_h - 14], fill=FAINT, width=1)
    if i < 2:
        d.line([cx0, cy0 + row_h - 6, cx0 + col_w, cy0 + row_h - 6], fill=FAINT, width=1)
y = gy + 2 * row_h
d.line([M, y, W - M, y], fill=RULE, width=2)
y += 9

# wide story
d.text((M, y), "RIYADH · MIDDLE EAST", font=f_k2, fill=RED)
d.text((M + 218, y - 5), "Drone Strike Injures 11 at Riyadh Tower", font=f_h2, fill=INK)
y += 22
y = para("Eleven people were injured in a Houthi drone attack on Riyadh's tallest tower — the second strike on the "
         "building within days. In Yemen, Houthi fighters have pushed to within 60 km of Aden, whose "
         "government insists the port city will not fall.",
         M, y, f_b2, W - 2 * M, 19)
y += 8

# ALSO TODAY
d.rectangle([M, y, W - M, y + 26], fill=INK)
d.text((M + 12, y + 5), "ALSO TODAY", font=font(SANS_B, 16), fill=PAPER)
y += 32
f_tick = font(SERIF, 15)
ticker = ("Trump pardons turkeys Freedom & Feathers, awards Giuliani the Medal of Freedom  ·  U.S. consumer "
          "confidence at a near-two-year high  ·  Chess: Gukesh–Sindarov draw Game 1 in Geneva  ·  Radar outage delays O'Hare flights")
y = para(ticker, M, y, f_tick, W - 2 * M, 20)
y += 4
d.line([M, y, W - M, y], fill=RULE, width=2)
f_foot = font(SERIF_I, 13)
center("Compiled from Reuters, Associated Press and AFP reports of 24–25 November 2026 · Every picture on this page was drawn for this page",
       y + 7, f_foot, fill=GRAY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes; content ends y =", y + 24)

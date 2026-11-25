#!/usr/bin/env python3
"""The Daily Globe — a one-image summary of the world news of
Wednesday 25 November 2026, drawn as a newspaper front page.

The page is rendered with PIL only. All stories were compiled from
Reuters, AP and AFP reporting of 24-25 November 2026; every picture
on the page (the courthouse, the GUILTY stamp) is drawn in code here.
Running this file writes entry.png beside it, deterministically.
"""
import os
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
TYPE = {
    "serif": "LiberationSerif-Regular.ttf",
    "serif_bold": "LiberationSerif-Bold.ttf",
    "serif_italic": "LiberationSerif-Italic.ttf",
    "sans_bold": "LiberationSans-Bold.ttf",
    "sans": "LiberationSans-Regular.ttf",
}

def face(kind, size):
    return ImageFont.truetype(FONT_DIR + TYPE[kind], size)

def ink(hexcode):
    return tuple(int(hexcode[i:i + 2], 16) for i in (0, 2, 4))

PAPER = ink("faf7ee")
BLACK = ink("121212")
ACCENT = ink("a31621")
MUTED = ink("5a5852")
HAIRLINE = ink("b2aea4")
SIZE = 1024
EDGE = 36

page = Image.new("RGB", (SIZE, SIZE), PAPER)
pen = ImageDraw.Draw(page)

def width_of(text, fnt):
    return pen.textlength(text, font=fnt)

def centred(text, top, fnt, colour=BLACK):
    pen.text(((SIZE - width_of(text, fnt)) / 2, top), text, font=fnt, fill=colour)

def flow(text, left, top, fnt, measure, leading, colour=BLACK):
    """Greedy word wrap; returns the y just past the last line."""
    line = ""
    for word in text.split():
        trial = word if not line else line + " " + word
        if width_of(trial, fnt) > measure and line:
            pen.text((left, top), line, font=fnt, fill=colour)
            top += leading
            line = word
        else:
            line = trial
    if line:
        pen.text((left, top), line, font=fnt, fill=colour)
        top += leading
    return top

def hline(left, top, right, colour=BLACK, weight=1):
    pen.line([left, top, right, top], fill=colour, width=weight)

# ---------------------------------------------------------------- frame
pen.rectangle([14, 14, SIZE - 14, SIZE - 14], outline=BLACK, width=3)
pen.rectangle([20, 20, SIZE - 20, SIZE - 20], outline=BLACK, width=1)

small = face("sans", 15)
pen.text((EDGE, 30), "Vol. I · No. 25", font=small, fill=MUTED)
tag = "ONE PAGE · THE WHOLE WORLD"
centred(tag, 30, small, MUTED)
right_tag = "WORLD EDITION"
pen.text((SIZE - EDGE - width_of(right_tag, small), 30), right_tag, font=small, fill=MUTED)
hline(EDGE, 56, SIZE - EDGE, BLACK, 2)

centred("THE DAILY GLOBE", 58, face("serif_bold", 88))
hline(EDGE, 156, SIZE - EDGE, BLACK, 4)
hline(EDGE, 164, SIZE - EDGE, BLACK, 1)

pen.text((EDGE, 175), "Wednesday, 25 November 2026", font=face("sans_bold", 20), fill=BLACK)
motto = "The day's world news, summed up on a single page"
pen.text((SIZE - EDGE - width_of(motto, face("serif_italic", 17)), 176),
         motto, font=face("serif_italic", 17), fill=MUTED)
hline(EDGE, 206, SIZE - EDGE, BLACK, 2)

# ---------------------------------------------------------------- lead
cursor = 218
pen.text((EDGE, cursor), "NEW YORK  ·  FEDERAL COURT", font=face("sans_bold", 17), fill=ACCENT)
cursor += 28
headline_face = face("serif_bold", 57)
for banner in ("HUAWEI CONVICTED IN U.S.", "CRIMINAL TRIAL"):
    pen.text((EDGE, cursor), banner, font=headline_face, fill=BLACK)
    cursor += 57
cursor = flow(
    "Jury finds the Chinese tech giant guilty on 10 of 12 counts — bank fraud and "
    "conspiring to steal trade secrets — after a three-month trial. Huawei rejects the verdict.",
    EDGE, cursor + 4, face("serif_italic", 21), SIZE - 2 * EDGE, 27)
cursor += 8

# lead body sits left; the courthouse drawing sits right, in a ruled box
body_top = cursor
flow(
    "A federal jury in New York convicted Huawei, the world's biggest maker of telecom "
    "equipment, after a sprawling trial over its Iran business and the theft of trade "
    "secrets. The company, long accused by Washington of posing a security risk, said "
    "the verdicts lacked legal or factual basis. Sentencing follows; the case caps "
    "years of U.S.–China technology tension.",
    EDGE, body_top, face("serif", 18), 540, 24)

box = (612, body_top, SIZE - EDGE, body_top + 168)
pen.rectangle(box, outline=BLACK, width=2)
mid = (box[0] + box[2]) / 2
roof_y = box[1] + 62
pen.polygon([(mid - 118, roof_y), (mid + 118, roof_y), (mid, box[1] + 18)],
            outline=BLACK, fill=ink("eee9db"))
hline(mid - 130, roof_y + 6, mid + 130, BLACK, 4)
for n in range(5):
    col_x = mid - 94 + n * 47
    pen.rectangle([col_x, box[1] + 76, col_x + 15, box[1] + 138],
                  outline=BLACK, width=2, fill=ink("f4f0e4"))
pen.rectangle([mid - 11, box[1] + 108, mid + 11, box[1] + 138], fill=BLACK)
hline(mid - 116, box[1] + 146, mid + 116, BLACK, 4)
hline(mid - 128, box[1] + 155, mid + 128, BLACK, 3)

# the verdict, stamped over the courthouse in red
stamp = Image.new("RGBA", (260, 80), (0, 0, 0, 0))
stamp_pen = ImageDraw.Draw(stamp)
stamp_pen.rounded_rectangle([4, 4, 256, 76], radius=8, outline=ACCENT + (255,), width=5)
verdict = "GUILTY"
stamp_face = face("sans_bold", 46)
stamp_pen.text(((260 - stamp_pen.textlength(verdict, font=stamp_face)) / 2, 13),
               verdict, font=stamp_face, fill=ACCENT + (255,))
tilted = stamp.rotate(13, expand=True, resample=Image.BICUBIC)
page.paste(tilted, (706, body_top + 62), tilted)
pen = ImageDraw.Draw(page)

cursor = body_top + 178
hline(EDGE, cursor, SIZE - EDGE, BLACK, 3)
cursor += 10

# ---------------------------------------------------------------- grid
STORIES = [
    {"beat": "WASHINGTON · SECURITY", "head": "CIA Hit by Cyber Breach",
     "body": "Attackers breached an unclassified system at the CIA and the office of the "
             "Director of National Intelligence, a source said — the latest intrusion to "
             "rock U.S. agencies."},
    {"beat": "KYIV · WAR AT SEA", "head": "Ukraine Strikes Russian Ships",
     "body": "Zelenskiy confirms Ukrainian drones sank a Russian warship in Benghazi "
             "harbour, Libya, and hit a cargo ship in the Gulf of Finland. Norway urges caution."},
    {"beat": "ITURI, CONGO · HEALTH", "head": "WHO Evacuates Ebola Hospital",
     "body": "Health workers sheltered three days from fierce fighting before evacuation "
             "from a hospital in Ituri. The record outbreak: 11,762 cases and 5,775 deaths."},
    {"beat": "PARIS · JUSTICE", "head": "Sarkozy Case Sent to Trial",
     "body": "French officials order ex-president Nicolas Sarkozy and his wife Carla "
             "Bruni to stand trial for corruption. First hearing: 1 April 2027."},
]
COLUMN = (SIZE - 2 * EDGE - 24) / 2
ROW = 108
grid_top = cursor
for idx, story in enumerate(STORIES):
    sx = EDGE + (idx % 2) * (COLUMN + 24)
    sy = grid_top + (idx // 2) * ROW
    pen.text((sx, sy), story["beat"], font=face("sans_bold", 15), fill=ACCENT)
    pen.text((sx, sy + 20), story["head"], font=face("serif_bold", 26), fill=BLACK)
    flow(story["body"], sx, sy + 50, face("serif", 16), COLUMN, 18)
    if idx % 2 == 0:
        pen.line([sx + COLUMN + 12, sy + 2, sx + COLUMN + 12, sy + ROW - 14], fill=HAIRLINE, width=1)
    if idx < 2:
        hline(sx, sy + ROW - 6, sx + COLUMN, HAIRLINE, 1)
cursor = grid_top + 2 * ROW
hline(EDGE, cursor, SIZE - EDGE, BLACK, 2)
cursor += 9

# ---------------------------------------------------------------- wide story
pen.text((EDGE, cursor), "RIYADH · MIDDLE EAST", font=face("sans_bold", 15), fill=ACCENT)
pen.text((EDGE + 218, cursor - 5), "Drone Strike Injures 11 at Riyadh Tower",
         font=face("serif_bold", 26), fill=BLACK)
cursor = flow(
    "Eleven people were injured in a Houthi drone attack on Riyadh's tallest tower — the "
    "second strike on the building within days. In Yemen, Houthi fighters have pushed to "
    "within 60 km of Aden, whose government insists the port city will not fall.",
    EDGE, cursor + 22, face("serif", 16), SIZE - 2 * EDGE, 19)
cursor += 8

# ---------------------------------------------------------------- also today
pen.rectangle([EDGE, cursor, SIZE - EDGE, cursor + 26], fill=BLACK)
pen.text((EDGE + 12, cursor + 5), "ALSO TODAY", font=face("sans_bold", 16), fill=PAPER)
cursor = flow(
    "Trump pardons turkeys Freedom & Feathers, awards Giuliani the Medal of Freedom  ·  "
    "U.S. consumer confidence at a near-two-year high  ·  Chess: Gukesh–Sindarov draw "
    "Game 1 in Geneva  ·  Radar outage delays O'Hare flights",
    EDGE, cursor + 32, face("serif", 15), SIZE - 2 * EDGE, 20)
cursor += 4
hline(EDGE, cursor, SIZE - EDGE, BLACK, 2)
centred("Compiled from Reuters, Associated Press and AFP reports of 24–25 November 2026 · "
        "Every picture on this page was drawn for this page",
        cursor + 7, face("serif_italic", 13), MUTED)

target = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
page.save(target, optimize=True)
print("saved", target, os.path.getsize(target), "bytes; content ends y =", cursor + 24)

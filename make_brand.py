# -*- coding: utf-8 -*-
"""
Solar Insights brand assets generator.
Outputs (in this folder):
  - linkedin-logo-1000.png        square logo for LinkedIn (circle-safe)
  - wordmark-transparent.png      horizontal wordmark, transparent bg (white text, dark-bg use)
  - wordmark-dark-transparent.png horizontal wordmark, transparent bg (dark text, light-bg use)
  - business-card-front.png       Simona Fleanta - Solar Energy Specialist
  - business-card-back.png        clean brand back
Brand: light corporate, ink #0B0F08, greens #adfc03 / #86b81a / #5b7a16,
wordmark S(o)LAR INSIGHTS (o = flat dot mark, #adfc03). No gradients/glow — flat marks only.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---- palette ----
BG        = (255, 255, 255)   # card/site background (light)
INK       = (11, 15, 8)       # #0B0F08 — near-black text
WHITE     = (255, 255, 255)
GREEN     = (173, 252, 3)     # #adfc03 — dot mark, highlights
GREEN_MID = (134, 184, 26)    # #86b81a — CTAs, icon fills
GREEN_D   = (91, 122, 22)     # #5b7a16 — body-safe accent text
GRAY      = (110, 118, 100)   # secondary text on light bg
GRAY_D    = (150, 156, 140)   # tertiary / faint text

FONT = "C:/Windows/Fonts/bahnschrift.ttf"
ARIAL   = "C:/Windows/Fonts/arial.ttf"
ARIALBD = "C:/Windows/Fonts/arialbd.ttf"

def f(size, path=FONT):
    return ImageFont.truetype(path, size)

# ---- flat dot mark (no glow) ----
def paste_dot(img, cx, cy, r, color=GREEN):
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

def tracked_len(draw, text, font, tracking):
    return sum(draw.textlength(ch, font=font) + tracking for ch in text) - tracking

def draw_tracked(draw, x, y, text, font, fill, tracking):
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x

# =====================================================================
# Wordmark renderer:  S [dot] LAR  INSIGHTS
# Returns total width. Draws at baseline-top y.
# =====================================================================
def wordmark(img, draw, x, y, size, tracking_ratio=0.14, gap_ratio=0.55,
             text_color=INK, measure_only=False):
    font = f(size)
    tr = size * tracking_ratio
    asc, desc = font.getmetrics()
    cap = size * 0.70
    dot_r = cap * 0.42
    x_cur = x
    word_gap = size * gap_ratio
    total = 0
    total += tracked_len(draw, "S", font, tr) + tr
    total += dot_r*2 + tr
    total += tracked_len(draw, "LAR", font, tr) + word_gap
    total += tracked_len(draw, "INSIGHTS", font, tr)
    if measure_only:
        return total
    x_cur = draw_tracked(draw, x_cur, y, "S", font, text_color, tr)
    dot_cy = y + asc - cap*0.5
    dot_cx = x_cur + dot_r
    paste_dot(img, dot_cx, dot_cy, int(dot_r), GREEN)
    x_cur = dot_cx + dot_r + tr
    x_cur = draw_tracked(draw, x_cur, y, "LAR", font, text_color, tr)
    x_cur += word_gap - tr
    x_cur = draw_tracked(draw, x_cur, y, "INSIGHTS", font, text_color, tr)
    return total

# =====================================================================
# 1) LINKEDIN SQUARE LOGO  (stacked, circle-safe, light canvas)
# =====================================================================
def linkedin_logo(scale=1):
    S = 1000 * scale
    img = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(img)

    # emblem: flat dot up top
    dot_r = int(S*0.052)
    dot_cy = int(S*0.335)
    paste_dot(img, S/2, dot_cy, dot_r, GREEN)
    d = ImageDraw.Draw(img)

    # "SOLAR"
    size1 = int(S*0.130)
    ft = f(size1)
    tr = size1*0.16
    solar = "SOLAR"
    w = tracked_len(d, solar, ft, tr)
    yy = int(S*0.46)
    draw_tracked(d, (S-w)/2, yy, solar, ft, INK, tr)
    # "INSIGHTS"
    size2 = int(S*0.130)
    ft2 = f(size2)
    tr2 = size2*0.16
    ins = "INSIGHTS"
    w2 = tracked_len(d, ins, ft2, tr2)
    yy2 = yy + int(size1*1.15)
    draw_tracked(d, (S-w2)/2, yy2, ins, ft2, INK, tr2)
    # divider
    dy = yy2 + int(size2*1.35)
    d.line([(S*0.30, dy), (S*0.70, dy)], fill=(225, 228, 218), width=max(1,int(S*0.002)))
    # tagline
    tag = "ENERGY ECONOMICS ADVISORY"
    ftg = f(int(S*0.040))
    trg = int(S*0.040)*0.22
    wt = tracked_len(d, tag, ftg, trg)
    draw_tracked(d, (S-wt)/2, dy+int(S*0.028), tag, ftg, GREEN_D, trg)

    img.save("linkedin-logo-1000.png")
    print("saved linkedin-logo-1000.png", img.size)

# =====================================================================
# 2) HORIZONTAL WORDMARK, transparent bg
# =====================================================================
def _wordmark_transparent(filename, text_color):
    tmp = Image.new("RGBA", (10,10))
    td = ImageDraw.Draw(tmp)
    size = 150
    total = wordmark(tmp, td, 0, 0, size, measure_only=True)
    W = int(total + 120)
    H = int(size*1.7)
    img = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(img)
    wordmark(img, d, 60, int(size*0.28), size, text_color=text_color)
    img.save(filename)
    print("saved", filename, img.size)

def wordmark_transparent():
    _wordmark_transparent("wordmark-transparent.png", WHITE)         # for dark-bg use
    _wordmark_transparent("wordmark-dark-transparent.png", INK)      # for light-bg use (default)

# =====================================================================
# 3) BUSINESS CARD FRONT  (85x55mm @300dpi = 1004x650, light canvas)
# =====================================================================
def card_front():
    W, H = 1004, 650
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # half-sun motif, top-right — concentric rings in the brand palette,
    # centered on the top edge so exactly half is visible
    sun_cx, sun_cy = W - 220, 0
    d.ellipse([sun_cx-170, sun_cy-170, sun_cx+170, sun_cy+170], fill=GREEN_D)
    d.ellipse([sun_cx-115, sun_cy-115, sun_cx+115, sun_cy+115], fill=GREEN_MID)
    d.ellipse([sun_cx-55, sun_cy-55, sun_cx+55, sun_cy+55], fill=GREEN)

    M = 68  # left margin
    # wordmark top-left
    wordmark(img, d, M, 60, 46, text_color=INK)
    d = ImageDraw.Draw(img)

    # name
    nf = f(78, ARIALBD)
    d.text((M, 250), "Simona Fleanta", font=nf, fill=INK)
    # title
    tf = f(38)
    draw_tracked(d, M, 348, "ADVISOR & ASSET ANALYST", tf, GREEN_D, 38*0.10)
    # divider
    d.line([(M, 428), (M+180, 428)], fill=GREEN_MID, width=3)

    # contacts
    cf = f(30, ARIAL)
    lines = [
        "+40 755 371 352",
        "simo.fleanta@gmail.com",
        "linkedin.com/in/vsimonafleanta",
        "solarinsights.vercel.app",
    ]
    yy = 470
    for ln in lines:
        d.ellipse([M, yy+11, M+9, yy+20], fill=GREEN_MID)
        d.text((M+26, yy), ln, font=cf, fill=INK if ln.endswith("app") else GRAY)
        yy += 44
    img.save("business-card-front.png")
    print("saved business-card-front.png", img.size)

# =====================================================================
# 4) BUSINESS CARD BACK  (solid brand card, logo only — entera-style pairing:
#    one solid-color brand face + one white info face)
# =====================================================================
def card_back():
    W, H = 1004, 650
    img = Image.new("RGB", (W, H), GREEN_D)
    d = ImageDraw.Draw(img)
    # centered wordmark, white text on solid green
    size = 58
    total = wordmark(img, d, 0, 0, size, measure_only=True)
    wordmark(img, d, (W-total)/2, H/2 - size*0.36, size, text_color=WHITE)
    img.save("business-card-back.png")
    print("saved business-card-back.png", img.size)

# =====================================================================
# 5) BUSINESS CARDS PDF  (2-page print-ready PDF, front + back, 300dpi)
# =====================================================================
def cards_pdf():
    front = Image.open("business-card-front.png").convert("RGB")
    back = Image.open("business-card-back.png").convert("RGB")
    front.save("business-cards.pdf", "PDF", resolution=300.0, save_all=True, append_images=[back])
    print("saved business-cards.pdf")

if __name__ == "__main__":
    linkedin_logo()
    wordmark_transparent()
    card_front()
    card_back()
    cards_pdf()
    print("DONE")

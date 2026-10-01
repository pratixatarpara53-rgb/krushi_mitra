"""
Generate attractive crop placeholder images for KhedutMitra.
Each image has a gradient background, crop emoji, name, and season label.
"""
from PIL import Image, ImageDraw, ImageFont
import os, math

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "static", "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 600, 400

CROPS = [
    # (filename,  name,        season,    emoji, top_color,       bot_color)
    ("cotton.jpg",    "Cotton",    "Kharif",  "🌿", (34,120,60),     (20,80,40)),
    ("groundnut.jpg", "Groundnut", "Kharif",  "🥜", (180,120,30),    (130,80,10)),
    ("wheat.jpg",     "Wheat",     "Rabi",    "🌾", (200,160,40),    (150,110,20)),
    ("bajra.jpg",     "Bajra",     "Kharif",  "🌾", (160,100,30),    (110,65,10)),
    ("maize.jpg",     "Maize",     "Kharif",  "🌽", (220,170,20),    (170,120,10)),
    ("cumin.jpg",     "Cumin",     "Rabi",    "🌱", (100,140,60),    (60,100,30)),
    ("chilli.jpg",    "Chilli",    "Kharif",  "🌶️", (200,50,30),     (150,20,10)),
    ("onion.jpg",     "Onion",     "Rabi",    "🧅", (160,60,130),    (110,30,90)),
]

def make_gradient(draw, w, h, top_rgb, bot_rgb):
    for y in range(h):
        t = y / h
        r = int(top_rgb[0] + (bot_rgb[0] - top_rgb[0]) * t)
        g = int(top_rgb[1] + (bot_rgb[1] - top_rgb[1]) * t)
        b = int(top_rgb[2] + (bot_rgb[2] - top_rgb[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

def add_pattern(draw, w, h, base_color):
    """Add subtle diagonal stripe texture."""
    r, g, b = base_color
    stripe = (min(r+20,255), min(g+20,255), min(b+20,255), 30)
    img_rgba = Image.new("RGBA", (w, h), (0,0,0,0))
    d = ImageDraw.Draw(img_rgba)
    for x in range(-h, w, 30):
        d.line([(x, 0), (x + h, h)], fill=stripe, width=12)
    return img_rgba

for fname, name, season, emoji, top, bot in CROPS:
    img = Image.new("RGB", (W, H), top)
    draw = ImageDraw.Draw(img)
    make_gradient(draw, W, H, top, bot)

    # Overlay stripe texture
    pattern = add_pattern(draw, W, H, top)
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, pattern)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Dark semi-transparent overlay at bottom for text
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.rectangle([(0, H//2), (W, H)], fill=(0, 0, 0, 140))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Try to load a font, fallback to default
    try:
        font_big   = ImageFont.truetype("arial.ttf", 56)
        font_mid   = ImageFont.truetype("arial.ttf", 36)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except:
        try:
            font_big   = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 56)
            font_mid   = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 36)
            font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 24)
        except:
            font_big = font_mid = font_small = ImageFont.load_default()

    # Crop name (large, centered, lower portion)
    name_bbox = draw.textbbox((0, 0), name, font=font_big)
    nw = name_bbox[2] - name_bbox[0]
    draw.text(((W - nw) // 2, H - 110), name, font=font_big, fill=(255, 255, 255))

    # Season badge
    season_text = f"  {season} Season  "
    s_bbox = draw.textbbox((0, 0), season_text, font=font_small)
    sw = s_bbox[2] - s_bbox[0]
    sx = (W - sw) // 2
    draw.rounded_rectangle([sx - 6, H - 52, sx + sw + 6, H - 20],
                            radius=10, fill=(255,255,255,180))
    draw.text((sx, H - 50), season_text, font=font_small, fill=bot)

    # Decorative circles top-right
    draw.ellipse([(W-120, -60), (W+60, 120)],
                 fill=(min(top[0]+40,255), min(top[1]+40,255), min(top[2]+40,255)))
    draw.ellipse([(W-80, -30), (W+20, 70)],
                 fill=(min(top[0]+60,255), min(top[1]+60,255), min(top[2]+60,255)))

    path = os.path.join(OUTPUT_DIR, fname)
    img.save(path, "JPEG", quality=92)
    print(f"OK  {fname}")

print("All crop images generated successfully!")

#!/usr/bin/env python3
"""
Generate six favicon candidates (PNG preview and ICO multi-size).
Outputs to assets/favicons/fav{1..6}.png and fav{1..6}.ico
"""
import os
import importlib
from typing import Any

OUT_DIR = os.path.join("assets", "favicons")
SIZES = [(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]

# Defer Pillow import to runtime to avoid static import resolution issues
Image: Any = None
ImageDraw: Any = None

def load_pillow() -> None:
    global Image, ImageDraw
    try:
        Image = importlib.import_module("PIL.Image")
        ImageDraw = importlib.import_module("PIL.ImageDraw")
    except Exception as e:
        msg = (
            "Pillow 未安装或不可用。请在项目虚拟环境中执行:\n"
            "python3 -m venv .venv && . .venv/bin/activate && pip install pillow\n"
        )
        raise RuntimeError(msg) from e


def ensure_out_dir():
    os.makedirs(OUT_DIR, exist_ok=True)


def save_icon(base_img: Any, name: str):
    png_path = os.path.join(OUT_DIR, f"{name}.png")
    ico_path = os.path.join(OUT_DIR, f"{name}.ico")
    # Save PNG preview
    base_img.save(png_path, format="PNG")
    # Save ICO with multiple sizes
    base_img.save(ico_path, format="ICO", sizes=SIZES)


def draw_lightning(draw: Any, cx: int, cy: int, scale: int, color: tuple):
    # Simple lightning bolt polygon
    points = [
        (cx - 0 * scale, cy - 60 * scale),
        (cx - 20 * scale, cy - 20 * scale),
        (cx - 5 * scale, cy - 20 * scale),
        (cx - 30 * scale, cy + 30 * scale),
        (cx + 10 * scale, cy - 10 * scale),
        (cx - 5 * scale, cy - 10 * scale),
    ]
    draw.polygon(points, fill=color)


def icon1():
    # Blue circle + white lightning (techy)
    img = Image.new("RGBA", (256, 256), (20, 30, 60, 255))
    draw = ImageDraw.Draw(img)
    # Circle
    draw.ellipse((16, 16, 240, 240), fill=(50, 120, 255, 255))
    # Lightning
    draw_lightning(draw, 128, 120, 1, (255, 255, 255, 255))
    return img


def icon2():
    # Dark background + neon ring (modern)
    img = Image.new("RGBA", (256, 256), (18, 18, 22, 255))
    draw = ImageDraw.Draw(img)
    # Outer ring
    draw.ellipse((32, 32, 224, 224), outline=(0, 255, 200, 255), width=12)
    # Inner fill
    draw.ellipse((56, 56, 200, 200), fill=(10, 10, 14, 255))
    # Dot
    draw.ellipse((116, 116, 140, 140), fill=(0, 255, 200, 255))
    return img


def icon3():
    # Diagonal split + minimal mark
    img = Image.new("RGBA", (256, 256), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    # Diagonal
    draw.polygon([(0, 0), (256, 0), (0, 256)], fill=(30, 30, 34, 255))
    # Small square mark
    draw.rectangle((196, 196, 236, 236), fill=(60, 160, 255, 255))
    return img


def icon4():
    # Pixel heart (friendly)
    img = Image.new("RGBA", (256, 256), (248, 248, 248, 255))
    draw = ImageDraw.Draw(img)
    unit = 16
    heart_pixels = [
        (5, 3), (6, 3), (9, 3), (10, 3),
        (4, 4), (7, 4), (8, 4), (11, 4),
        (3, 5), (12, 5),
        (2, 6), (13, 6),
        (2, 7), (13, 7),
        (3, 8), (12, 8),
        (4, 9), (11, 9),
        (5,10), (10,10),
        (6,11), (9,11),
        (7,12), (8,12),
    ]
    for (x, y) in heart_pixels:
        draw.rectangle((x*unit, y*unit, (x+1)*unit, (y+1)*unit), fill=(230, 60, 90, 255))
    return img


def icon5():
    # Star on gradient
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    # simple vertical gradient
    base = Image.new("RGBA", (256, 256), (40, 60, 160, 255))
    top = Image.new("RGBA", (256, 256), (120, 80, 200, 255))
    mask = Image.linear_gradient("L").resize((256, 256))
    img = Image.composite(top, base, mask)
    draw = ImageDraw.Draw(img)
    # Star polygon
    pts = [
        (128, 40), (150, 100), (212, 100), (162, 140), (180, 200),
        (128, 168), (76, 200), (94, 140), (44, 100), (106, 100)
    ]
    draw.polygon(pts, fill=(255, 220, 80, 255))
    return img


def icon6():
    # Overlapping squares (clean)
    img = Image.new("RGBA", (256, 256), (245, 246, 250, 255))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((40, 40, 180, 180), radius=20, fill=(70, 140, 240, 255))
    draw.rounded_rectangle((76, 76, 216, 216), radius=20, fill=(20, 30, 60, 230))
    draw.rounded_rectangle((96, 96, 236, 236), radius=16, outline=(255, 255, 255, 255), width=8)
    return img


def main():
    load_pillow()
    ensure_out_dir()
    icons = [icon1(), icon2(), icon3(), icon4(), icon5(), icon6()]
    for i, img in enumerate(icons, start=1):
        save_icon(img, f"fav{i}")
    print(f"Generated {len(icons)} favicon candidates in {OUT_DIR}")


if __name__ == "__main__":
    main()
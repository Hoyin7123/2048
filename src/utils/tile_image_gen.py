from PIL import Image, ImageDraw, ImageFont

import sys
import math
import platform

SQUARE_SIZE = 90

SQUARE_COLORS = [
    (205, 193, 180),
    (238, 228, 218),
    (237, 224, 200),
    (242, 177, 121),
    (245, 149, 99),
    (246, 124, 95),
    (246, 94, 59),
    (237, 207, 114),
    (237, 204, 97),
    (237, 200, 80),
    (237, 197, 63),
    (237, 194, 46),
    (62, 57, 51)
]

sys_font = None

TEXT_SIZE = 30

TEXT_COLOR = (119, 110, 101)


def get_font():
    global sys_font
    system = sys.platform
    sys_font = "arial.ttf" if system in ("win32", "cygwin", "darwin") else "Arialbd.TTF" if system == "linux" else None


def generate_image(text: int) -> Image:
    get_font()

    if not sys_font:
        raise Exception(f"Your OS({platform.platform()}) is not supported lol.")

    if text == 0:
        return Image.new("RGB", (SQUARE_SIZE, SQUARE_SIZE), color=(255, 255, 255))

    power = int(math.log(text, 2))
    t = str(text)
    img = Image.new('RGB', (SQUARE_SIZE, SQUARE_SIZE), color=SQUARE_COLORS[power-1])
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(sys_font, TEXT_SIZE)
    text_width, text_height = font.getsize(t)

    d.text(xy=(SQUARE_SIZE/2 - text_width/2, SQUARE_SIZE/2 - text_height/2),
           text=t, fill=TEXT_COLOR,
           anchor="center",
           align="center",
           font=font)

    return img


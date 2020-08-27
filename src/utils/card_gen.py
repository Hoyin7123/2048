from PIL import Image, ImageDraw, ImageFont

import math

SQUARE_SIZE = 80

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

FONT = "arial.ttf"

TEXT_SIZE = 30


def generate_image(text: int):
    power = int(math.log(text, 2))
    img = Image.new('RGB', (SQUARE_SIZE, SQUARE_SIZE), color=SQUARE_COLORS[power-1])
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, TEXT_SIZE)

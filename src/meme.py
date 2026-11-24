"""Рисуем подпись на фото кота и отдаём готовый PNG в виде байтов."""

import io

from PIL import Image, ImageDraw, ImageFont

from config import FONT_PATH


def wrap(draw, text, font, max_width):
    """Разбиваем фразу на строки так, чтобы каждая влезала в max_width."""
    lines, current = [], ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def make_meme(image_path, text: str) -> bytes:
    image = Image.open(image_path).convert("RGB")
    image.thumbnail((1024, 1024))
    width, height = image.size

    size = max(24, width // 10)
    font = ImageFont.truetype(str(FONT_PATH), size)
    draw = ImageDraw.Draw(image)

    lines = wrap(draw, text, font, int(width * 0.9))
    line_height = int(size * 1.2)
    y = height - len(lines) * line_height - 20

    for line in lines:
        x = (width - draw.textlength(line, font=font)) / 2
        # Белый текст с чёрной обводкой читается и на светлом, и на тёмном фоне.
        draw.text(
            (x, y), line, font=font,
            fill="white", stroke_width=max(2, size // 12), stroke_fill="black",
        )
        y += line_height

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()

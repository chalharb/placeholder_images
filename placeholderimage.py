from PIL import Image, ImageFont, ImageDraw
from flask import Flask, send_file, render_template, request
import io


def convert_hex_to_rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))


def create_image(width, height, color, text, text_color):
    img = Image.new('RGB', (width, height), color=convert_hex_to_rgb(color))

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/sans-serif.ttf", 64)
    text_width, text_height = draw.textsize(text, font)

    draw.text(
        ((img.width - text_width) / 2, (height - text_height) / 2)
        , text, (convert_hex_to_rgb(text_color)), font=font)
    return img

def serve_image(img):
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG', quality=50)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

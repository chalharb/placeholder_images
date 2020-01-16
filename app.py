from flask import Flask, send_file, render_template, request
from PIL import Image, ImageFont, ImageDraw
import io

app = Flask('__name__')


def convert_hex_to_rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))


def create_image(width, height, color, text, text_color, font_size):
    img = Image.new('RGB', (width, height), color=convert_hex_to_rgb(color))

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/sans-serif.ttf", font_size)
    text_width, text_height = draw.textsize(text, font)

    draw.text(
        ((img.width - text_width) / 2, (height - text_height) / 2)
        , text, (convert_hex_to_rgb(text_color)), font=font)
    return img


def serve_image(img):
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG', quality=100)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@app.route('/image/')
def image_landing_page():
    img = create_image(400, 400, '0000FF', "Hello World", 'FAFAFA')
    return serve_image(img)


@app.route('/image/<int:size>')
def create_square_image(size):
    img = create_image(size, size, 'FAFAFA', "Image Placeholder", '000000')
    return serve_image(img)


@app.route('/image/<int:width>x<int:height>')
def create_image_with_width_height(width, height):
    background_color = request.args.get('bg')
    image_text = request.args.get('text')
    text_color = request.args.get('color')
    font_size = request.args.get('text-size')

    if background_color is None:
        background_color = 'FAFAFA'

    if image_text is None:
        image_text = 'Image Placeholder'

    if text_color is None:
        text_color = '000000'

    if font_size is None:
        font_size = 64

    img = create_image(width, height, background_color, image_text, text_color, font_size)
    return serve_image(img)


app.run()
from flask import Flask, send_file, render_template, request, Response
from placeholderimage import convert_hex_to_rgb, create_image, serve_image


app = Flask('__name__')


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

    img = create_image(width, height, background_color, image_text, text_color)
    return serve_image(img)


app.run()
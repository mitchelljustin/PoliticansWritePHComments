import os
import random
from db.generate import generate_comment
from flask import send_file, jsonify
from . import app

IMAGES_DIR = 'static/images'


@app.route('/')
def index():
    return send_file('../static/index.html')


@app.route('/generate')
def generate():
    image_choices = os.listdir(IMAGES_DIR)
    image_url = os.path.join(IMAGES_DIR, random.choice(image_choices))
    comment = generate_comment()
    return jsonify(
        image=image_url,
        comment=comment,
    )

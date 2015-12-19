import json

import os
import random
from core.generate_comment import generate_pornhub_comment
from flask import send_file, jsonify
from . import app


@app.route('/')
def index():
    return send_file('../static/index.html')


comments_json = None

IMAGES_DIR = 'static/images'


@app.route('/generate')
def generate():
    image_choices = os.listdir(IMAGES_DIR)
    image_url = os.path.join(IMAGES_DIR, random.choice(image_choices))
    global comments_json
    if not comments_json:
        comments_json = json.load(open('static/comments.json'))
    quote = generate_pornhub_comment(
        markov_dict=comments_json['prefix_dict'],
        prefix_len=comments_json['prefix_len'],
        blacklist=comments_json['comments'],
    )
    return jsonify(
        image=image_url,
        quote=quote,
    )

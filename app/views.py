import json

from core.generate_comment import generate_pornhub_comment
from flask import send_file
from . import app


@app.route('/')
def index():
    return send_file('../static/index.html')


comments_json = None


@app.route('/gen_quote')
def gen_quote():
    global comments_json
    if not comments_json:
        comments_json = json.load(open('static/comments.json'))
    quote = generate_pornhub_comment(
        markov_dict=comments_json['prefix_dict'],
        prefix_len=comments_json['prefix_len'],
        blacklist=comments_json['comments'],
    )
    return quote

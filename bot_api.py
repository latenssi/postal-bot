# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from flask import Flask, request, json
from PostalBot import PostalBot

app = Flask(__name__)
bot = PostalBot(os.getenv('BOT_TG_API_KEY'), os.getenv('TG_LOUNGE_ID'))

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello world!'

def handle_json_request(r, call_f, return_f):
    try:
        data = json.loads(r.data)
    except ValueError:
        return '', 400
    return return_f(call_f(data))

@app.route('/telegram/update', methods=['POST'])
def telegram_update():
    return handle_json_request(request, bot.handle_tg_update, lambda x: x)

@app.route('/stream/publish', methods=['POST'])
def stream_publish():
    return handle_json_request(request, bot.handle_stream_publish, lambda x: x)

@app.route('/postal/new-post', methods=['POST'])
def postal_new_post():
    return handle_json_request(request, bot.handle_postal_new_post, lambda x: x)


if __name__ == '__main__':
    app.run(debug=True)

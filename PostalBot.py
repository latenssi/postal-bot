# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import humanize
from requests import request
from werkzeug.contrib.cache import SimpleCache


STR_USERNAME = 'USERNAME'
STR_MESSAGE_SENT = "Message sent"

class PostalBot(object):

    def __init__(self, tg_api_key, tg_lounge_id):
        self.tg_api_key = tg_api_key
        self.tg_lounge_id = tg_lounge_id
        self.cache = SimpleCache()

    def send_tg_message(self, chat_id, text):
        request('get', 'https://api.telegram.org/bot{api_key}/sendMessage?chat_id={chat_id}&text={text}'.format(
            api_key=self.tg_api_key,
            chat_id=chat_id,
            text=text
        ))

    def handle_stream_publish(self, data):
        keys = data.keys()
        if 'watch_url' in keys and 'username' in keys:
            c_key = STR_USERNAME + ':' + data['username']
            if not self.cache.get(c_key):
                message = '{username} went live on Postal\n{url}'.format(
                    username=data['username'],
                    url=data['watch_url']
                )
                self.send_tg_message(self.tg_lounge_id, message)
                self.cache.set(c_key, True, timeout=10*60)
                return STR_MESSAGE_SENT
        return ''

    def handle_postal_new_post(self, data):
        keys = data.keys()
        if 'username' in keys and 'title' in keys:
            message = "New post by {username}\n{title}".format(
                username=data['username'],
                title=data['title']
            )

            if 'image_url' in keys and 'image_size' in keys:
                message += "\n{url} {size}".format(
                    url=data['image_url'],
                    size=humanize.naturalsize(data['image_size'], gnu=True)
                )

            if 'file_url' in keys and 'file_size' in keys:
                message += "\n{url} {size}".format(
                    url=data['file_url'],
                    size=humanize.naturalsize(data['file_size'], gnu=True)
                )

            self.send_tg_message(self.tg_lounge_id, message)
            return STR_MESSAGE_SENT
        return ''

    def handle_tg_update(self, data):
        keys = data.keys()

        if 'message' in keys:
            self.handle_tg_message(data['message'])
        return ''

    def handle_tg_message(self, message):
        # print "%s %s: %s" % (message['from']['first_name'], message['from']['last_name'], message['text'])
        pass

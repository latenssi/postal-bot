# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import json
import unittest
import bot_api


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = bot_api.app.test_client()
        bot_api.app.config['TESTING'] = True

    def test_index(self):
        rv = self.app.get('/')
        assert rv.data == 'Hello world!'
        rv = self.app.post('/')
        assert rv.status_code == 405

    def test_empty_telegram_update(self):
        rv = self.app.get('/telegram/update')
        assert rv.status_code == 405
        rv = self.app.post('/telegram/update')
        assert rv.status_code == 400

    def test_empty_stream_publish(self):
        rv = self.app.get('/stream/publish')
        assert rv.status_code == 405
        rv = self.app.post('/stream/publish')
        assert rv.status_code == 400

    def test_empty_postal_new_post(self):
        rv = self.app.get('/postal/new-post')
        assert rv.status_code == 405
        rv = self.app.post('/postal/new-post')
        assert rv.status_code == 400

    def test_proper_telegram_update(self):
        data = {
            "update_id": 135497311,
            "message": {
                "message_id": 75,
                "from": {
                    "id": 1234,
                    "first_name": "Test",
                    "last_name": "User",
                    "username": "testuser"
                },
                "chat": {
                    "id": 12345,
                    "first_name": "Test",
                    "last_name": "User",
                    "username": "testuser"
                },
                "date": 1435524799,
                "text": "test"
            }
        }
        rv = self.app.post('/telegram/update', data=json.dumps(data))
        assert rv.status_code == 200

    def test_proper_stream_publish(self):
        data = {
            'username': 'testuser',
            'watch_url': 'http://www.example.com/stream/testuser'
        }
        rv = self.app.post('/stream/publish', data=json.dumps(data))
        assert rv.status_code == 200

    def test_proper_postal_new_post(self):
        data = {
            "username": "testuser",
            "image_size": 23086,
            "image_url": "http://www.example.com/posts/1238ujsfdj984324123ffg43.jpg",
            "image_name": "35_hauki1.jpg",
            "title": "Test"
        }
        rv = self.app.post('/postal/new-post', data=json.dumps(data))
        assert rv.status_code == 200
        data = {
            "username": "testuser",
            "file_size": 23086,
            "file_url": "http://www.example.com/posts/1238ujsfdj984324123ffg43.jpg",
            "file_name": "35_hauki1.jpg",
            "title": "Test"
        }
        rv = self.app.post('/postal/new-post', data=json.dumps(data))
        assert rv.status_code == 200
        data = {
            "username": "testuser",
            "file_size": 23086,
            "file_url": "http://www.example.com/posts/1238ujsfdj984324123ffg43.jpg",
            "file_name": "35_hauki1.jpg",
            "image_size": 23086,
            "image_url": "http://www.example.com/posts/1238ujsfdj984324123ffg43.jpg",
            "image_name": "35_hauki1.jpg",
            "title": "Test"
        }
        rv = self.app.post('/postal/new-post', data=json.dumps(data))
        assert rv.status_code == 200

    def test_stream_publish_spam_prevention(self):
        data = {
            'username': 'testuser',
            'watch_url': 'http://www.example.com/stream/testuser'
        }
        rv = self.app.post('/stream/publish', data=json.dumps(data))
        rv = self.app.post('/stream/publish', data=json.dumps(data))
        assert rv.data == ''
        assert rv.status_code == 200

if __name__ == '__main__':
    unittest.main()
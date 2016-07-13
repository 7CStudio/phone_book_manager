# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
import calendar

from flask import url_for, json, current_app
from phone_book_manager import db

import pytest
import status


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        db.session.commit()
        db.create_all()

    def tearDown(self):
        db.session.commit()
        db.drop_all()


@pytest.mark.usefixtures('client_class')
class TestAPI(BaseTestCase):
    def make_post(self, url, data, with_auth=False):
        if with_auth:
            return self.client.post(url,
                                    data=json.dumps(data),
                                    content_type="application/json",
                                    headers={'Authorization': 'Token: {}'.format(  # noqa
                                        self.access_token)})
        else:
            app_token = current_app.config['APP_TOKEN']
            return self.client.post(url,
                                    data=json.dumps(data),
                                    content_type="application/json",
                                    headers={'Authorization': 'Token: {}'.format(  # noqa
                                        app_token)})

    def create_user(self):
        d = datetime.utcnow()
        unix_time = calendar.timegm(d.utctimetuple())
        self.access_token = str(unix_time)
        data = {'phone': unix_time, 'access_token': self.access_token}
        return self.make_post(url_for('api.user'), data=data)

    def test_user_api_with_improper_token(self):
        self.access_token = '123'
        d = datetime.utcnow()
        unix_time = calendar.timegm(d.utctimetuple())
        self.access_token = str(unix_time)
        data = {'phone': unix_time, 'access_token': self.access_token}
        resp = self.make_post(url_for('api.user'), data=data, with_auth=True)

        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_user_api(self):
        resp = self.create_user()
        assert resp.status_code == status.HTTP_201_CREATED

    def test_duplicate_user_api_post(self):
        resp = self.create_user()
        data = {'phone': resp.json['phone'],
                'access_token': resp.json['access_token']}
        return self.make_post(url_for('api.user'), data=data)
        assert resp.status_code == status.HTTP_200_OK

    def test_check_api(self):
        self.create_user()
        data = {'contacts': [{'phone': '+911234', 'name': 'Walter'}]}
        resp = self.make_post(url_for('api.sync'), data=data,
                              with_auth=True)

        contacts = data['contacts']
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json[0]['is_user'] is False
        assert resp.json[0]['phone'] == contacts[0]['phone']

    def test_check_api_with_improper_token(self):
        self.create_user()
        data = {'contacts': [{'phone': '+911234', 'name': 'Walter'}]}
        resp = self.make_post(url_for('api.sync'), data=data,
                              with_auth=False)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_check_api_with_empty_contacts(self):
        self.create_user()
        data = {'contacts': []}
        resp = self.make_post(url_for('api.sync'), data=data,
                              with_auth=True)

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert resp.json == {'error': '`contacts` field is required'}

    def test_check_api_without_body(self):
        self.create_user()
        resp = self.make_post(url_for('api.sync'), data={},
                              with_auth=True)

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert resp.json == {'error': 'No JSON found'}

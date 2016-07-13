# -*- coding: utf-8 -*-

from flask import Blueprint

import status

from .utils import (HTTPException, make_response, get_request_data,
                    validate_or_raise)
from .base_views import BaseAPIView
from .validators import SyncValidator, UserValidator

from . import services
from . import formatter

api = Blueprint('api', import_name='api', url_prefix='/api/v1/phonebook')


class SyncAPIView(BaseAPIView):
    def post(self):
        try:
            self.authenticate()
            self.validate_data()
            contacts = services.sync_contacts(
                user_id=self.user.id,
                contacts=self.validator.contacts)
            return self.format_response(contacts)
        except HTTPException as e:
            return make_response(data=e.data, status=e.status)

    def validate_data(self):
        data = get_request_data()
        self.validator = validate_or_raise(SyncValidator, data)

    def format_response(self, contacts):
        resp = []
        for contact in contacts:
            d = {'name': contact.name, 'phone': contact.phone}
            if contact.user_id:
                d['is_user'] = True
            else:
                d['is_user'] = False
            resp.append(d)
        return make_response(status=status.HTTP_200_OK, data=resp)


class UserAPIView(BaseAPIView):
    def post(self):
        try:
            self.authenticate_app()
            self.validate_data()
            user, is_created = services.get_or_create_user(
                access_token=self.validator.access_token,
                phone=self.validator.phone)
            data = formatter.format_user(user)
            if is_created:
                return make_response(status=status.HTTP_201_CREATED, data=data)
            return make_response(status=status.HTTP_200_OK, data=data)
        except HTTPException as e:
            return make_response(data=e.data, status=e.status)

    def validate_data(self):
        data = get_request_data()
        self.validator = validate_or_raise(UserValidator, data)


api.add_url_rule(
    '/sync',
    view_func=SyncAPIView.as_view('sync'))
api.add_url_rule(
    '/user',
    view_func=UserAPIView.as_view('user'))

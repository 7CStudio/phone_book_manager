# -*- coding: utf-8 -*-

from flask import request, current_app
from flask.views import MethodView

import status

from .utils import get_token, HTTPException
from . import services


class AuthMixin:
    def authenticate(self):
        token = get_token()
        self.user = services.get_user_by_access_token(
            access_token=token)
        if not self.user:
            raise HTTPException(status=status.HTTP_401_UNAUTHORIZED)

    def authenticate_app(self):
        token = get_token()
        if token != current_app.config['APP_TOKEN']:
            raise HTTPException(status=status.HTTP_403_FORBIDDEN)


class BaseAPIView(MethodView, AuthMixin):
    def dispatch_request(self, *args, **kwargs):
        method = request.method
        meth = getattr(self, method.lower(), None)
        assert meth is not None, 'Unimplemented method %r' % method

        resp = meth(*args, **kwargs)
        return resp

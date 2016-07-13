# -*- coding: utf-8 -*-

from flask import Response, json, request

from schematics.exceptions import ModelConversionError, ModelValidationError
import status


class HTTPException(Exception):
    """Wrapper to raise all 4XX exception at the bottom level
    """
    def __init__(self, status, data=None, *args, **kwargs):
        super(HTTPException, self).__init__(*args, **kwargs)
        self.data = data or {}
        self.status = status


def make_response(data=None, status=200):
    """Create JSON Response to the user with data and status code.
    """
    if data is None:
        data = {}
    return Response(status=status, response=json.dumps(data),
                    mimetype="application/json")


def get_token():
    token = request.headers.get('Authorization')

    if not token:
        raise HTTPException(status=status.HTTP_403_FORBIDDEN)

    if 'Token' in token:
        token = token.split('Token:')[-1].strip()

    return token


def validate_or_raise(validator, data):
    try:
        obj = validator(data)
        obj.validate()
        return obj
    except ModelConversionError as e:
        message = get_validation_error_message(e.messages)
        raise HTTPException(status=422, data={'error': message})
    except ModelValidationError as e:
        message = get_validation_error_message(e.messages)
        raise HTTPException(status=400, data={'error': message})


def get_validation_error_message(message):
    if isinstance(message, basestring):
        return message
    elif isinstance(message, list) and message:
        return message[0]
    elif isinstance(message, dict):
        _, message = message.popitem()
        return get_validation_error_message(message)
    else:
        return None


def get_request_data():
    data = request.get_json()
    if not data:
        raise HTTPException(status=status.HTTP_400_BAD_REQUEST,
                            data={'error': 'No JSON found'})
    return data

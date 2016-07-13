# -*- coding: utf-8 -*-


USER_FIELDS = ['id', 'access_token', 'phone']


def formatter(obj, allowed_keys):
    """Pull attributes from objects and convert to camelCase
    """
    data = {}
    for key in allowed_keys:
        val = getattr(obj, key, None)
        data[key] = val
    return data


def format_user(user):
    return formatter(user, USER_FIELDS)

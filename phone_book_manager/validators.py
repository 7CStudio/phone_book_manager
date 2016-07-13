# -*- coding: utf-8 -*-

from schematics.models import Model
from schematics.types import StringType
from schematics.types.compound import ModelType, ListType

HANDLE_MESSAGES = {'min_length': 'Minimum 1 record is required',
                   'max_length': 'Exceeded max length of 20'}


class UserValidator(Model):
    access_token = StringType(max_length=30, min_length=2, required=True)
    phone = StringType(max_length=15)


class PhoneValidator(Model):
    name = StringType(required=True)
    phone = StringType(max_length=15, min_length=3,
                       required=True,
                       validators=[lambda val: val.strip()])


class SyncValidator(Model):
    contacts = ListType(ModelType(PhoneValidator))

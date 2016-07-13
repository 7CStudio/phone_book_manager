# -*- coding: utf-8 -*-

from app import get_default_settings
from phone_book_manager import create_app


import os

settings_file = os.environ.setdefault("APP_CONFIG", get_default_settings())


application = create_app(settings_file)

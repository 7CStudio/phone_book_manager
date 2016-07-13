# -*- coding: utf-8 -*-

import os

import pytest

from app import create_app


@pytest.fixture
def app():
    cwd = os.getcwd()
    app_env_config = cwd + os.path.sep + 'instance/settings.py'
    app = create_app(app_env_config)
    return app

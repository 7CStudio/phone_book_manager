# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config):
    global db
    app = Flask(__name__)
    app.config.from_pyfile(config)
    db.init_app(app)
    db.app = app
    from .v1_views import api  # noqa
    app.register_blueprint(api)
    return app

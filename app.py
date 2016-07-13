# -*- coding: utf-8 -*-

import os

from phone_book_manager import create_app, db


if __name__ == "__main__":
    cwd = os.getcwd()
    app_env_config = cwd + os.path.sep + 'instance/settings.py'
    config_file = os.environ.get('APP_CONFIG', app_env_config)
    app = create_app(config=config_file)
    db.create_all()
    app.run(host='0.0.0.0', debug=True, port=3000)

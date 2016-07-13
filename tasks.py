# -*- coding: utf-8 -*-

import os
from invoke import task


@task
def clean(ctx):
    ctx.run("rm -rf **/*.pyc")


@task
def test(ctx, pdb=False):
    cmd = "py.test -v -s"
    if pdb:
        cmd += ' --pdb'
    ctx.run(cmd, pty=True)
    ctx.run("py.test --cov-report term-missing --cov=phone_book_manager test_api.py")  # noqa
    ctx.run('flake8 .')


@task
def create_schema(ctx):
    from phone_book_manager import create_app, db
    from app import get_default_settings

    os.environ['SQLALCHEMY_ECHO'] = 'True'
    create_app(get_default_settings())
    db.create_all()

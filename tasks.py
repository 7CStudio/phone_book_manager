# -*- coding: utf-8 -*-

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

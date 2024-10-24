"""
PastForward login (main) view.

URLs include:

"""
import flask
import PastForward
from flask import url_for, request
import uuid
import hashlib

PastForward.app.secret_key = (
    b'\x97d\xb7\x81W\xb2\x8b~\x03\xbc\xb4\x88\xa2\x89\x89\x9d('
    b'\x8b\x85\xc2\x13\xb5\x86\x10'
)


@PastForward.app.route('/accounts/login/')
def show_login():
    """Render login template."""
    return flask.render_template("login.html")

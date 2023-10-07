"""
Insta485 create (main) view.

URLs include:
/accounts/create/

"""
import flask
import insta485
from flask import url_for
import uuid
import hashlib
import pathlib
from flask import abort


@insta485.app.route('/accounts/create/', methods=['GET', 'POST'])
def show_create():
    """Render template for create page."""
    if 'logname' in flask.session:
        return flask.redirect(url_for('show_edit'))
    else:
        return flask.render_template("create.html", **context)

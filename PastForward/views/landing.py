"""
PastForward create (main) view.

URLs include:
/accounts/landing/

"""
import flask
import PastForward
from flask import url_for
import uuid
import hashlib
import pathlib
from flask import abort


@PastForward.app.route('/landing/', methods=['GET', 'POST'])
def show_landing():
    """Render template for landing page."""
    if 'logname' in flask.session:
        return flask.redirect(url_for('show_explore'))
    else:
        context = {}
        return flask.render_template("landing.html", **context)
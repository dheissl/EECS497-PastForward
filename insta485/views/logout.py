"""
Insta485 logout (main) view.

URLs include:

"""
import flask
import insta485
from flask import url_for


@insta485.app.route('/accounts/logout/', methods=['POST'])
def show_logout():
    """POST: log out of session and go to login page."""
    if 'logname' not in flask.session:
        return flask.redirect(url_for('show_login'))
    flask.session.clear()
    return flask.redirect(flask.url_for('show_login'))

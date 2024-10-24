"""
PastForward logout (main) view.

URLs include:

"""
import flask
import PastForward
from flask import url_for


@PastForward.app.route('/accounts/logout/', methods=['POST'])
def show_logout():
    """POST: log out of session and go to login page."""
    if 'logname' not in flask.session:
        return flask.redirect(url_for('show_login'))
    flask.session.clear()
    return flask.redirect(flask.url_for('show_login'))

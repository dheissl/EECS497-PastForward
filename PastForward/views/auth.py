"""
PastForward auth (main) view.

URLs include:

"""
import flask
import PastForward
from flask import url_for
from flask import abort


@PastForward.app.route('/accounts/auth/')
def show_auth():
    """Show auth for  aws."""
    if 'logname' not in flask.session:
        abort(403)
    return ""

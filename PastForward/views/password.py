"""
PastForward password (main) view.

URLs include:

"""
import flask
import PastForward
from flask import url_for
from flask import abort


@PastForward.app.route('/accounts/password/', methods=['GET', 'POST'])
def show_password():
    """Render template password."""
    if 'logname' not in flask.session:
        return flask.redirect(url_for('show_login'))
    context = {}
    context["logname"] = flask.session['logname']
    return flask.render_template("password.html", **context)

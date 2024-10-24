"""
PastForward delete (main) view.

URLs include:

"""
import flask
import PastForward
from flask import url_for
from flask import abort


@PastForward.app.route('/accounts/delete/', methods=['GET', 'POST'])
def show_delete():
    """Render template for delate page."""
    if 'logname' not in flask.session:
        return flask.redirect(url_for('show_login'))
    username = flask.session['logname']
    context = {}
    context["logname"] = username
    return flask.render_template("delete.html", **context)

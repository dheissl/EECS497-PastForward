"""
PastForward edit (main) view.

URLs include:

"""
import flask
import pathlib
import uuid
import PastForward
from flask import url_for
from flask import abort


@PastForward.app.route('/accounts/edit/')
def show_edit():
    """Render template for edit."""
    if 'logname' not in flask.session:
        return flask.redirect(url_for('show_login'))

    connection = PastForward.model.get_db()

    logname = flask.session['logname']
    log = connection.execute(
        "SELECT username, filename, fullname, email "
        "FROM users "
        "WHERE username = ? ",
        (logname, )
    )
    users = log.fetchone()
    context = {}
    context["filename"] = users["filename"]
    context["username"] = users["username"]
    context["fullname"] = users["fullname"]
    context["email"] = users["email"]
    context["logname"] = logname

    return flask.render_template("edit.html", **context)

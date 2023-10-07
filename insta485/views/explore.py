"""
Insta485 explore (main) view.

URLs include:

"""
import flask
import insta485
from flask import url_for


@insta485.app.route('/explore/')
def show_explore():
    """Display /explore/ route."""
    if 'logname' not in flask.session:
        return flask.redirect(url_for('show_login'))

    # Connect to database
    connection = insta485.model.get_db()

    logname = flask.session['logname']

    ing = connection.execute(
        "SELECT u.username, u.filename AS profile_picture "
        "FROM users u "
        "WHERE u.username != ? "
        "AND u.username NOT IN ("
        "SELECT f.username2 "
        "FROM following f "
        "WHERE f.username1 = ?)",
        (logname, logname,)
    )
    not_following = ing.fetchall()
    # Add database info to context
    context = {"not_following": not_following}
    context["logname"] = logname
    return flask.render_template("explore.html", **context)

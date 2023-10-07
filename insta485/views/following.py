"""
Insta485 following (main) view.

URLs include:

"""
import flask
import insta485
import arrow
from flask import url_for


@insta485.app.route('/users/<username>/following/')
def show_following(username):
    """Display /users/<user_url_slug>/following/ route."""
    if 'logname' not in flask.session:
        return flask.redirect(url_for('show_login'))

    logname = flask.session['logname']
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    wing = connection.execute(
        "SELECT u.username, u.filename AS profile_picture "
        "FROM users AS u "
        "JOIN following AS f ON u.username = f.username2 "
        "WHERE f.username1 = ? ",
        (username, )
    )
    following = wing.fetchall()

    fol = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 = ?",
        (logname, )
    )
    followers = fol.fetchall()

    follownames = []
    for follow in followers:
        follownames.append(follow["username2"])
    for follow in following:
        if follow["username"] in follownames:
            follow["user_follows"] = True
        else:
            follow["user_follows"] = False

    # Add database info to context
    context = {"following": following}
    context["logname"] = logname
    context["username"] = username
    return flask.render_template("following.html", **context)

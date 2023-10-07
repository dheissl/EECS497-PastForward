"""
Insta485 followers (main) view.

URLs include:

"""
import flask
import insta485
import arrow
from flask import url_for


@insta485.app.route('/users/<username>/followers/')
def show_followers(username):
    """Display /users/<user_url_slug>/followers/ route."""
    if 'logname' not in flask.session:
        return flask.redirect(url_for('show_login'))
    logname = flask.session['logname']
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    ing = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 = ?",
        (logname, )
    )
    following = ing.fetchall()

    wer = connection.execute(
        "SELECT u.username, u.filename AS profile_picture "
        "FROM users AS u "
        "JOIN following AS f ON u.username = f.username1 "
        "WHERE f.username2 = ?",
        (username, )
    )
    followers = wer.fetchall()
    follownames = []
    for follow in following:
        follownames.append(follow["username2"])
    for follower in followers:
        if follower["username"] in follownames:
            follower["following"] = True
        else:
            follower["following"] = False

    # Add database info to context
    context = {"followers": followers}
    context["logname"] = logname
    context["username"] = username
    return flask.render_template("followers.html", **context)

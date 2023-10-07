"""
Insta485 users (main) view.

URLs include:
/users
"""
import flask
import insta485
from flask import url_for


@insta485.app.route('/users/<username>/')
def show_user(username):
    """Render template for user page."""
    if 'logname' not in flask.session:
        return flask.redirect(url_for('show_login'))

    """Display /users route."""

    # Connect to database
    connection = insta485.model.get_db()

    # Query database

    logname = flask.session['logname']

    log = connection.execute(
        "SELECT username, fullname "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    users = log.fetchall()

    wing = connection.execute(
        "SELECT username1 "
        "FROM following "
        "WHERE username1 = ? ",
        (username, )
    )
    following = wing.fetchall()

    wers = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username2 = ? ",
        (username, )
    )
    followers = wers.fetchall()

    lf = connection.execute(
        "SELECT username1, username2 "
        "FROM following "
        "WHERE username1 = ? AND username2 = ? ",
        (logname, username)
    )
    logfol = lf.fetchone()

    pos = connection.execute(
        "SELECT postid, filename "
        "FROM posts "
        "WHERE owner = ?",
        (username, )
    )
    posts = pos.fetchall()

    for user in users:
        user["total_following"] = 0
        user["total_followers"] = 0
        user["logname_follows"] = False
        user["total_posts"] = 0
        user["posts"] = []
        if logfol:
            user["logname_follows"] = True
        for follow in following:
            user["total_following"] += 1
        for follows in followers:
            user["total_followers"] += 1
        for post in posts:
            user["total_posts"] += 1
            user["posts"].append(
                {"postid": post["postid"], "filename": post["filename"]})

    # Add database info to context
    context = {"users": users}
    context["logname"] = logname
    context["username"] = username
    return flask.render_template("user.html", **context)

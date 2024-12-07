"""
PastForward users (main) view.

URLs include:
/users
"""
import flask
import PastForward
from flask import url_for
import datetime
from datetime import datetime, date


@PastForward.app.route('/users/<username>/')
def show_user(username):
    """Render template for user page."""
    if 'logname' not in flask.session:
        return flask.redirect(url_for('show_login'))

    """Display /users route."""

    # Connect to database
    connection = PastForward.model.get_db()

    # Query database

    logname = flask.session['logname']

    log = connection.execute(
        "SELECT username, fullname, filename "
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
        "SELECT postid, filename, scheduled_date "
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
            if post["scheduled_date"] is not None:
                post["scheduled_date"] = datetime.strptime(post["scheduled_date"], "%Y-%m-%d").date()
            user["total_posts"] += 1
            user["posts"].append(
                {"postid": post["postid"], "filename": post["filename"], "scheduled_date": post["scheduled_date"]})

    # Add database info to context
    context = {"users": users}
    context["logname"] = logname
    context["username"] = username
    return flask.render_template("user.html", **context, current_date=date.today())

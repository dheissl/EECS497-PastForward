"""
PastForward index (main) view.

URLs include:
/
"""
import flask
import PastForward
import arrow
from flask import url_for


@PastForward.app.route('/')
def show_index():
    """Render template for index page."""
    if 'logname' not in flask.session:
        return flask.redirect(url_for('show_landing'))
    """Display / route."""
    logname = flask.session['logname']
    # Connect to database
    connection = PastForward.model.get_db()
    followerurl = url_for('show_followers', username=logname)
    # Query database
    cur = connection.execute(
        "SELECT p.filename AS pic, p.owner AS owner, p.postid AS postid,"
        " p.created AS timestamp, u.filename AS profile_pic "
        "FROM posts AS p "
        "JOIN following AS f ON p.owner = f.username2 "
        "JOIN users AS u ON p.owner = u.username "
        "WHERE f.username1 = ? "
        "UNION "
        "SELECT p.filename AS pic, p.owner AS owner, p.postid AS postid,"
        " p.created AS timestamp, u.filename AS profile_pic "
        "FROM posts AS p "
        "JOIN users AS u ON p.owner = u.username "
        "WHERE p.owner = ?",
        (logname, logname,)
    )
    posts = cur.fetchall()

    lik = connection.execute(
        "SELECT owner, postid "
        "FROM likes"
    )
    likes = lik.fetchall()

    com = connection.execute(
        "SELECT owner, postid, text "
        "FROM comments"
    )
    comments = com.fetchall()
    for post in posts:
        time = arrow.get(post["timestamp"])
        post["timestamp"] = time.humanize()

        post["likes"] = 0
        post["liked"] = False
        post["comments"] = []
        for like in likes:
            if post["postid"] == like["postid"]:
                if like["owner"] == logname:
                    post["liked"] = True
                post["likes"] += 1
        for comment in comments:
            if comment["postid"] == post["postid"]:
                post["comments"].append({"owner": comment["owner"],
                                        "text": comment["text"]})

    # Add database info to context
    context = {"posts": posts}
    context["logname"] = logname
    return flask.render_template("index.html", **context)

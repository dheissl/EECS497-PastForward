"""
PastForward followers (main) view.

URLs include:

"""
import flask
import PastForward
import arrow
from flask import url_for


@PastForward.app.route('/posts/<postid>/')
def show_posts(postid):
    """Display /posts/<postid>/ route."""
    if 'logname' not in flask.session:
        return flask.redirect(url_for('show_login'))

    logname = flask.session['logname']
    # Connect to database
    connection = PastForward.model.get_db()
    usrurl = url_for('show_user', username=logname)
    # Query database
    cur = connection.execute(
        "SELECT p.filename AS pic, p.owner AS owner, p.postid AS postid,"
        " p.created AS timestamp, u.filename AS profile_pic "
        "FROM posts AS p "
        "JOIN users AS u ON p.owner = u.username "
        "WHERE p.postid = ? ",
        (postid,)
    )
    posts = cur.fetchall()

    lik = connection.execute(
        "SELECT owner, postid "
        "FROM likes "
        "WHERE postid = ?",
        (postid,)
    )
    likes = lik.fetchall()

    com = connection.execute(
        "SELECT owner, postid, text, commentid "
        "FROM comments "
        "WHERE postid = ?",
        (postid,)
    )
    comments = com.fetchall()
    for post in posts:
        time = arrow.get(post["timestamp"])
        post["timestamp"] = time.humanize()

        post["likes"] = 0
        post["comments"] = []
        post["liked"] = False
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
    context = {"posts": posts, "logname": logname}
    context["user_url"] = usrurl
    context["postid"] = postid
    return flask.render_template("post.html", **context)

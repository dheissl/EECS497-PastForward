"""
PastForward logout (main) view.

URLs include:

"""
import flask
import PastForward
from flask import url_for, request, abort, redirect


@PastForward.app.route('/likes/', methods=['POST'])
def handle_likes():
    """POST likes like and unlike."""
    if 'logname' not in flask.session:
        return flask.redirect(url_for('show_login'))
    logname = flask.session['logname']
    connection = PastForward.model.get_db()
    # Get the operation and postid from the form data
    operation = request.form.get('operation')
    postid = request.form.get('postid')

    # Get the current URL or use '/' as the default
    target_url = request.args.get('target', '/')

    lik = connection.execute(
        "SELECT owner "
        "FROM likes "
        "WHERE postid = ?",
        (postid,)
    )
    li = lik.fetchall()
    likes = []
    for like in li:
        likes.append(like["owner"])

    # Check if the user has already liked the post or not
    if operation == 'like':
        if logname in likes:
            abort(409, 'User already liked this post')
        else:
            connection.execute(
                "INSERT INTO likes (owner, postid) "
                "VALUES (?, ?)",
                (logname, postid,)
            )
    elif operation == 'unlike':
        if logname not in likes:
            abort(409, 'User has not liked this post')
        else:
            connection.execute(
                "DELETE FROM likes "
                "WHERE owner = ? AND postid = ?",
                (logname, postid,)
            )

    # Redirect to the specified target URL
    return redirect(target_url)

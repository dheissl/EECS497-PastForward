"""
Insta485 logout (main) view.

URLs include:

"""
import flask
import insta485
from flask import url_for, request, abort, redirect


@insta485.app.route('/comments/', methods=['POST'])
def handle_comments():
    """Handle comments."""
    if 'logname' not in flask.session:
        return flask.redirect(url_for('show_login'))
    logname = flask.session['logname']
    connection = insta485.model.get_db()
    # Get the operation, postid, commentid, and text from the form data
    operation = request.form.get('operation')
    postid = request.form.get('postid')
    commentid = request.form.get('commentid')
    text = request.form.get('text')

    # Get the current URL or use '/' as the default
    target_url = request.args.get('target', '/')

    if operation == 'create':
        # Check if the comment text is empty
        if not text:
            abort(400, 'Comment text cannot be empty')

        # Create a new comment
        connection.execute(
            "INSERT INTO comments(owner, postid, text) "
            "VALUES (?, ?, ?)",
            (logname, postid, text)
        )

    elif operation == 'delete':
        com = connection.execute(
            "SELECT owner "
            "FROM comments "
            "WHERE commentid = ?",
            (commentid,)
        )
        comments = com.fetchall()

        # Check if the user owns the comment
        if comments[0]['owner'] != logname:
            abort(403, 'You do not have permission to delete this comment')

        # Delete the comment
        else:
            connection.execute(
                "DELETE FROM comments "
                "WHERE commentid = ?",
                (commentid,)
            )

    # Redirect to the specified target URL
    return redirect(target_url)

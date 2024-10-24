"""
PastForward logout (main) view.

URLs include:

"""
import flask
import PastForward
from flask import url_for, request, abort, redirect


@PastForward.app.route('/following/', methods=['POST'])
def handle_follows():
    """POST accounts for create, delete, edit, login, and update_password."""
    if 'logname' not in flask.session:
        return flask.redirect(url_for('show_login'))
    logname = flask.session['logname']
    connection = PastForward.model.get_db()
    # Get the operation and postid from the form data
    operation = request.form.get('operation')
    username = request.form.get('username')

    # Get the current URL or use '/' as the default
    target_url = request.args.get('target', '/')

    lik = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 = ?",
        (logname,)
    )
    foll = lik.fetchall()
    print(foll)
    following = []
    for follow in foll:
        following.append(follow['username2'])

    # Check if the user has already liked the post or not
    if operation == 'follow':
        if username in following:
            abort(409, 'User already follows them')
        else:
            connection.execute(
                "INSERT INTO following(username1, username2) VALUES"
                "(?, ?)",
                (logname, username,)
            )
    elif operation == 'unfollow':
        if username not in following:
            abort(409, 'User does not follow them')
        else:
            connection.execute(
                "DELETE FROM following "
                "WHERE username1 = ? AND username2 = ?",
                (logname, username,)
            )

    # Redirect to the specified target URL
    return redirect(target_url)

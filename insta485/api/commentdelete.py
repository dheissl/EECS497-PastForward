"""REST API for likes create."""
import flask
import insta485
from insta485.api.auth import get_auth


@insta485.app.route('/api/v1/comments/<commentid>/', methods=['DELETE'])
def get_comment_delete(commentid):
    """Delete a comment. Include the ID of the comment in the URL. Return 204.

    on success. If the commentid does not exist, return 404. If the user
    doesn’t own the comment, return 403.
    """
    logname = ""

    if 'logname' not in flask.session:
        if 'Authorization' in flask.request.headers:
            username = flask.request.authorization['username']
            password = flask.request.authorization['password']
            context = {}
            # -1 represents username does not exist
            if (get_auth(username, password) == -1):
                context["message"] = "Username not found"
                context["status_code"] = 403
                return flask.jsonify(**context), 403

            # -2 represents wrong password
            elif (get_auth(username, password) == -2):
                context["message"] = "Incorrect Password"
                context["status_code"] = 403
                return flask.jsonify(**context), 403
            else:
                logname = username
        else:
            return flask.redirect(flask.url_for('show_login')), 403
    else:
        logname = flask.session['logname']

    connection = insta485.model.get_db()
    com = connection.execute(
        "SELECT owner "
        "FROM comments "
        "WHERE commentid = ?",
        (commentid,)
    )
    comment = com.fetchone()

    context = {}
    if comment is None:
        context["message"] = "commentid does not exist"
        context["status_code"] = 404
        return flask.jsonify(**context), 404
    elif (comment["owner"] != logname):
        context["message"] = "user does not own the comment"
        context["status_code"] = 403
        return flask.jsonify(**context), 403
    else:
        connection.execute(
            "DELETE FROM comments "
            "WHERE commentid = ?",
            (commentid,)
        )

        context["message"] = "delete comment with commentid = {{commentid}}"
        context["status_code"] = 204
        return flask.jsonify(**context), 204

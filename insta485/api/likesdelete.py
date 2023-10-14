"""REST API for likes create."""
import flask
import insta485
from insta485.api.auth import get_auth


@insta485.app.route('/api/v1/likes/<likeid>/', methods=['DELETE'])
def get_like_delete(likeid):
    """Delete one “like”. Return 204 on success. If the likeid does not exist,
     return 404. If the user does not own the like, return 403."""
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
    username = logname


    connection = insta485.model.get_db()
    lik = connection.execute(
        "SELECT owner, likeid "
        "FROM likes "
        "WHERE likeid = ?",
        (likeid,)
    )
    like = lik.fetchone()

    context = {}
    if like is None:
        context["message"] = "likeid does not exist"
        context["status_code"] = 404
        return flask.jsonify(**context), 404
    elif (like["owner"] != logname):
        context["message"] = "user does not own the like"
        context["status_code"] = 403
        return flask.jsonify(**context), 403
    else:
        connection.execute(
            "DELETE FROM likes "
            "WHERE owner = ? AND likeid = ?",
            (logname, likeid,)
        )

        context["message"] = "delete like with likeid = {{likeid}}"
        context["status_code"] = 204
        return flask.jsonify(**context), 204

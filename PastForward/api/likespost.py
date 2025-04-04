"""REST API for likes create."""

import flask
import PastForward
from PastForward.api.auth import get_auth


@PastForward.app.route('/api/v1/likes/', methods=['POST'])
def get_like_create():
    """Create one “like” for a specific post. Return 201 on success. If the."""
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

    postid = flask.request.args.get('postid')

    connection = PastForward.model.get_db()
    lik = connection.execute(
        "SELECT owner, likeid "
        "FROM likes "
        "WHERE owner = ? AND postid = ?",
        (logname, postid,)
    )
    like = lik.fetchone()

    content = {}
    if like is None:
        connection.execute(
            "INSERT INTO likes (owner, postid) "
            "VALUES (?, ?)",
            (logname, postid,)
        )

        cre = connection.execute(
            "SELECT owner, likeid "
            "FROM likes "
            "WHERE owner = ? AND postid = ?",
            (logname, postid,)
        )
        created = cre.fetchone()

        content["likeid"] = created["likeid"]
        content["url"] = f"/api/v1/likes/{ created['likeid'] }/"

        return flask.jsonify(**content), 201
    else:
        content["likeid"] = like["likeid"]
        content["url"] = f"/api/v1/likes/{ like['likeid'] }/"
        return flask.jsonify(**content), 200

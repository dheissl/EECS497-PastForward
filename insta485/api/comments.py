"""REST API for likes create."""
import flask
import insta485
from insta485.api.auth import get_auth


@insta485.app.route('/api/v1/comments/', methods=['POST'])
def get_comment_create():
    """Add one comment to a post. Include the ID of the new comment in the
     return data. Return 201 on success."""
    logname = ""

    if 'logname' not in flask.session:
        username = flask.request.authorization['username']
        password = flask.request.authorization['password']
        if username is not None:
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
            return flask.redirect(url_for('show_login'))
    else:
        logname = flask.session['logname']
        
    postid = flask.request.args.get('postid')
    text = flask.request.form.get('text')
    
    connection = insta485.model.get_db()
    connection.execute(
        "INSERT INTO comments (owner, postid, text) "
        "VALUES (?, ?, ?)",
        (logname, postid, text)
    )
    
    com = connection.execute(
        "SELECT * FROM comments WHERE commentid = "
        "(SELECT last_insert_rowid() FROM comments) ",
    )
    comment = com.fetchone()
    
    context = {}
    context["commentid"] = comment["commentid"]
    context["lognameOwnsThis"] = True
    context["owner"] = logname
    context["ownerShowUrl"] = flask.url_for('show_user', username=logname)
    context["text"] = text
    context["url"] = f"/api/vi/comments/{comment['commentid']}"

    return flask.jsonify(**context), 201

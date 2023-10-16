"""REST API for posts."""
import flask
import insta485
from insta485.api.auth import get_auth


@insta485.app.route('/api/v1/posts/')
def get_posts():
    """Return post on postid."""
    params = []
    if flask.request.args.get("size", type=int) is not None:
        # Default to 10 if not provided
        size = flask.request.args.get("size", default=10, type=int)
        params.append(f"size={size}")
    else:
        size = 10
    if flask.request.args.get("page", type=int) is not None:
        # Default to 0 if not provided
        page = flask.request.args.get("page", default=0, type=int)
        params.append(f"page={page}")
    else:
        page = 0
    if flask.request.args.get('postid_lte', type=int) is not None:
        # Default to None if not provided
        postid_lte = flask.request.args.get('postid_lte',
                                            type=int, default=None)
        params.append(f"postid_lte={postid_lte}")
    else:
        postid_lte = None

    if size <= 0:
        return flask.Response('BAD REQUEST', 400)
    if page < 0:
        return flask.Response('BAD REQUEST', 400)
    # todo this being a bitch cant authorize
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
    cur = connection.execute(
        "SELECT p.filename AS pic, p.owner AS owner, p.postid AS postid,"
        " p.created AS timestamp, u.filename AS profile_pic "
        "FROM posts AS p "
        "JOIN following AS f ON p.owner = f.username2 "
        "JOIN users AS u ON p.owner = u.username "
        "WHERE f.username1 = ? "
        "AND p.postid > ? "
        "UNION "
        "SELECT p.filename AS pic, p.owner AS owner, p.postid AS postid,"
        " p.created AS timestamp, u.filename AS profile_pic "
        "FROM posts AS p "
        "JOIN users AS u ON p.owner = u.username "
        "WHERE p.owner = ? "
        "AND p.postid > ?",
        (username, postid_lte, username, postid_lte)
    )
    newposts = cur.fetchall()

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
        "WHERE p.owner = ? "
        "ORDER BY p.postid DESC"
        " LIMIT ? "
        "OFFSET ?",
        (username, username, size, (page*size)+len(newposts))
    )
    posts = cur.fetchall()
    if postid_lte is None:
        postid_lte = posts[0]["postid"]
    page = page + 1
    nex = ""
    lenth = len(posts)
    if lenth >= size:
        nex = f"/api/v1/posts/?size={size}&page={page}&postid_lte={postid_lte}"
    else:
        size = lenth

    base_url = f"/api/v1/posts/"
    if params:
        base_url = f"{base_url}?{'&'.join(params)}"

    result = {"next": nex, "results": [], "url": base_url}
    for i in range(size):
        result["results"].append({"postid": posts[i]["postid"],
                                  "url": f"/api/v1/posts/"
                                  + f"{posts[i]['postid']}/"})
    return result


def verify_user(username, password):
    """DOCTRING."""
    connection = insta485.model.get_db()

    cred = connection.execute(
        "SELECT username, password "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    credentials = cred.fetchone()

    if not credentials:
        return False

    if credentials['username'] != username:
        return False

    db_password = credentials['password']
    algorithm, salt, hash = db_password.split('$')

    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_string = "$".join([algorithm, salt, password_hash])

    if db_password != password:
        return False

    return True

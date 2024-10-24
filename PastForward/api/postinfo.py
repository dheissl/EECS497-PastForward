"""REST API for posts."""
import flask
import PastForward
from PastForward.api.auth import get_auth


@PastForward.app.route('/api/v1/posts/<int:postid>/')
def get_post(postid):
    """Header stuff."""
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

    connection = PastForward.model.get_db()
    cur = connection.execute(
        "SELECT p.owner AS owner "
        "FROM posts AS p ",
    )
    allposts = cur.fetchall()

    if postid > len(allposts):
        return flask.Response('Not Found', 404)

    context = {}
    comments = create_comments(postid, logname)
    context['comments'] = comments
    context['comments_url'] = f"/api/v1/comments/?postid={postid}"

    cur = connection.execute(
        """SELECT
        created AS post_created_time,
        filename AS image_url
    FROM
        posts
    WHERE
        postid = ?""", (postid,)
    )
    timenimg = cur.fetchall()
    context['created'] = timenimg[0]['post_created_time']
    context['imgUrl'] = f"/uploads/{timenimg[0]['image_url']}"

    cur = connection.execute(
        """SELECT
            posts.owner AS owner,
            users.filename AS pic
        FROM
            posts
        INNER JOIN
            users ON posts.owner = users.username
        WHERE
            posts.postid = ?""", (postid,)
    )
    ownernpic = cur.fetchall()
    context['owner'] = ownernpic[0]['owner']
    context['ownerImgUrl'] = f"/uploads/{ownernpic[0]['pic']}"
    context['ownerShowUrl'] = f"/users/{ownernpic[0]['owner']}/"
    context['postShowUrl'] = f"/posts/{postid}/"
    context['postid'] = postid
    context['url'] = f"/api/v1/posts/{postid}/"

    likes = create_likes(postid, logname)
    context['likes'] = likes

    return flask.jsonify(**context)


def create_likes(postid, logname):
    """DOCSTRING."""
    connection = PastForward.model.get_db()
    cur = connection.execute(
        """SELECT
            owner, likeid
        FROM
            likes
        WHERE
            postid = ?""", (postid,)
    )
    lik = cur.fetchall()

    liked = False
    numLikes = 0
    for like in lik:
        if like['owner'] == logname:
            liked = True
        numLikes += 1

    likes = {}
    likes['lognameLikesThis'] = liked
    likes['numLikes'] = numLikes
    if liked is True:
        likes['url'] = f"/api/v1/likes/{like['likeid']}/"
    else:
        likes['url'] = None
    return likes


def create_comments(postid, logname):
    """Docstring."""
    connection = PastForward.model.get_db()
    cur = connection.execute(
          """SELECT
    commentid AS id,
    text,
    created,
    owner
    FROM
    comments
          WHERE
    postid = ?""", (postid,)
    )
    com = cur.fetchall()
    comments = []
    for comment in com:
        val = {}
        val['commentid'] = comment['id']
        if comment['owner'] == logname:
            val['lognameOwnsThis'] = True
        else:
            val['lognameOwnsThis'] = False
        val['owner'] = comment['owner']
        val['ownerShowUrl'] = f"/users/{comment['owner']}/"
        val['text'] = comment['text']
        val['url'] = f"/api/v1/comments/{comment['id']}/"
        comments.append(val)
    return comments

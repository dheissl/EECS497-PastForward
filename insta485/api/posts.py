"""REST API for posts."""
import flask
import insta485


@insta485.app.route('/api/v1/posts/')
def get_post():
    """Return post on postid."""

    size = flask.request.args.get("size", default=10, type=int)  # Default to 10 if not provided
    page = flask.request.args.get("page", default=0, type=int)  # Default to 0 if not provided
    postid_lte = flask.request.args.get('postid_lte', type=int, default=None)  # Default to None if not provided
    if size <= 0:
      return flask.Response('BAD REQUEST', 400)
    if page < 0:
      return flask.Response('BAD REQUEST', 400)
    #todo this being a bitch cant authorize
    username = ""
    if hasattr(flask, 'session'):
      if 'username' in flask.session:
        username = flask.session['username']
      else:
        return flask.Response('Could not verify', 403)
    # Todo: change this to account for each username
    elif 'username' in flask.request.authorization:
      username = flask.request.authorization['username']
      password = flask.request.authorization['password']
      if not verify_user(username, password):
        return flask.Response('Could not verify', 403)
      pass
    else:
      return flask.Response('Could not verify', 403)
      
    connection = insta485.model.get_db()
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
        (username, username, size, page*size)
    )
    posts = cur.fetchall()
    if postid_lte is None:
      postid_lte = posts[0]["postid"]
    page = page + 1
    nex = ""
    lenth = length(posts)
    if lenth >= size:
      nex = f"/api/v1/posts/?size={size}&page={page}&postid_lte={postid_lte}"
    else:
      size = lenth


    result = {"next": nex, "results": [], "url": "/api/v1/posts/"}
    for i in range(size):
      result["results"].append({"postid": posts[i]["postid"], 
                          "url": f"/api/v1/posts/{posts[i]['postid']}/"})
    
    return result

def verify_user(username, password):
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

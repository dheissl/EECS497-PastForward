"""
PastForward logout (main) view.

URLs include:

"""
import pathlib
import uuid
import flask
import PastForward
from flask import url_for, request, abort, redirect
import os


@PastForward.app.route('/posts/', methods=['POST'])
def handle_posts():
    """POST posts for create, delete."""
    if 'logname' not in flask.session:
        return flask.redirect(url_for('show_login'))
    logname = flask.session['logname']
    connection = PastForward.model.get_db()
    # Get the operation and postid from the form data
    operation = request.form.get('operation')
    postid = request.form.get('postid')
    if operation == 'create':
        image_file = request.files['file']
    # Get the current URL or use '/' as the default
    target_url = request.args.get('target', f'/users/{logname}/')
    if operation == 'create':
        # Check if the image file is empty
        print(image_file)
        if not image_file or not image_file.filename:
            abort(400, 'Image file cannot be empty')

        # Save the image file to the disk
        # Unpack flask object
        filename = image_file.filename

        # Compute base name (filename without directory).
        # We use a UUID to avoid clashes with existing files, and ensure that
        # the name is compatible with the filesystem.
        # For best practive, we ensure uniform file extensions
        # (e.g. lowercase).
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"

        # Save to disk
        path = PastForward.app.config["UPLOAD_FOLDER"]/uuid_basename
        image_file.save(path)

        # Create a new post
        connection.execute(
            "INSERT INTO posts(filename, owner) VALUES "
            "(?, ?)",
            (uuid_basename, logname,)
        )
    elif operation == 'delete':
        # Check if the user owns the post
        pos = connection.execute(
            "SELECT owner, filename "
            "FROM posts "
            "WHERE postid = ?",
            (postid,)
        )
        post = pos.fetchall()

        if post[0]['owner'] != logname:
            abort(403, 'You do not have permission to delete this post')

        # Delete the image file from the filesystem
        filena = PastForward.app.config["UPLOAD_FOLDER"]/post[0]['filename']
        if os.path.exists(filena):
            os.remove(filena)

        # Delete the post from the data store
            connection.execute(
                "DELETE FROM posts "
                "WHERE postid = ?",
                (postid,)
            )

    # Redirect to the specified target URL
    return redirect(target_url)

"""
PastForward followers (main) view.

URLs include:

"""
import flask
import PastForward
import arrow
from flask import url_for
from flask import send_from_directory, abort
import os


@PastForward.app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Image."""
    # Serve the image from the uploads directory
    if 'logname' not in flask.session:
        abort(403, "User not authenticated")
    filena = PastForward.app.config["UPLOAD_FOLDER"]/filename
    if not os.path.exists(filena):
        abort(404, "image does not exist")
    return send_from_directory(PastForward.app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)

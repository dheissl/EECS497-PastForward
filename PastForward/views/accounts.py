"""
PastForward account posts.

URLs include:

"""

import flask
import PastForward
import uuid
import hashlib
import pathlib
import os
from flask import abort
from flask import url_for, request


@PastForward.app.route('/accounts/', methods=['POST'])
def show_accounts():
    """POST accounts for create, delete, edit, login, and update_password."""
    operation = flask.request.form.get('operation')

    if operation == 'login':
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')

        if not username:
            abort(400)
        if not password:
            abort(400)

        connection = PastForward.model.get_db()

        cred = connection.execute(
            "SELECT username, password "
            "FROM users "
            "WHERE username = ? ",
            (username, )
        )
        credentials = cred.fetchone()

        if not credentials:
            abort(403)

        if credentials['username'] != username:
            abort(403)

        db_password = credentials['password']
        algorithm, salt, hash = db_password.split('$')

        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_string = "$".join([algorithm, salt, password_hash])

        if db_password != password_string:
            abort(403)

        flask.session['logname'] = username
        target_url = flask.request.args.get('target', url_for('show_index'))
        return flask.redirect(target_url)

    elif operation == 'create':
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')
        fullname = flask.request.form.get('fullname')
        email = flask.request.form.get('email')
        file = flask.request.files.get('file')

        if not username:
            abort(400)
        if not password:
            abort(400)
        if not fullname:
            abort(400)
        if not email:
            abort(400)
        if not file:
            abort(400)

        """set passord"""
        algorithm = 'sha512'
        salt = uuid.uuid4().hex
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])

        """set file"""
        filename = file.filename
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"
        path = PastForward.app.config["UPLOAD_FOLDER"]/uuid_basename
        file.save(path)

        """check for username in database"""
        connection = PastForward.model.get_db()

        u = connection.execute(
            "SELECT username "
            "FROM users "
            "WHERE username = ? ",
            (username, )
        )
        check = u.fetchone()

        if check:
            abort(409)

        """add to database"""
        cre = connection.execute(
            "INSERT INTO users "
            "(username, password, fullname, email, filename) "
            "VALUES (?, ?, ?, ?, ?)",
            (username, password_db_string, fullname, email, uuid_basename,)
        )
        connection.commit()

        """log in user"""
        flask.session['logname'] = username

        target_url = flask.request.args.get('target', url_for('show_index'))
        return flask.redirect(target_url)

    elif operation == 'delete':
        if 'logname' not in flask.session:
            abort(403)
        else:
            logname = flask.session['logname']
            connection = PastForward.model.get_db()

            """delete post files created by this user"""
            pos = connection.execute(
                "SELECT filename "
                "FROM posts "
                "WHERE owner = ?",
                (logname,)
            )
            posts = pos.fetchall()

            for p in posts:
                filename = PastForward.app.config["UPLOAD_FOLDER"]/p['filename']
                if os.path.exists(filename):
                    os.remove(filename)

            """delete user icon file"""
            u = connection.execute(
                "SELECT filename "
                "FROM users "
                "WHERE username = ? ",
                (logname, )
            )
            user = u.fetchall()

            for u in user:
                filename = PastForward.app.config["UPLOAD_FOLDER"]/u['filename']
                if os.path.exists(filename):
                    os.remove(filename)

            """remove from users"""
            connection.execute(
                "DELETE FROM users "
                "WHERE username = ?",
                (logname,)
            )
            connection.commit()

            flask.session.clear()
            targ = flask.request.args.get('target', url_for('show_create'))
            return flask.redirect(targ)

    elif operation == 'edit_account':
        if 'logname' not in flask.session:
            abort(403)

        logname = flask.session['logname']
        fullname = flask.request.form.get('fullname')
        email = flask.request.form.get('email')
        file = flask.request.files.get('file')

        if not fullname:
            abort(403)

        if not email:
            abort(403)

        connection = PastForward.model.get_db()

        if not file:
            connection.execute(
                "UPDATE users "
                "SET fullname = ?, email = ?"
                "WHERE username = ? ",
                (fullname, email, logname, )
            )
            connection.commit()
        else:
            filename = file.filename
            stem = uuid.uuid4().hex
            suffix = pathlib.Path(filename).suffix.lower()
            uuid_basename = f"{stem}{suffix}"
            path = PastForward.app.config["UPLOAD_FOLDER"]/uuid_basename
            file.save(path)

            connection.execute(
                "UPDATE users "
                "SET fullname = ?, email = ?, filename = ?"
                "WHERE username = ? ",
                (fullname, email, uuid_basename, logname, )
            )
            connection.commit()

            targ = flask.request.args.get('target', url_for('show_edit'))
            return flask.redirect(targ)

    elif operation == 'update_password':
        if 'logname' not in flask.session:
            abort(403)

        logname = flask.session['logname']

        password = flask.request.form.get('password')
        new_password1 = flask.request.form.get('new_password1')
        new_password2 = flask.request.form.get('new_password2')

        if not password:
            abort(400)

        if not new_password1:
            abort(400)

        if not new_password2:
            abort(400)

        """verify password against user's password in database"""
        connection = PastForward.model.get_db()

        cred = connection.execute(
            "SELECT password "
            "FROM users "
            "WHERE username = ? ",
            (logname, )
        )
        credentials = cred.fetchone()

        db_password = credentials['password']

        algorithm, salt, hash = db_password.split('$')

        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_string = "$".join([algorithm, salt, password_hash])

        if db_password != password_string:
            abort(403)

        """verify new passwords are equal"""
        if new_password1 != new_password2:
            abort(401)

        """create new hashed password"""
        algorithm2 = 'sha512'
        salt2 = uuid.uuid4().hex
        hash_obj2 = hashlib.new(algorithm2)
        password_salted2 = salt2 + new_password1
        hash_obj2.update(password_salted2.encode('utf-8'))
        password_hash2 = hash_obj2.hexdigest()
        password_db_string2 = "$".join([algorithm2, salt2, password_hash2])

        connection.execute(
            "UPDATE users "
            "SET password = ? "
            "WHERE username = ? ",
            (password_db_string2, logname, )
        )
        connection.commit()

        target_url = flask.request.args.get('target', url_for('show_edit'))
        return flask.redirect(target_url)

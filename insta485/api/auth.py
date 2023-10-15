"""Authentification."""
import flask
import insta485
import hashlib


def get_auth(username, password):
    connection = insta485.model.get_db()

    cred = connection.execute(
        "SELECT username, password "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    credentials = cred.fetchone()

    if not credentials:
        return -1

    db_password = credentials['password']
    algorithm, salt, hash = db_password.split('$')

    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_string = "$".join([algorithm, salt, password_hash])

    if db_password != password_string:
        return -2

    return 0

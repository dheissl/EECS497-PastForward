"""PastForward development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b"'\xa7]\xd97Y#\x1f\x00\x9a\xb1\xb2\xa1RHU\x88\r\xb3o$\x17\xe2R"
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
PastForward_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = PastForward_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/PastForward.sqlite3
DATABASE_FILENAME = PastForward_ROOT/'var'/'PastForward.sqlite3'

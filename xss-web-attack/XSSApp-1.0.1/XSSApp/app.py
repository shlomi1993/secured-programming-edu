from http import HTTPStatus

import flask
import base64
import hmac
import os
import logging
import jinja2.utils

from . import validation_utilities
from .validation_utilities import generate_regex_validator, is_valid_uploaded_file_name

from werkzeug.utils import secure_filename

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from flask import Flask

TEMPLATES_FOLDER = "templates"
app = Flask(__name__, template_folder=TEMPLATES_FOLDER, static_folder="static")


def generate_random_key(length=16):
    return base64.b64encode(os.urandom(length))


messages = []


VALIDATORS = {
    "name": generate_regex_validator(validation_utilities.NAME_REGEX, "name"),
    "phone_number": generate_regex_validator(validation_utilities.PHONE_REGEX, "phone number"),
    "email": generate_regex_validator(validation_utilities.MAIL_REGEX, "mail address"),
    "message": validation_utilities.validate_message,
}


BASE_PATH = os.path.dirname(__file__)
IS_ADMIN_KEY = 'is_admin'
CSRF_TOKEN_KEY = 'csrf_token'
AES_BLOCK_SIZE = AES.block_size // 8
# Simple and collision free
CSRF_LENGTH = AES_BLOCK_SIZE * 2


def is_administrator_logged_in():
    return IS_ADMIN_KEY in flask.session and flask.session[IS_ADMIN_KEY]


def attempt_admin_login():
    sent_password = flask.request.args.get("password", None)
    if sent_password and test_administrator_password(sent_password):
        app.logger.info("Administrator logged in successfully!")
        flask.session[IS_ADMIN_KEY] = True
        return True
    return False


def aes_encrypt(key: bytes, iv: bytes, message: bytes) -> bytes:
    encryptor = Cipher(AES(key), CBC(iv)).encryptor()
    return encryptor.update(message) + encryptor.finalize()


def aes_decrypt(key: bytes, iv: bytes, message: bytes) -> bytes:
    decryptor = Cipher(AES(key), CBC(iv)).decryptor()
    return decryptor.update(message) + decryptor.finalize()


def get_app_key():
    return base64.b64decode(app.secret_key)


def get_csrf_token_noexcept():
    csrf_encoded_value = flask.session.get(CSRF_TOKEN_KEY, None)
    if not csrf_encoded_value:
        return None
    csrf_value = base64.b64decode(csrf_encoded_value)
    iv, encrypted_csrf = csrf_value[:AES_BLOCK_SIZE], csrf_value[AES_BLOCK_SIZE:]
    return aes_decrypt(get_app_key(), iv, encrypted_csrf)


def generate_csrf_token():
    csrf_value = os.urandom(CSRF_LENGTH)
    iv = os.urandom(AES_BLOCK_SIZE)
    flask.session[CSRF_TOKEN_KEY] = base64.b64encode(
        iv + aes_encrypt(get_app_key(), iv, csrf_value)).decode()
    return csrf_value


def get_or_set_csrf_token():
    csrf_value = get_csrf_token_noexcept()
    if not csrf_value:
        csrf_value = generate_csrf_token()
    return base64.b64encode(csrf_value).decode()


def add_message(args: dict):
    required_args = ["name", "phone_number", "email", "subject", "message"]
    result = {name: args.get(name) for name in required_args}
    for validator_name, validator in VALIDATORS.items():
        if validator_name in result:
            validator(result[validator_name])
    result["message"] = jinja2.utils.markupsafe.Markup(result["message"])

    if not result["name"]:
        # Empty message or None
        raise ValueError("Must provide a name for every message!")

    if is_administrator_logged_in():
        result["name"] = result["name"] + " (Administrator)"
    else:
        result["name"] = result["name"] + " (Weak)"

    messages.append(result)


PUBLIC_SALT_VALUE = bytes.fromhex("d38b1c682094f508a871fbdd9508ac00")
PASSWORD_HASH = bytes.fromhex(
    "fe6620ee183864c965445072cdff51b0e474094c66ae874b40bc4f47ea563ff0")


def test_administrator_password(password: str) -> bool:
    encoded_password = password.encode("utf-8")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=PUBLIC_SALT_VALUE,
        iterations=390000,
    )
    try:
        kdf.verify(encoded_password, PASSWORD_HASH)
        return True
    except Exception:
        return False


@ app.route('/')
def index():
    is_admin = is_administrator_logged_in()
    resp = flask.Response()
    resp.set_data(flask.render_template(
        "index.html", messages=messages, csrf_value=get_or_set_csrf_token(), is_admin=is_admin))
    resp.calculate_content_length()
    return resp


@app.route("/login", methods=["GET"])
def login():
    attempt_admin_login()
    return flask.redirect('/')


@app.route("/drop_all_messages")
def drop_all_messages():
    if is_administrator_logged_in():
        messages.clear()
    return flask.redirect('/')


@app.route("/logout")
def logout():
    flask.session[IS_ADMIN_KEY] = False
    return flask.redirect('/')


@app.route('/request', methods=['POST'])
def handle_request():
    sent_token = flask.request.form.get(CSRF_TOKEN_KEY)
    try:
        if sent_token is not None:
            sent_token = base64.b64decode(sent_token)
    except Exception:
        sent_token = None
    actual_token = get_csrf_token_noexcept()
    if not actual_token or not sent_token or not hmac.compare_digest(sent_token, actual_token):
        # You can assume this is not a vulnerability.
        app.logger.error(
            "Bad request - invalid csrf token (%s != %s)", sent_token, actual_token)
        return flask.Response(
            response="Invalid token", status=HTTPStatus.UNAUTHORIZED)
    try:
        add_message(flask.request.form)
    except ValueError as e:
        app.logger.error(
            "Bad request - invalid content (%s)", e.args[0])
        return flask.Response(
            response=e.args[0], status=HTTPStatus.BAD_REQUEST)

    return flask.redirect('/')


@app.route('/favicon.ico')
def get_icon():
    return app.send_static_file('favicon.ico')


#################################################
#           Start of optional code              #
#################################################


@app.route("/local/<file>")
def browse_local_file(file):
    if not is_administrator_logged_in():
        return flask.Response(status=HTTPStatus.UNAUTHORIZED)
    if isinstance(file, str) and is_valid_uploaded_file_name(file):
        full_path = os.path.join(
            BASE_PATH, TEMPLATES_FOLDER, secure_filename(file))
        if os.path.isfile(full_path):
            resp = flask.Response()
            resp.set_data(flask.render_template(file))
            resp.calculate_content_length()
            return resp
    return flask.redirect('/')


@app.route('/upload', methods=['POST'])
def do_upload_file():
    if not is_administrator_logged_in():
        return flask.Response(status=HTTPStatus.UNAUTHORIZED)
    if 'file' not in flask.request.files:
        return flask.Response(response="No file found", status=HTTPStatus.BAD_REQUEST)
    file = flask.request.files['file']
    if file.filename == '':
        return flask.Response(response="No file name found", status=HTTPStatus.BAD_REQUEST)
    if file and file.filename and is_valid_uploaded_file_name(file.filename):
        target_path = os.path.join(
            BASE_PATH, TEMPLATES_FOLDER, secure_filename(file.filename))
        if not os.path.exists(target_path):
            file.save(target_path)
            return flask.redirect("/")
        return flask.Response(response="File already exists", status=HTTPStatus.BAD_REQUEST)
    return flask.Response(response="Invalid filename", status=HTTPStatus.BAD_REQUEST)


@app.route('/upload', methods=['GET'])
def upload_file():
    if not is_administrator_logged_in():
        return flask.Response(status=HTTPStatus.UNAUTHORIZED)
    resp = flask.Response()
    resp.set_data(flask.render_template("upload.html"))
    resp.calculate_content_length()
    return resp


#################################################
#           End of optional code                #
#################################################


def start_app():
    secret_key = generate_random_key()
    app.logger.setLevel(logging.INFO)
    app.logger.info("App secret key: %s", base64.b64encode(secret_key))
    app.secret_key = secret_key
    app.config["SESSION_COOKIE_HTTPONLY"] = False

    app.run(host="0.0.0.0", ssl_context=('cert.pem', 'key.pem'))


if __name__ == "__main__":
    start_app()

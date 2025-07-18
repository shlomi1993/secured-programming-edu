from flask import Flask


app = Flask(__name__)


@ app.route('/')
def index():
    return '<script>alert(\'Executed from <object>\')</script>'


def start_app():
    app.run(host='127.0.0.1', port=8080)


if __name__ == "__main__":
    start_app()

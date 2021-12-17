"""Main class of the project"""
import os
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    """Sample path function"""
    return "<p>Hello, World!</p>"


def create_app():
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_ENV") == "dev")

import os

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'


def create_app():
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_ENV") == "dev")
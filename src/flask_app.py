"""Initial app module"""

import os

from flask import Flask
from flask_breadcrumbs import Breadcrumbs

app = Flask(__name__)
app.config["SECRET_KEY"] = "C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb"

Breadcrumbs(app=app)


def create_app():
    """Starts the application"""
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_ENV") == "dev")

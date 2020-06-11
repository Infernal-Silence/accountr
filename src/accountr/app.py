from flask import Flask

from .database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('accountr.config.Config')
    db.init_app(app)
    return app

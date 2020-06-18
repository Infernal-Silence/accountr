from flask import Flask

from accountr.blueprints import auth_bp, users_bp
from accountr.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix = '/users')
    return app
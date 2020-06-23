from flask import Flask

from accountr.blueprints import (
    auth_bp,
    users_bp,
    categories_bp,
    operations_bp,
    report_bp,
)
from accountr.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('accountr.config.Config')
    db.init_app(app)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(operations_bp, url_prefix='/operations')
    app.register_blueprint(report_bp, url_prefix='/report')
    return app

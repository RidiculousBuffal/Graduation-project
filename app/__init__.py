from flask import Flask

from app.config import config
from app.ext.extensions import db, migrate, jwt, cors


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # 注册蓝图
    from app.routes.auth_api import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app

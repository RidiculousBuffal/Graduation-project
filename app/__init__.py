from flask import Flask

from app.config import config
from app.ext.extensions import db, migrate, jwt, cors
from app.routes.aircraft_api import aircraft_bp
from app.routes.auth_api import auth_bp
from app.routes.dictionary_api import dictionary_bp
from app.routes.flight_api import flight_bp
from app.routes.inspection_record_api import inspection_bp
from app.routes.ipfs_api import ipfs_bp
from app.routes.task_api import task_bp
from app.routes.terminal_api import terminal_bp


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    print('✅ 数据库链接成功')
    migrate.init_app(app, db)
    print('✅ 数据库迁移成功')
    jwt.init_app(app)
    print('✅ jwt初始化成功')
    cors.init_app(app)
    print('✅ cors初始化成功')

    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(aircraft_bp, url_prefix='/api/aircraft')
    app.register_blueprint(ipfs_bp, url_prefix='/api/ipfs')
    app.register_blueprint(flight_bp, url_prefix='/api/flight')
    app.register_blueprint(terminal_bp, url_prefix='/api/terminal')
    app.register_blueprint(dictionary_bp, url_prefix='/api/dict')
    app.register_blueprint(task_bp, url_prefix='/api/task')
    app.register_blueprint(inspection_bp, url_prefix='/api/inspection')
    return app

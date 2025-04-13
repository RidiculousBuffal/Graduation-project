import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{os.environ.get('DB_USERNAME')}:"
        f"{os.environ.get('DB_PASSWORD')}@"
        f"{os.environ.get('DB_HOST')}:"
        f"{os.environ.get('DB_PORT')}/"
        f"{os.environ.get('DB_NAME')}"
        f"?charset=utf8mb4"
    )
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)  # 1 天
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # refresh token 30天
    # IPFS配置
    IPFS_API_HOST = os.environ.get('ipfs_host') or 'http://127.0.0.1'
    IPFS_API_PORT = int(os.environ.get('ipfs_port') or 10503)
    IPFS_GATEWAY_HOST = os.environ.get('ipfs_gateway') or 'http://127.0.0.1'
    IPFS_GATEWAY_PORT = int(os.environ.get('ipfs_gateway_port') or 8080)
    # IPFS MFS配置
    IPFS_USE_MFS = True if os.getenv('ipfs_use_mfs').upper() == 'TRUE' else False
    IPFS_MAX_UPLOAD_WORKERS = int(os.getenv('IPFS_MAX_UPLOAD_WORKERS')) or 4
    IPFS_TIMESTAMP_FORMAT = os.environ.get('IPFS_TIMESTAMP_FORMAT') or 'timestamp'
    IPFS_MFS_BASE_DIR = os.getenv('ipfs_mfs_base_dir') or '/upload'
    UPLOAD_ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'zip', 'rar'}
    MAX_CONTENT_LENGTH = 1000 * 1024 * 1024  # 限制上传大小为1G

class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

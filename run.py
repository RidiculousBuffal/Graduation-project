import os

if os.environ.get("FLASK_ENV") == "production":
    from gevent import monkey

    monkey.patch_all()
from dotenv import load_dotenv

load_dotenv()
from app.ext.extensions import db
from scripts.startScripts import initRoles, initPermissions, combineRoleWithPermissions, initDictionaryData
from app import app,celery


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'app': app}


with app.app_context():
    # 初始化角色
    initRoles()
    # 初始化权限
    initPermissions()
    # 绑定角色和权限
    combineRoleWithPermissions()
    # 字典表
    initDictionaryData()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

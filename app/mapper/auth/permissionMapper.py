from sqlalchemy import select

from app.models import Permission
from app.ext.extensions import db

class PermissionMapper:
    @staticmethod
    def get_permission_by_name(permission_name:str):
        q = select(Permission).where(Permission.permission_name==permission_name)
        permission = db.session.execute(q).scalar_one_or_none()
        return permission
from sqlalchemy import select
from app.models.auth import Permission
from app.DTO.user import Permission as AuthPermission
from app.ext.extensions import db


class PermissionMapper:
    @staticmethod
    def get_permission_by_name(permission_name: str):
        q = select(Permission).where(Permission.permission_name == permission_name)
        permission = db.session.execute(q).scalar_one_or_none()
        return permission

    @staticmethod
    def getAllPermissions():
        q = select(Permission)
        permissions = db.session.execute(q).scalars()
        return [
            AuthPermission(permission_id=p.permission_id, permission_name=p.permission_name, description=p.description)
            for p in permissions]

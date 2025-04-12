from sqlalchemy import select, and_

from app.ext.extensions import db
from app.models import Permission, RolePermission
from app.models.auth import Role,User
from app.models.auth import UserRole


class UserRolePermissionMapper:
    @staticmethod
    def combineUserWithRole(userId, roleId):
        userRole = UserRole(role_id=roleId, user_id=userId)
        db.session.add(userRole)
        db.session.commit()

    @staticmethod
    def getUserRole(userId: str):
        q = select(Role).join(UserRole).where(UserRole.user_id == userId)
        roles = db.session.execute(q).scalars()
        serialized_roles = [
            {
                "role_id": res.role_id,
                "role_name": res.role_name,
                "description": res.description
            }
            for res in roles
        ]
        return serialized_roles

    @staticmethod
    def getRolePermissions(roleId: int):
        q = select(Permission).distinct().join(RolePermission).where(RolePermission.role_id == roleId)
        permissions = db.session.execute(q).scalars()
        serialized_permissions = [
            {
                "permission_id": p.permission_id,
                "permission_name": p.permission_name,
                "description": p.description,
            } for p in permissions
        ]
        return serialized_permissions

    @staticmethod
    def getUserPermissions(userId:str):
        q = select(Permission).distinct().join(RolePermission).join(Role).join(UserRole).join(User).where(User.user_id==userId)
        permissions = db.session.execute(q).scalars()
        serialized_permissions = [
            {
                "permission_id": p.permission_id,
                "permission_name": p.permission_name,
                "description": p.description,
            } for p in permissions
        ]
        return serialized_permissions
    
    @staticmethod
    def combine_role_permission(roleId, permissionId):
        rp = RolePermission(role_id=roleId, permission_id=permissionId)
        db.session.add(rp)
        db.session.commit()

    @staticmethod
    def getRolePermissionsByRoleIdAndPermissionId(roleId: int, permissionId: int):
        q = select(RolePermission).where(
            and_(RolePermission.role_id == roleId, RolePermission.permission_id == permissionId))
        rp = db.session.execute(q).scalar_one_or_none()
        return rp

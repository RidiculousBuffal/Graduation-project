from app.ext.extensions import db
from app.models import Permission, RolePermission
from app.models.auth import Role
from app.models.auth import UserRole


class UserRolePermissionMapper:
    @staticmethod
    def combineUserWithRole(userId, roleId):
        userRole = UserRole(role_id=roleId, user_id=userId)
        db.session.add(userRole)
        db.session.commit()

    @staticmethod
    def getUserRole(userId):
        roles = db.session.query(UserRole, Role).join(
            Role, UserRole.role_id == Role.role_id
        ).filter(UserRole.user_id == userId).all()
        serialized_roles = [
            {
                "role_id": role_obj.role_id,
                "role_name": role_obj.role_name,
                "description": role_obj.description
            }
            for user_role, role_obj in roles
        ]
        print(serialized_roles)
        return serialized_roles

    @staticmethod
    def getRolePermissions(roleId):
        permissions = (db.session.query(Permission.permission_id, Permission.permission_name, Permission.description)
                       .distinct()
                       .join(RolePermission, RolePermission.permission_id == Permission.permission_id)
                       .filter(RolePermission.role_id == roleId).all())

        serialized_permissions = [
            {
                "permission_id": p.permission_id,
                "permission_name": p.permission_name,
                "description": p.description,
            } for p in permissions
        ]

        return serialized_permissions

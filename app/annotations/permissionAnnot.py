from functools import wraps

from flask_jwt_extended import jwt_required, get_jwt_identity

from app.mapper.auth.userRolePermissionMapper import UserRolePermissionMapper
from app.models.response import ResponseModel


def permission_required(permissions, all_required=True):
    if isinstance(permissions, str):
        permissions = [permissions]

    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user_permissions = UserRolePermissionMapper.getUserPermissions(user_id)
            user_permissions_name = [p.get('permission_name') for p in user_permissions]
            if all_required:
                # 要所有权限
                has_permission = all(p in user_permissions_name for p in permissions)
            else:
                has_permission = any(p in user_permissions_name for p in permissions)
            if not has_permission:
                return ResponseModel.fail(f'权限校验失败,要求权限:{permissions}'), 403
            return func(*args, **kwargs)

        return wrapper

    return decorator

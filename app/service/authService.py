from flask_jwt_extended import create_access_token, create_refresh_token

from app.consts.Roles import RoleConsts
from app.consts.auth import AuthConsts
from app.mapper.auth.roleMapper import RoleMapper
from app.mapper.auth.userMapper import UserMapper
from app.mapper.auth.userRolePermissionMapper import UserRolePermissionMapper
from app.models.response import ResponseModel


class AuthService:
    # 登录注册服务
    @staticmethod
    def login(username: str, password: str) -> ResponseModel:
        user = UserMapper.get_user_by_name(username)
        if not user or not user.check_password(password):
            return ResponseModel.fail(AuthConsts.LOGIN_ERROR)
        if not user.status:
            return ResponseModel.fail(AuthConsts.ACCOUNT_DISABLED)
        UserMapper.update_last_login(user.user_id)
        roles = UserRolePermissionMapper.getUserRole(user.user_id)
        permissions = []
        for r in roles:
            permissions.extend(UserRolePermissionMapper.getRolePermissions(r.get('role_id')))
        payload = {
            "user": user.to_dict(),
            "role": roles,
            "permissions": permissions
        }
        access_token = create_access_token(identity=user.user_id)
        refresh_token = create_refresh_token(identity=user.user_id)
        return ResponseModel.success(
            msg=AuthConsts.LOGIN_SUCCESS,
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "payload": payload
            }
        )

    @staticmethod
    def register(username: str, password: str, email: str = None) -> ResponseModel:
        if not UserMapper.validate_username(username):
            return ResponseModel.fail(msg=AuthConsts.USERNAME_ALREADY_EXISTS)
        if email and not UserMapper.validate_email(email):
            return ResponseModel.fail(msg=AuthConsts.EMAIL_ALREADY_EXISTS)
        user_id = UserMapper.add_user(username, password, email)
        role_id = RoleMapper.getRole(RoleConsts.USER).role_id
        UserRolePermissionMapper.combineUserWithRole(user_id, role_id)
        return ResponseModel.success(msg=AuthConsts.REGISTER_SUCCESS)

    @staticmethod
    def getAllEngineers():
        return ResponseModel.success(UserMapper.get_users_by_role(RoleConsts.ENGINEER))

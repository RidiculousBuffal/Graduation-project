from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash

from app.DTO.user import UserDTO, ResetPasswordDTO
from app.consts.Roles import RoleConsts
from app.consts.auth import AuthConsts
from app.exceptions.face import NoFaceFound
from app.lib.face.faceRecognition import FaceRecognition
from app.lib.face.faceRecognition import frc
from app.mapper.auth.roleMapper import RoleMapper
from app.mapper.auth.userMapper import UserMapper
from app.mapper.auth.userRolePermissionMapper import UserRolePermissionMapper
from app.models import User
from app.models.response import ResponseModel


class AuthService:
    # 登录注册服务
    faceLoginClient = FaceRecognition()

    @staticmethod
    def _process_login_info(user: User):
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
    def login(username: str, password: str) -> ResponseModel:
        user = UserMapper.get_user_by_name(username)
        if not user or not user.check_password(password):
            return ResponseModel.fail(AuthConsts.LOGIN_ERROR)
        if not user.status:
            return ResponseModel.fail(AuthConsts.ACCOUNT_DISABLED)
        return AuthService._process_login_info(user)

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

    @staticmethod
    def updateUserFaceInfo(user_id, face_info):
        UserMapper.update_user_face_login_info(user_id, face_info)
        # 上传图片到向量数据库
        try:
            embed = frc.face_embedding(face_info)
        except NoFaceFound as e:
            return ResponseModel.fail(msg=AuthConsts.FACEINFO_REQUIRED)
        frc.put_embedding_to_weaviate(embed, user_id)
        return ResponseModel.success(msg=None, data=face_info)

    @staticmethod
    def loginWithFaceInfo(face_info):
        try:
            embed = frc.face_embedding(face_info)
        except NoFaceFound as e:
            return ResponseModel.fail(msg=AuthConsts.FACEINFO_REQUIRED)
        user_id = frc.check_without_uuid(embed)
        if user_id:
            user = UserMapper.get_user_by_user_id(user_id)
            if user:
                return AuthService._process_login_info(user)
            else:
                return ResponseModel.fail(msg=AuthConsts.FACE_ERROR)
        else:
            return ResponseModel.fail(msg=AuthConsts.FACE_ERROR)

    @staticmethod
    def update_user_info(user: UserDTO, user_id: str):
        try:
            if user.faceInfo is None or user.faceInfo == '':
                frc.delete_embedding(user_id)
            UserMapper.update_user_basic_info(user, user_id)
            return ResponseModel.success(msg=AuthConsts.UPDATE_USER_INFO_SUCCESS,
                                         data=UserMapper.get_user_by_user_id(user_id).to_dict())
        except Exception as e:
            return ResponseModel.fail(msg=AuthConsts.UPDATE_USER_INFO_FAILURE, data=str(e))

    @staticmethod
    def resetUserPassword(password: ResetPasswordDTO, userId):
        user = UserMapper.get_user_by_user_id(userId)
        if not user.check_password(password.password):
            return ResponseModel.fail(msg=AuthConsts.ORIGIN_PASSWORD_WRONG, data=None)
        else:
            UserMapper.updatePassword(userId, generate_password_hash(password.newPassword))
            return ResponseModel.success(msg=AuthConsts.UPDATE_PASSWORD_SUCCESS, data=True)

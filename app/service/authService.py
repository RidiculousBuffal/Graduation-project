from typing import Optional

from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash

from app.DTO.user import UserDTO, ResetPasswordDTO, Role, Permission, RolePermissionDTO, createRoleDTO
from app.consts.Roles import RoleConsts
from app.consts.auth import AuthConsts
from app.mapper.auth.permissionMapper import PermissionMapper
from app.mapper.auth.roleMapper import RoleMapper
from app.mapper.auth.userMapper import UserMapper
from app.mapper.auth.userRolePermissionMapper import UserRolePermissionMapper
from app.models import User
from app.models.response import ResponseModel


class AuthService:
    @staticmethod
    def getAllUsersInfo(username: Optional[str] = None, name: Optional[str] = None, email: Optional[str] = None,
                        pageNum=1,
                        pageSize=10):
        resultWithoutRP = UserMapper.get_userInfo(username, name, email, pageNum, pageSize)
        for user in resultWithoutRP.data:
            roles, permissions = AuthService._getRoleAndPermissionByUserId(user.user_id)
            user.roles = [Role.model_validate(r) for r in roles]
            user.permissions = [Permission.model_validate(p) for p in permissions]
        return ResponseModel.success(msg=AuthConsts.GET_USERINFO_SUCCESS, data=resultWithoutRP.model_dump())

    @staticmethod
    def _getRoleAndPermissionByUserId(user_id):
        roles = UserRolePermissionMapper.getUserRole(user_id)
        permissions = []
        for r in roles:
            permissions.extend(UserRolePermissionMapper.getRolePermissions(r.get('role_id')))
        return roles, permissions

    @staticmethod
    def _process_login_info(user: User):
        UserMapper.update_last_login(user.user_id)
        roles, permissions = AuthService._getRoleAndPermissionByUserId(user.user_id)
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
        return ResponseModel.success(data=UserMapper.get_users_by_role(RoleConsts.ENGINEER),
                                     msg=AuthConsts.GET_ENGINEER_SUCCESS)

    @staticmethod
    def updateUserFaceInfo(user_id, face_info):
        UserMapper.update_user_face_login_info(user_id, face_info)
        # 同步调用 celery
        from app.worker.faceRecognition import create_user_face_embedding
        result = create_user_face_embedding.delay(face_info, user_id).get(timeout=120)
        if not result.get("success"):
            return ResponseModel.fail(msg=result.get("error") or "Face embedding failed")
        return ResponseModel.success(msg=None, data=face_info)

    @staticmethod
    def loginWithFaceInfo(face_info):
        # 同步调用 celery
        from app.worker.faceRecognition import get_user_id_by_face
        result = get_user_id_by_face.delay(face_info).get(timeout=120)
        user_id = result.get("user_id")
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
                # 同步删除
                from app.worker.faceRecognition import delete_face_embedding
                result = delete_face_embedding.delay(user_id).get(timeout=120)
                if not result.get("success"):
                    return ResponseModel.fail(msg=result.get("error") or "Delete embedding failed")
            UserMapper.update_user_basic_info(user, user_id)
            return ResponseModel.success(
                msg=AuthConsts.UPDATE_USER_INFO_SUCCESS,
                data=UserMapper.get_user_by_user_id(user_id).to_dict()
            )
        except Exception as e:
            return ResponseModel.fail(msg=AuthConsts.UPDATE_USER_INFO_FAILURE, data=str(e))
    @staticmethod
    def force_update_userInfo(user: UserDTO, user_id: str):
        try:
            UserMapper.update_user_basic_info(user, user_id)
            return ResponseModel.success(
                msg=AuthConsts.UPDATE_USER_INFO_SUCCESS,
                data=UserMapper.get_user_by_user_id(user_id).to_dict()
            )
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

    @staticmethod
    def forceResetUserPassword(password: str, userId: str):
        UserMapper.updatePassword(userId, generate_password_hash(password))
        return ResponseModel.success(msg=AuthConsts.UPDATE_PASSWORD_SUCCESS, data=True)

    @staticmethod
    def getAllPermissions():
        return ResponseModel.success(msg=AuthConsts.GET_USERINFO_SUCCESS,
                                     data=[x.model_dump() for x in PermissionMapper.getAllPermissions()])

    @staticmethod
    def getAllRolesWithTheirPermissions():
        AllRoles = RoleMapper.getAllRoles()
        res = []
        for r in AllRoles:
            res.append(RolePermissionDTO(role=r, permissions=[Permission.model_validate(p) for p in
                                                              UserRolePermissionMapper.getRolePermissions(
                                                                  r.role_id)]).model_dump())
        return ResponseModel.success(msg=AuthConsts.GET_ALL_ROLE_PERMISSION_LIST_SUCCESS, data=res)

    @staticmethod
    def updateUserStatus(userId, status):
        UserMapper.setUserStatus(userId, status)
        return ResponseModel.success(msg=AuthConsts.UPDATE_USER_STATUS_SUCCESS, data=True)

    @staticmethod
    def updateRolePermission(roleId, permissionIds: list[int]):
        # clear role's perm
        try:
            UserRolePermissionMapper.clearRolePermission(roleId)
            flag = False
            for p in permissionIds:
                try:
                    UserRolePermissionMapper.combine_role_permission(roleId, p)
                except Exception as e:
                    flag = True
            if flag:
                return ResponseModel.fail(msg=AuthConsts.SOME_PERM_UPDATE_FAIL, data=False)
            else:
                return ResponseModel.success(msg=AuthConsts.ROLE_PERM_UPDATE_SUCCESS, data=True)
        except Exception as e:
            return ResponseModel.fail(msg=AuthConsts.SOME_PERM_UPDATE_FAIL, data=False)

    @staticmethod
    def updateUserRole(userId, roleIds: list[int]):
        try:
            UserRolePermissionMapper.clearUserRole(userId)
            flag = False
            for r in roleIds:
                try:
                    UserRolePermissionMapper.combineUserWithRole(userId, r)
                except Exception as e:
                    flag = True
            if flag:
                return ResponseModel.fail(msg=AuthConsts.SOME_ROLE_UPDATE_FAILURE, data=False)
            else:
                return ResponseModel.success(msg=AuthConsts.USER_ROLE_UPDATE_SUCCESS, data=True)
        except Exception as e:
            return ResponseModel.fail(msg=AuthConsts.SOME_ROLE_UPDATE_FAILURE, data=False)

    @staticmethod
    def createRole(role: createRoleDTO):
        RoleMapper.createNewRole(role.role_name, role.description)
        return ResponseModel.success(msg=AuthConsts.CREATE_ROLE_SUCCESS, data=True)

    @staticmethod
    def deleteRole(role_id: int):
        RoleMapper.deleteRole(roleId=role_id)
        return ResponseModel.success(msg=AuthConsts.DELETE_ROLE_SUCCESS, data=True)

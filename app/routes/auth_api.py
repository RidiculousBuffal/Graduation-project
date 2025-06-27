from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_jwt_extended.exceptions import JWTExtendedException

from app.DTO.user import UserDTO, ResetPasswordDTO, createRoleDTO
from app.annotations.permissionAnnot import permission_required
from app.consts.Network import NetWorkConst
from app.consts.Permissions import Permissions
from app.consts.auth import AuthConsts
from app.models.auth import User
from app.models.response import ResponseModel
from app.service.authService import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=[NetWorkConst.POST])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return ResponseModel.fail(
            msg=AuthConsts.INFO_REQUIRED,
        ).to_dict(), 200
    user = User(**data)
    result = AuthService.login(user.username, password=data.get('password'))
    return result.to_dict(), 200


@auth_bp.route('/getEngineers', methods=[NetWorkConst.GET])
@permission_required(permissions=Permissions.USER_READ.get('permission_name'))
def getEngineers():
    result = AuthService.getAllEngineers()
    return result.to_dict(), 200


@auth_bp.route("/refresh", methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        # 解析 JWT 中的 identity
        identity = get_jwt_identity()
        if not identity:  # 如果 identity 为空，说明 token 数据可能损坏
            return ResponseModel.fail("Invalid token: identity not found").to_dict(), 401
        access_token = create_access_token(identity=identity)
        payload = {
            "access_token": access_token,
        }
        return ResponseModel.success(AuthConsts.REFRESH_SUCCESS, payload).to_dict(), 200
    except JWTExtendedException as e:  # 处理 JWT 扩展库的所有异常
        # 捕获并返回有关无效或过期的 Token 异常
        print("JWT Error:", str(e))
        return ResponseModel.fail("Invalid or expired token").to_dict(), 401
    except Exception as e:  # 捕获其他未知异常，保证接口健壮性
        return ResponseModel.fail("An unexpected error occurred").to_dict(), 500


@auth_bp.route('/register', methods=[NetWorkConst.POST])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return ResponseModel.fail(
            msg=AuthConsts.INFO_REQUIRED,
        ).to_dict(), 200
    user = User(**data)
    result = AuthService.register(user.username, data.get('password'), user.email)
    return result.to_dict(), 200


@auth_bp.post("/updateFaceInfo")
@jwt_required()
def updateFaceInfo():
    user_id = get_jwt_identity()
    faceInfo = request.get_json().get('faceInfo', None)
    if faceInfo is None:
        return ResponseModel.fail(msg=AuthConsts.FACEINFO_REQUIRED).to_dict(), 200
    else:
        return AuthService.updateUserFaceInfo(user_id, faceInfo).to_dict(), 200


@auth_bp.post("/loginByFaceInfo")
def loginByFaceInfo():
    faceInfo = request.get_json().get('faceInfo', None)
    if faceInfo is None:
        return ResponseModel.fail(msg=AuthConsts.FACEINFO_REQUIRED).to_dict(), 200
    else:
        return AuthService.loginWithFaceInfo(faceInfo).to_dict(), 200


@auth_bp.post("/updateInfo")
@permission_required(permissions=Permissions.USER_UPDATE.get('permission_name'))
def updateUserInfo():
    userInfo = request.get_json()
    userDto = UserDTO.model_validate(userInfo)
    user_id = get_jwt_identity()
    return AuthService.update_user_info(userDto, user_id).to_dict(), 200


@auth_bp.post("/forceUpdateInfo")
@permission_required(permissions=Permissions.USER_UPDATE.get('permission_name'))
def forceUpdateUserInfo():
    userInfo = request.get_json()
    userDto = UserDTO.model_validate(userInfo)
    return AuthService.force_update_userInfo(userDto, userInfo.get("user_id")).to_dict(), 200


@auth_bp.post("/updatePassword")
@jwt_required()
def updateUserPassword():
    password = request.get_json()
    password = ResetPasswordDTO.model_validate(password)
    user_id = get_jwt_identity()
    return AuthService.resetUserPassword(password, user_id).to_dict(), 200


@auth_bp.post("/forceUpdateUserPassword")
@permission_required(permissions=Permissions.USER_READ_ALL.get('permission_name'))
def forceUpdateUserPassword():
    payload = request.get_json()
    return AuthService.forceResetUserPassword(payload.get("password"), payload.get("userId")).to_dict(), 200


@auth_bp.get("/getAllUserInfo")
@permission_required(permissions=Permissions.USER_READ_ALL.get("permission_name"))
def searchAllUserInfo():
    data = request.args.to_dict()
    username = data.get("username", None)
    name = data.get("name", None)
    email = data.get("email", None)
    pageNum = int(data.get("current_page", 1))
    pageSize = int(data.get("page_size", 10))
    return AuthService.getAllUsersInfo(username, name, email, pageNum, pageSize).to_dict(), 200


@auth_bp.get("/getPermissionList")
@permission_required(permissions=Permissions.PERMISSIONS_MANAGEMENT.get("permission_name"))
def getAllPermissionList():
    return AuthService.getAllPermissions().to_dict(), 200


@auth_bp.get("/getRolePermList")
@permission_required(permissions=Permissions.PERMISSIONS_MANAGEMENT.get("permission_name"))
def getAllRoleWithPermList():
    return AuthService.getAllRolesWithTheirPermissions().to_dict(), 200


@auth_bp.post("/updateUserStatus")
@permission_required(permissions=Permissions.USER_READ_ALL.get('permission_name'))
def updateUserStatus():
    payload = request.get_json()
    return AuthService.updateUserStatus(payload.get("userId"), payload.get("status")).to_dict(), 200


@auth_bp.post("/updateRolePerm")
@permission_required(permissions=Permissions.PERMISSIONS_MANAGEMENT.get("permission_name"))
def updateRolePerm():
    payload = request.json
    return AuthService.updateRolePermission(payload.get("roleId"), payload.get("permIds")).to_dict(), 200


@auth_bp.post("/updateUserRole")
@permission_required(permissions=Permissions.USER_READ_ALL.get('permission_name'))
def updateUserRole():
    payload = request.json
    return AuthService.updateUserRole(payload.get("userId"), payload.get("roleIds")).to_dict(), 200


@auth_bp.post("/createRole")
@permission_required(permissions=Permissions.PERMISSIONS_MANAGEMENT.get("permission_name"))
def createRole():
    payload = request.json
    return AuthService.createRole(createRoleDTO.model_validate(payload)).to_dict(), 200


@auth_bp.delete("/deleteRole/<int:roleId>")
def deleteRole(roleId: int):
    return AuthService.deleteRole(roleId).to_dict(), 200

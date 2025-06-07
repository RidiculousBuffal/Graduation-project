from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_jwt_extended.exceptions import JWTExtendedException

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
@permission_required(Permissions.USER_READ.get('permission_name'))
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

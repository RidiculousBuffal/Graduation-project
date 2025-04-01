from flask import Blueprint, request

from app.consts.Network import NetWorkConst
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


@auth_bp.route('/register', methods=[NetWorkConst.POST])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return ResponseModel.fail(
            msg=AuthConsts.INFO_REQUIRED,
        ).to_dict(), 200
    user = User(**data)
    result = AuthService.register(user.username, user.password, user.email)
    return result.to_dict(),200

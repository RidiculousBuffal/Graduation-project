from flask import Blueprint, request
from pydantic import ValidationError

from app.DTO.terminals import TerminalCreateDTO, TerminalUpdateDTO
from app.annotations.permissionAnnot import permission_required
from app.consts.Network import NetWorkConst
from app.consts.Permissions import Permissions
from app.models.response import ResponseModel
from app.service.terminalService import TerminalService

terminal_bp = Blueprint('terminal', __name__)


@terminal_bp.post('/createTerminal')
@permission_required(Permissions.TERMINAL_ADD.get('permission_name'), True)
def create_terminal():
    """创建航站楼记录"""
    data = request.get_json()
    try:
        dto = TerminalCreateDTO(**data)
        result = TerminalService.create_terminal(dto)
        return result.to_dict(), 200
    except ValidationError as e:
        return ResponseModel.fail(msg=NetWorkConst.PARAMS_MISSING, data=str(e)).to_dict(), 400


@terminal_bp.get('/getTerminal/<string:terminal_id>')
@permission_required(Permissions.TERMINAL_READ.get('permission_name'), True)
def get_terminal(terminal_id: str):
    """根据ID获取航站楼记录"""
    result = TerminalService.get_terminal_by_id(terminal_id)
    return result.to_dict(), 200


@terminal_bp.post('/updateTerminal/<string:terminal_id>')
@permission_required(Permissions.TERMINAL_UPDATE.get('permission_name'), True)
def update_terminal(terminal_id: str):
    """更新航站楼记录"""
    data = request.get_json()
    try:
        dto = TerminalUpdateDTO(**data)
        result = TerminalService.update_terminal(terminal_id, dto)
        return result.to_dict(), 200
    except ValidationError as e:
        return ResponseModel.fail(msg=NetWorkConst.PARAMS_MISSING, data=str(e)).to_dict(), 400


@terminal_bp.delete('/deleteTerminal/<string:terminal_id>')
@permission_required(Permissions.TERMINAL_DELETE.get('permission_name'), True)
def delete_terminal(terminal_id: str):
    """删除航站楼记录"""
    result = TerminalService.delete_terminal(terminal_id)
    return result.to_dict(), 200


@terminal_bp.get('/searchTerminal')
@permission_required(Permissions.TERMINAL_READ.get('permission_name'), True)
def search_terminal():
    """分页查询航站楼记录"""
    args = request.args
    terminal_name = args.get('terminal_name', type=str)
    page_num = args.get('page_num', default=1, type=int)
    page_size = args.get('page_size', default=10, type=int)
    terminal_description = args.get('terminal_description', type=str)
    if not terminal_description:
        terminal_description = request.args.get('description', type=str)
    result = TerminalService.search_terminal(
        terminal_name=terminal_name,
        terminal_description=terminal_description,
        page_num=page_num,
        page_size=page_size
    )
    return result.to_dict(), 200

from flask import Blueprint, request

from app.annotations.permissionAnnot import permission_required
from app.consts.Permissions import Permissions
from app.service.dictionaryService import DictionaryService

dictionary_bp = Blueprint('dictionary', __name__)


@dictionary_bp.get('/getDictionary/<string:dict_key>')
@permission_required(Permissions.DICTIONARY_READ.get('permission_name'), True)
def get_dictionary(dict_key: str):
    """根据字典键获取字典记录，包含详细信息"""
    result = DictionaryService.get_dictionary_by_key(dict_key)
    return result.to_dict(), 200


@dictionary_bp.get('/getChildrenByParentKey/<string:parent_key>')
@permission_required(Permissions.DICTIONARY_READ.get('permission_name'), True)
def get_children_by_parent_key(parent_key: str):
    """查询某个父字典下的所有子字典"""
    result = DictionaryService.get_children_by_parent_key(parent_key)
    return result.to_dict(), 200


@dictionary_bp.get('/searchDictionary')
@permission_required(Permissions.DICTIONARY_READ.get('permission_name'), True)
def search_dictionary():
    """分页查询字典记录，支持按名称和父字典键过滤"""
    args = request.args
    dict_name = args.get('dict_name', type=str)
    parent_key = args.get('parent_key', type=str)
    page_num = args.get('page_num', default=1, type=int)
    page_size = args.get('page_size', default=10, type=int)

    result = DictionaryService.search_dictionary(
        dict_name=dict_name,
        parent_key=parent_key,
        page_num=page_num,
        page_size=page_size
    )
    return result.to_dict(), 200

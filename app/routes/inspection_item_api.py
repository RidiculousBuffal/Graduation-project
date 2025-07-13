from flask import Blueprint, request
from app.DTO.inspectionItems import InspectionItemCreateDTO, InspectionItemUpdateDTO
from app.annotations.permissionAnnot import permission_required
from app.consts.InspectionItem import InspectionItemConsts
from app.consts.Permissions import Permissions
from app.models.response import ResponseModel
from app.service.InspectionItemService import InspectionItemService

inspection_item_bp = Blueprint('inspectionitem', __name__)


@inspection_item_bp.route('/create', methods=['POST'])
@permission_required(Permissions.INSPECTION_ITEM_ADD["permission_name"])
def create_inspection_item():
    """
    创建检查项
    """
    try:
        data = request.get_json()
        item_dto = InspectionItemCreateDTO(**data)
        result = InspectionItemService.create_inspection_item(item_dto)
        return ResponseModel.success(
            msg=InspectionItemConsts.ItemInsertSuccess,
            data=result.model_dump()
        ).to_dict()
    except Exception as e:
        return ResponseModel.fail(
            f"{InspectionItemConsts.ItemInsertFail}: {str(e)}"
        ).to_dict(), 400


@inspection_item_bp.route('/getItemById/<item_id>', methods=['GET'])
@permission_required(Permissions.INSPECTION_ITEM_READ["permission_name"])
def get_inspection_item(item_id):
    """
    根据ID获取检查项详情
    """
    try:
        item = InspectionItemService.get_inspection_item(item_id)
        if not item:
            return ResponseModel.fail(
                f"{InspectionItemConsts.ItemNotFound}: {item_id}"
            ).to_dict(), 404

        return ResponseModel.success(
            msg=InspectionItemConsts.ItemFetchSuccess,
            data=item.model_dump()
        ).to_dict()
    except Exception as e:
        return ResponseModel.fail(
            f"{InspectionItemConsts.ItemFetchFail}: {str(e)}"
        ).to_dict(), 400


@inspection_item_bp.route('/updateItem/<item_id>', methods=['PUT'])
@permission_required(Permissions.INSPECTION_ITEM_UPDATE["permission_name"])
def update_inspection_item(item_id):
    """
    更新检查项
    """
    try:
        data = request.get_json()
        update_dto = InspectionItemUpdateDTO(**data)
        result = InspectionItemService.update_inspection_item(item_id, update_dto)
        if not result:
            return ResponseModel.fail(
                f"{InspectionItemConsts.ItemNotFound}: {item_id}"
            ).to_dict(), 404

        return ResponseModel.success(
            msg=InspectionItemConsts.ItemUpdateSuccess,
            data=result.model_dump()
        ).to_dict()
    except Exception as e:
        return ResponseModel.fail(
            f"{InspectionItemConsts.ItemUpdateFail}: {str(e)}"
        ).to_dict(), 400


@inspection_item_bp.route('/deleteItem/<item_id>', methods=['DELETE'])
@permission_required(Permissions.INSPECTION_ITEM_DELETE["permission_name"])
def delete_inspection_item(item_id):
    """
    删除检查项
    """
    try:
        success = InspectionItemService.delete_inspection_item(item_id)
        if not success:
            return ResponseModel.fail(
                f"{InspectionItemConsts.ItemNotFound}: {item_id}"
            ).to_dict(), 404

        return ResponseModel.success(
            msg=InspectionItemConsts.ItemDeleteSuccess
        ).to_dict()
    except Exception as e:
        return ResponseModel.fail(
            f"{InspectionItemConsts.ItemDeleteFail}: {str(e)}"
        ).to_dict(), 400


@inspection_item_bp.route('/listByInspection', methods=['GET'])
@permission_required(Permissions.INSPECTION_ITEM_READ["permission_name"])
def list_items_by_inspection():
    """
    根据 inspection_id 分页列出所有检查项
    """
    try:
        # 从请求的查询参数中获取分页信息
        inspection_id = request.args.get('inspection_id', type=str)
        page_num = request.args.get('current_page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)

        # 调用 Service 层获取分页结果
        paged_result = InspectionItemService.list_items_by_inspection(
            inspection_id=inspection_id,
            page_num=page_num,
            page_size=page_size
        )

        # 直接序列化整个分页响应 DTO
        return ResponseModel.success(
            msg=InspectionItemConsts.ItemListFetchSuccess,
            data=paged_result.model_dump()
        ).to_dict()
    except Exception as e:
        return ResponseModel.fail(
            f"{InspectionItemConsts.ItemListFetchFail}: {str(e)}"
        ).to_dict(), 400

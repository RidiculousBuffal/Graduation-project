from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity

from app.DTO.inspections import InspectionRecordCreateDTO, InspectionRecordUpdateDTO
from app.annotations.permissionAnnot import permission_required
from app.consts.InspectionConsts import InspectionConsts
from app.consts.Permissions import Permissions
from app.models.response import ResponseModel
from app.service.inspectionRecordService import InspectionRecordService

inspection_bp = Blueprint('inspection', __name__, )


@inspection_bp.route('/create', methods=['POST'])
@permission_required(Permissions.INSPECTION_ADD["permission_name"])
def create_inspection():
    """
    创建检查记录
    """
    try:
        data = request.get_json()
        inspection_data = InspectionRecordCreateDTO(**data)
        result = InspectionRecordService.create_inspection_record(inspection_data)
        return ResponseModel.success(msg=InspectionConsts.InspectionRecordInsertSuccess,
                                     data=result.model_dump()).to_dict()
    except Exception as e:
        return ResponseModel.fail(f"{InspectionConsts.InspectionRecordInsertFail}: {str(e)}").to_dict(), 400


@inspection_bp.route('/getInspectionById/<inspection_id>', methods=['GET'])
@permission_required(Permissions.INSPECTION_READ["permission_name"])
def get_inspection(inspection_id):
    """
    获取检查记录详情
    """
    try:
        inspection = InspectionRecordService.get_inspection_record(inspection_id)
        if not inspection:
            return ResponseModel.fail(f"{InspectionConsts.InspectionRecordNotFound}: {inspection_id}").to_dict(), 404
        return ResponseModel.success(msg=InspectionConsts.InspectionRecordFetchSuccess,
                                     data=inspection.model_dump()).to_dict()
    except Exception as e:
        return ResponseModel.fail(f"{InspectionConsts.InspectionRecordFetchFailed}: {str(e)}").to_dict(), 400


@inspection_bp.route('/updateInspection/<inspection_id>', methods=['PUT'])
@permission_required(Permissions.INSPECTION_UPDATE["permission_name"])
def update_inspection(inspection_id):
    """
    更新检查记录
    """
    try:
        data = request.get_json()
        update_data = InspectionRecordUpdateDTO(**data)
        result = InspectionRecordService.update_inspection_record(inspection_id, update_data)
        if not result:
            return ResponseModel.fail(f"{InspectionConsts.InspectionRecordNotFound}: {inspection_id}").to_dict(), 404
        return ResponseModel.success(msg=f'{InspectionConsts.InspectionRecordUpdateSuccess}',
                                     data=result.model_dump()).to_dict()
    except Exception as e:
        return ResponseModel.fail(f"{InspectionConsts.InspectionRecordUpdateFailed}: {str(e)}").to_dict(), 400


@inspection_bp.route('/deleteInspection/<inspection_id>', methods=['DELETE'])
@permission_required(Permissions.INSPECTION_DELETE["permission_name"])
def delete_inspection(inspection_id):
    """
    删除检查记录
    """
    try:
        result = InspectionRecordService.delete_inspection_record(inspection_id)
        if not result:
            return ResponseModel.fail(f"{InspectionConsts.InspectionRecordNotFound}: {inspection_id}").to_dict(), 404
        return ResponseModel.success(msg=f"{InspectionConsts.InspectionRecordDeleteSuccess}").to_dict()
    except Exception as e:
        return ResponseModel.fail(f"删除检查记录失败: {str(e)}").to_dict(), 400


@inspection_bp.route('/getMyInspections', methods=['GET'])
@permission_required(Permissions.INSPECTION_READ_SELF["permission_name"])
def getMyInspections():
    """
    搜索检查记录
    """
    try:
        data = request.args.to_dict()
        # 获取分页参数
        page_num = int(data.get('current_page', 1))
        page_size = int(data.get('page_size', 10))

        # 获取查询参数
        task_id = data.get('task_id')
        executor_id = get_jwt_identity()
        inspection_status = data.get('inspection_status')
        reference_image_id = data.get('reference_image_id')
        flight_id = data.get('flight_id')
        aircraft_id = data.get('aircraft_id')
        executor_name = data.get('executor_name')
        start_time_from = data.get('start_time_from')
        start_time_to = data.get('start_time_to')
        end_time_from = data.get('end_time_from')
        end_time_to = data.get('end_time_to')

        result = InspectionRecordService.search_inspection_records(
            task_id=task_id,
            executor_id=executor_id,
            inspection_status=inspection_status,
            reference_image_id=reference_image_id,
            flight_id=flight_id,
            aircraft_id=aircraft_id,
            executor_name=executor_name,
            start_time_from=start_time_from,
            start_time_to=start_time_to,
            end_time_from=end_time_from,
            end_time_to=end_time_to,
            page_num=page_num,
            page_size=page_size
        )

        return ResponseModel.success(msg=InspectionConsts.InspectionRecordFetchSuccess,
                                     data=result.model_dump()).to_dict()
    except Exception as e:
        return ResponseModel.fail(f"{InspectionConsts.InspectionRecordFetchFailed}: {str(e)}").to_dict(), 400


@inspection_bp.route('/search', methods=['GET'])
@permission_required(Permissions.INSPECTION_READ["permission_name"])
def search_inspections():
    """
    搜索检查记录
    """
    try:
        data = request.args.to_dict()
        # 获取分页参数
        page_num = int(data.get('current_page', 1))
        page_size = int(data.get('page_size', 10))

        # 获取查询参数
        task_id = data.get('task_id')
        executor_id = data.get('executor_id')
        inspection_status = data.get('inspection_status')
        reference_image_id = data.get('reference_image_id')
        flight_id = data.get('flight_id')
        aircraft_id = data.get('aircraft_id')
        executor_name = data.get('executor_name')
        start_time_from = data.get('start_time_from')
        start_time_to = data.get('start_time_to')
        end_time_from = data.get('end_time_from')
        end_time_to = data.get('end_time_to')

        result = InspectionRecordService.search_inspection_records(
            task_id=task_id,
            executor_id=executor_id,
            inspection_status=inspection_status,
            reference_image_id=reference_image_id,
            flight_id=flight_id,
            aircraft_id=aircraft_id,
            executor_name=executor_name,
            start_time_from=start_time_from,
            start_time_to=start_time_to,
            end_time_from=end_time_from,
            end_time_to=end_time_to,
            page_num=page_num,
            page_size=page_size
        )

        return ResponseModel.success(msg=InspectionConsts.InspectionRecordFetchSuccess,
                                     data=result.model_dump()).to_dict()
    except Exception as e:
        return ResponseModel.fail(f"{InspectionConsts.InspectionRecordFetchFailed}: {str(e)}").to_dict(), 400

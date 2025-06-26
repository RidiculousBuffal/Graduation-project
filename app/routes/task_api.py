from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity

from app.DTO.tasks import TaskCreateDTO, TaskUpdateDTO
from app.annotations.permissionAnnot import permission_required
from app.consts.Permissions import Permissions
from app.consts.Task import TaskConsts
from app.models.response import ResponseModel
from app.service.taskService import TaskService

task_bp = Blueprint('task', __name__)


@task_bp.route('/create', methods=['POST'])
@permission_required(Permissions.TASK_ADD["permission_name"])
def create_task():
    """
    创建任务
    """
    try:
        data = request.get_json()
        data['admin_id'] = get_jwt_identity()
        task_data = TaskCreateDTO(**data)
        result = TaskService.create_task(task_data)
        return ResponseModel.success(msg=TaskConsts.TASK_CREATE_SUCCESS, data=result.model_dump()).to_dict()
    except Exception as e:
        return ResponseModel.fail(f"{TaskConsts.TASK_CREATE_FAIL}: {str(e)}").to_dict(), 400


@task_bp.route('/getTaskById/<task_id>', methods=['GET'])
@permission_required(Permissions.TASK_READ["permission_name"])
def get_task(task_id):
    """
    获取任务详情
    """
    try:
        task = TaskService.get_task(task_id)
        if not task:
            return ResponseModel.fail(f"{TaskConsts.TASK_NOT_FOUND}: {task_id}").to_dict(), 404
        return ResponseModel.success(msg=TaskConsts.TASK_FIND_SUCCESS, data=task.model_dump()).to_dict()
    except Exception as e:
        return ResponseModel.fail(f"{TaskConsts.TASK_FETCH_FAIL}: {str(e)}").to_dict(), 400


@task_bp.route('/updateTask/<task_id>', methods=['PUT'])
@permission_required(Permissions.TASK_UPDATE["permission_name"])
def update_task(task_id):
    """
    更新任务
    """
    try:
        data = request.get_json()
        update_data = TaskUpdateDTO(**data)
        result = TaskService.update_task(task_id, update_data)
        if not result:
            return ResponseModel.fail(f"{TaskConsts.TASK_NOT_FOUND}: {task_id}").to_dict(), 404
        return ResponseModel.success(msg=TaskConsts.TASK_UPDATE_SUCCESS, data=result.model_dump()).to_dict()
    except Exception as e:
        return ResponseModel.fail(f"{TaskConsts.TASK_UPDATE_FAIL}: {str(e)}").to_dict(), 400


@task_bp.route('/deleteTask/<task_id>', methods=['DELETE'])
@permission_required(Permissions.TASK_DELETE["permission_name"])
def delete_task(task_id):
    """
    删除任务
    """
    try:
        result = TaskService.delete_task(task_id)
        if not result:
            return ResponseModel.fail(f"{TaskConsts.TASK_NOT_FOUND}: {task_id}").to_dict(), 404
        return ResponseModel.success(msg=f'{TaskConsts.TASK_DELETE_SUCCESS}', data=True).to_dict()
    except Exception as e:
        return ResponseModel.fail(f"{TaskConsts.TASK_DELETE_FAIL}: {str(e)}").to_dict(), 400


@task_bp.route('/search', methods=['GET'])
@permission_required(Permissions.TASK_READ["permission_name"])
def search_tasks():
    try:
        data = request.args.to_dict()
        # 获取分页参数
        page_num = int(data.get('page_num', 1))
        page_size = int(data.get('page_size', 10))

        # 获取查询参数
        flight_id = data.get('flight_id')
        admin_id = data.get('admin_id')
        task_status = data.get('task_status')
        aircraft_id = data.get('aircraft_id')
        aircraft_name = data.get('aircraft_name')
        admin_name = data.get('admin_name')
        estimated_start_from = data.get('estimated_start_from')
        estimated_start_to = data.get('estimated_start_to')
        estimated_end_from = data.get('estimated_end_from')
        estimated_end_to = data.get('estimated_end_to')
        actual_start_from = data.get('actual_start_from')
        actual_start_to = data.get('actual_start_to')
        actual_end_to = data.get('actual_end_to')
        actual_end_from = data.get('actual_end_from')
        result = TaskService.search_tasks(
            flight_id=flight_id,
            admin_id=admin_id,
            task_status=task_status,
            aircraft_id=aircraft_id,
            aircraft_name=aircraft_name,
            admin_name=admin_name,
            estimated_start_from=estimated_start_from,
            estimated_start_to=estimated_start_to,
            estimated_end_from=estimated_end_from,
            estimated_end_to=estimated_end_to,
            actual_start_from=actual_start_from,
            actual_start_to=actual_start_to,
            actual_end_from=actual_end_from,
            actual_end_to=actual_end_to,
            page_num=page_num,
            page_size=page_size
        )

        return ResponseModel.success(msg=TaskConsts.TASK_FIND_SUCCESS, data=result.model_dump()).to_dict()
    except Exception as e:
        return ResponseModel.fail(f"{TaskConsts.TASK_SEARCH_FAIL}: {str(e)}").to_dict(), 400

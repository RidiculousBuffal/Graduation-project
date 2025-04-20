from flask import Blueprint, request
from pydantic import ValidationError

from app.DTO.flights import FlightCreateDTO, FlightUpdateDTO
from app.annotations.permissionAnnot import permission_required
from app.consts.Network import NetWorkConst
from app.consts.Permissions import Permissions
from app.models.response import ResponseModel
from app.service.flightService import FlightService

flight_bp = Blueprint('flight', __name__)

# Flight (航班) 相关接口
@flight_bp.post('/createFlight')
@permission_required(Permissions.FLIGHT_ADD.get('permission_name'), True)
def create_flight():
    """创建航班记录"""
    data = request.get_json()
    try:
        dto = FlightCreateDTO(**data)
        result = FlightService.create_flight(dto)
        return result.to_dict(), 200
    except ValidationError as e:
        return ResponseModel.fail(msg=NetWorkConst.PARAMS_MISSING, data=str(e)).to_dict(), 400

@flight_bp.get('/getFlight/<string:flight_id>')
@permission_required(Permissions.FLIGHT_READ.get('permission_name'), True)
def get_flight(flight_id: str):
    """根据ID获取航班记录，包含详细信息"""
    result = FlightService.get_flight_by_id(flight_id)
    return result.to_dict(), 200

@flight_bp.post('/updateFlight/<string:flight_id>')
@permission_required(Permissions.FLIGHT_UPDATE.get('permission_name'), True)
def update_flight(flight_id: str):
    """更新航班记录"""
    data = request.get_json()
    try:
        dto = FlightUpdateDTO(**data)
        result = FlightService.update_flight(flight_id, dto)
        return result.to_dict(), 200
    except ValidationError as e:
        return ResponseModel.fail(msg=NetWorkConst.PARAMS_MISSING, data=str(e)).to_dict(), 400

@flight_bp.delete('/deleteFlight/<string:flight_id>')
@permission_required(Permissions.FLIGHT_DELETE.get('permission_name'), True)
def delete_flight(flight_id: str):
    """删除航班记录"""
    result = FlightService.delete_flight(flight_id)
    return result.to_dict(), 200

@flight_bp.get('/searchFlight')
@permission_required(Permissions.FLIGHT_READ.get('permission_name'), True)
def search_flight():
    """分页查询航班记录，包含详细信息，支持按航站楼名称、飞机名称及时间段查询"""
    args = request.args
    aircraft_id = args.get('aircraft_id', type=str)
    terminal_id = args.get('terminal_id', type=str)
    flight_status = args.get('flight_status', type=str)
    health_status = args.get('health_status', type=str)
    approval_status = args.get('approval_status', type=str)
    aircraft_name = args.get('aircraft_name', type=str)  # 新增：按飞机名称查询
    terminal_name = args.get('terminal_name', type=str)  # 新增：按航站楼名称查询
    estimated_departure_start = args.get('estimated_departure_start', type=str)  # 新增：预计起飞起始时间
    estimated_departure_end = args.get('estimated_departure_end', type=str)      # 新增：预计起飞结束时间
    estimated_arrival_start = args.get('estimated_arrival_start', type=str)      # 新增：预计到达起始时间
    estimated_arrival_end = args.get('estimated_arrival_end', type=str)          # 新增：预计到达结束时间
    actual_departure_start = args.get('actual_departure_start', type=str)        # 新增：实际起飞起始时间
    actual_departure_end = args.get('actual_departure_end', type=str)            # 新增：实际起飞结束时间
    actual_arrival_start = args.get('actual_arrival_start', type=str)            # 新增：实际到达起始时间
    actual_arrival_end = args.get('actual_arrival_end', type=str)                # 新增：实际到达结束时间
    page_num = args.get('page_num', default=1, type=int)
    page_size = args.get('page_size', default=10, type=int)

    result = FlightService.search_flight(
        aircraft_id=aircraft_id,
        terminal_id=terminal_id,
        flight_status=flight_status,
        health_status=health_status,
        approval_status=approval_status,
        aircraft_name=aircraft_name,
        terminal_name=terminal_name,
        estimated_departure_start=estimated_departure_start,
        estimated_departure_end=estimated_departure_end,
        estimated_arrival_start=estimated_arrival_start,
        estimated_arrival_end=estimated_arrival_end,
        actual_departure_start=actual_departure_start,
        actual_departure_end=actual_departure_end,
        actual_arrival_start=actual_arrival_start,
        actual_arrival_end=actual_arrival_end,
        page_num=page_num,
        page_size=page_size
    )
    return result.to_dict(), 200
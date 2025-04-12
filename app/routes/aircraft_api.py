from flask import Blueprint, request
from pydantic import ValidationError

from app.DTO.aircrafts import (
    AircraftCreateDTO, AircraftUpdateDTO,
    AircraftTypeCreateDTO, AircraftTypeUpdateDTO
)
from app.annotations.permissionAnnot import permission_required
from app.consts.Network import NetWorkConst
from app.consts.Permissions import Permissions
from app.models.response import ResponseModel
from app.service.aircraftService import AircraftService

aircraft_bp = Blueprint('aircraft', __name__)


# Aircraft 相关接口
@aircraft_bp.post('/createAircraft')
@permission_required(Permissions.AIRCRAFT_ADD.get('permission_name'), True)
def create_aircraft():
    data = request.get_json()
    try:
        dto = AircraftCreateDTO(**data)
        result = AircraftService.create_aircraft(dto)
        return result.to_dict(), 200
    except ValidationError as e:
        return ResponseModel.fail(msg=NetWorkConst.PARAMS_MISSING, data=str(e)).to_dict(), 400


@aircraft_bp.get('/getAircraft/<string:aircraft_id>')
@permission_required(Permissions.AIRCRAFT_READ.get('permission_name'), True)
def get_aircraft(aircraft_id: str):
    result = AircraftService.get_aircraft_by_id(aircraft_id)
    return result.to_dict(), 200


@aircraft_bp.post('/updateAircraft/<string:aircraft_id>')
@permission_required(Permissions.AIRCRAFT_UPDATE.get('permission_name'), True)
def update_aircraft(aircraft_id: str):
    data = request.get_json()
    try:
        dto = AircraftUpdateDTO(**data)
        result = AircraftService.update_aircraft(aircraft_id, dto)
        return result.to_dict(), 200
    except ValidationError as e:
        return ResponseModel.fail(msg=NetWorkConst.PARAMS_MISSING, data=str(e)).to_dict(), 400


@aircraft_bp.delete('/deleteAircraft/<string:aircraft_id>')
@permission_required(Permissions.AIRCRAFT_DELETE.get('permission_name'), True)
def delete_aircraft(aircraft_id: str):
    result = AircraftService.delete_aircraft(aircraft_id)
    return result.to_dict(), 200


@aircraft_bp.get('/searchAircraft')
@permission_required(Permissions.AIRCRAFT_READ.get('permission_name'), True)
def search_aircraft():
    args = request.args
    aircraft_name = args.get('aircraft_name', type=str)
    aircraft_age = args.get('aircraft_age', type=str)
    aircraft_type_name = args.get('aircraft_type_name', type=str)
    page_num = args.get('page_num', default=1, type=int)
    page_size = args.get('page_size', default=10, type=int)

    result = AircraftService.search_aircraft(
        aircraft_name=aircraft_name,
        aircraft_age=aircraft_age,
        aircraft_type_name=aircraft_type_name,
        page_num=page_num,
        page_size=page_size
    )
    return result.to_dict(), 200


# AircraftType 相关接口
@aircraft_bp.post('/createAircraftType')
@permission_required(Permissions.AIRCRAFT_TYPE_ADD.get('permission_name'), True)
def create_aircraft_type():
    data = request.get_json()
    try:
        dto = AircraftTypeCreateDTO(**data)
        result = AircraftService.create_aircraft_type(dto)
        return result.to_dict(), 200
    except ValidationError as e:
        return ResponseModel.fail(msg=NetWorkConst.PARAMS_MISSING, data=str(e)).to_dict(), 400


@aircraft_bp.get('/getAircraftType/<string:typeid>')
@permission_required(Permissions.AIRCRAFT_READ.get('permission_name'), True)
def get_aircraft_type(typeid: str):
    result = AircraftService.get_aircraft_type_by_id(typeid)
    return result.to_dict(), 200


@aircraft_bp.post('/updateAircraftType/<string:typeid>')
@permission_required(Permissions.AIRCRAFT_TYPE_UPDATE.get('permission_name'), True)
def update_aircraft_type(typeid: str):
    data = request.get_json()
    try:
        dto = AircraftTypeUpdateDTO(**data)
        result = AircraftService.update_aircraft_type(typeid, dto)
        return result.to_dict(), 200
    except ValidationError as e:
        return ResponseModel.fail(msg=NetWorkConst.PARAMS_MISSING, data=str(e)).to_dict(), 400


@aircraft_bp.delete('/deleteAircraftType/<string:typeid>')
@permission_required(Permissions.AIRCRAFT_TYPE_DELETE.get('permission_name'), True)
def delete_aircraft_type(typeid: str):
    result = AircraftService.delete_aircraft_type(typeid)
    return result.to_dict(), 200


@aircraft_bp.get('/searchAircraftType')
@permission_required(Permissions.AIRCRAFT_TYPE_READ.get('permission_name'), True)
def search_aircraft_type():
    args = request.args
    type_name = args.get('type_name', type=str)
    page_num = args.get('page_num', default=1, type=int)
    page_size = args.get('page_size', default=10, type=int)

    result = AircraftService.search_aircraft_type(
        type_name=type_name,
        page_num=page_num,
        page_size=page_size
    )
    return result.to_dict(), 200

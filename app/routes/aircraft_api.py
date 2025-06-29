from flask import Blueprint, request
from pydantic import ValidationError

from app.DTO.aircrafts import (
    AircraftCreateDTO, AircraftUpdateDTO,
    AircraftTypeCreateDTO, AircraftTypeUpdateDTO, AircraftReferenceImageUpdateDTO, AircraftReferenceImageCreateDTO
)
from app.annotations.loggingAnnot import logging_to_blockchain
from app.annotations.permissionAnnot import permission_required
from app.consts.Network import NetWorkConst
from app.consts.Permissions import Permissions
from app.models.response import ResponseModel
from app.service.aircraftReferenceImageService import AircraftReferenceImageService
from app.service.aircraftService import AircraftService

aircraft_bp = Blueprint('aircraft', __name__)


# Aircraft 相关接口
@aircraft_bp.post('/createAircraft')
@permission_required(Permissions.AIRCRAFT_ADD.get('permission_name'), True)
# @logging_to_blockchain("createAircraft")
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
# @logging_to_blockchain(event_name='SEARCH_AIRCRAFT')  ##测试阶段等下测试区块链
def search_aircraft():
    args = request.args
    aircraft_name = args.get('aircraft_name', type=str)
    aircraft_age = args.get('aircraft_age', type=int) or args.get('age', type=int)
    aircraft_type_name = args.get('aircraft_type_name', type=str) or args.get('type_name', type=str)
    page_num = args.get('current_page', default=1, type=int)
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
    description = args.get('description', type=str)
    page_num = args.get('current_page', default=1, type=int)
    page_size = args.get('page_size', default=10, type=int)

    result = AircraftService.search_aircraft_type(
        type_name=type_name,
        page_num=page_num,
        page_size=page_size,
        description=description
    )
    return result.to_dict(), 200


@aircraft_bp.post('/createAircraftImage')
@permission_required(Permissions.AIRCRAFT_IMAGE_ADD.get('permission_name', ''), True)
def create_aircraft_image():
    """创建飞机参考图片"""
    data = request.get_json()
    try:
        dto = AircraftReferenceImageCreateDTO(**data)
        result = AircraftReferenceImageService.create_image(dto)
        return result.to_dict(), 200
    except ValidationError as e:
        return ResponseModel.fail(msg=NetWorkConst.PARAMS_MISSING, data=str(e)).to_dict(), 400


@aircraft_bp.get('/getAircraftImage/<string:image_id>')
@permission_required(Permissions.AIRCRAFT_IMAGE_READ.get('permission_name', ''), True)
def get_aircraft_image(image_id: str):
    """根据ID获取飞机参考图片"""
    result = AircraftReferenceImageService.get_image_by_id(image_id)
    return result.to_dict(), 200


@aircraft_bp.post('/updateAircraftImage/<string:image_id>')
@permission_required(Permissions.AIRCRAFT_IMAGE_UPDATE.get('permission_name', ''), True)
def update_aircraft_image(image_id: str):
    """更新飞机参考图片"""
    data = request.get_json()
    try:
        dto = AircraftReferenceImageUpdateDTO(**data)
        result = AircraftReferenceImageService.update_image(image_id, dto)
        return result.to_dict(), 200
    except ValidationError as e:
        return ResponseModel.fail(msg=NetWorkConst.PARAMS_MISSING, data=str(e)).to_dict(), 400


@aircraft_bp.delete('/deleteAircraftImage/<string:image_id>')
@permission_required(Permissions.AIRCRAFT_IMAGE_DELETE.get('permission_name', ''), True)
def delete_aircraft_image(image_id: str):
    """删除飞机参考图片"""
    result = AircraftReferenceImageService.delete_image(image_id)
    return result.to_dict(), 200


@aircraft_bp.get('/searchAircraftImage')
@permission_required(Permissions.AIRCRAFT_IMAGE_READ.get('permission_name', ''), True)
def search_aircraft_image():
    """分页查询飞机参考图片"""
    args = request.args
    image_name = args.get('image_name', type=str)
    aircraft_id = args.get('aircraft_id', type=str)
    aircraft_name = args.get('aircraft_name', type=str)
    page_num = args.get('current_page', default=1, type=int)
    page_size = args.get('page_size', default=10, type=int)

    result = AircraftReferenceImageService.search_image(
        image_name=image_name,
        aircraft_id=aircraft_id,
        aircraft_name=aircraft_name,
        page_num=page_num,
        page_size=page_size
    )
    return result.to_dict(), 200

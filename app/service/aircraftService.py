from typing import Optional

from sqlalchemy.exc import IntegrityError

from app.DTO.aircrafts import (
    AircraftCreateDTO, AircraftUpdateDTO, AircraftDTO,
    AircraftTypeCreateDTO, AircraftTypeUpdateDTO, AircraftTypeDTO
)
from app.consts.Aircrafts import AircraftConsts
from app.mapper.aircraft.aircraftMapper import AircraftMapper
from app.mapper.aircraft.aircraftTypeMapper import AircraftTypeMapper
from app.models.response import ResponseModel


class AircraftService:
    # Aircraft 相关服务方法
    @staticmethod
    def create_aircraft(aircraft_data: AircraftCreateDTO) -> ResponseModel:
        """创建飞机记录"""
        # 参数校验
        if not aircraft_data.aircraft_name or not aircraft_data.typeid:
            return ResponseModel.fail(
                msg=AircraftConsts.INVALID_PLANE_DATA,
                data={"error": "飞机名称和类型ID不能为空"}
            )

        try:
            result = AircraftMapper.create(aircraft_data)
            return ResponseModel.success(
                msg=AircraftConsts.ADD_PLANE_SUCCESS,
                data=result.model_dump()
            )
        except IntegrityError as e:
            return ResponseModel.fail(
                msg=AircraftConsts.GET_TYPE_NOT_FOUND,
                data={"error": str(e)}
            )
        except Exception as e:
            return ResponseModel.fail(
                msg=AircraftConsts.ADD_PLANE_ERROR,
                data={"error": str(e)}
            )

    @staticmethod
    def get_aircraft_by_id(aircraft_id: str) -> ResponseModel:
        """根据ID获取飞机记录"""
        if not aircraft_id:
            return ResponseModel.fail(
                msg=AircraftConsts.INVALID_PLANE_DATA,
                data={"error": "飞机ID不能为空"}
            )

        result: Optional[AircraftDTO] = AircraftMapper.get_by_id(aircraft_id)
        if result:
            return ResponseModel.success(
                msg=AircraftConsts.GET_PLANE_SUCCESS,
                data=result.model_dump()
            )
        return ResponseModel.fail(
            msg=AircraftConsts.GET_PLANE_NOT_FOUND,
            data={"error": f"未找到ID为{aircraft_id}的飞机"}
        )

    @staticmethod
    def update_aircraft(aircraft_id: str, update_data: AircraftUpdateDTO) -> ResponseModel:
        """更新飞机记录"""
        if not aircraft_id:
            return ResponseModel.fail(
                msg=AircraftConsts.INVALID_PLANE_DATA,
                data={"error": "飞机ID不能为空"}
            )

        try:
            result: Optional[AircraftDTO] = AircraftMapper.update(aircraft_id, update_data)
            if result:
                return ResponseModel.success(
                    msg=AircraftConsts.UPDATE_PLANE_SUCCESS,
                    data=result.model_dump()
                )
            return ResponseModel.fail(
                msg=AircraftConsts.UPDATE_PLANE_ERROR,
                data={"error": f"未找到ID为{aircraft_id}的飞机或更新失败"}
            )
        except IntegrityError as e:
            return ResponseModel.fail(
                msg=AircraftConsts.GET_TYPE_NOT_FOUND,
                data={"error": str(e)}
            )
        except Exception as e:
            return ResponseModel.fail(
                msg=AircraftConsts.UPDATE_PLANE_ERROR,
                data={"error": str(e)}
            )

    @staticmethod
    def delete_aircraft(aircraft_id: str) -> ResponseModel:
        """删除飞机记录"""
        if not aircraft_id:
            return ResponseModel.fail(
                msg=AircraftConsts.INVALID_PLANE_DATA,
                data={"error": "飞机ID不能为空"}
            )

        success = AircraftMapper.delete(aircraft_id)
        if success:
            return ResponseModel.success(
                msg=AircraftConsts.DELETE_PLANE_SUCCESS,
                data=None
            )
        return ResponseModel.fail(
            msg=AircraftConsts.DELETE_PLANE_ERROR,
            data={"error": f"未找到ID为{aircraft_id}的飞机或删除失败"}
        )

    @staticmethod
    def search_aircraft(
            aircraft_name: Optional[str] = None,
            aircraft_age: Optional[str] = None,
            aircraft_type_name: Optional[str] = None,
            page_num: int = 1,
            page_size: int = 10
    ) -> ResponseModel:
        """分页查询飞机记录"""
        if page_num < 1 or page_size < 1:
            return ResponseModel.fail(
                msg=AircraftConsts.INVALID_PLANE_DATA,
                data={"error": "页码和每页大小必须大于0"}
            )

        result = AircraftMapper.searchAircraft(
            aircraftName=aircraft_name,
            aircraftAge=aircraft_age,
            aircraftTypeName=aircraft_type_name,
            pageNum=page_num,
            pageSize=page_size
        )
        return ResponseModel.success(
            msg=AircraftConsts.SEARCH_PLANE_SUCCESS,
            data=result.model_dump()
        )

    # AircraftType 相关服务方法
    @staticmethod
    def create_aircraft_type(type_data: AircraftTypeCreateDTO) -> ResponseModel:
        """创建飞机类型记录"""
        # 参数校验
        if not type_data.type_name:
            return ResponseModel.fail(
                msg=AircraftConsts.INVALID_TYPE_DATA,
                data={"error": "飞机类型名称不能为空"}
            )

        try:
            type_ = AircraftTypeMapper.search(type_data.type_name)
            if len(type_.data) > 0:
                return ResponseModel.fail(
                    msg=AircraftConsts.AIRCRAFT_TYPE_ALREADY_EXISTS
                )
            result: AircraftTypeDTO = AircraftTypeMapper.create(type_data)
            return ResponseModel.success(
                msg=AircraftConsts.ADD_TYPE_SUCCESS,
                data=result.model_dump()
            )
        except Exception as e:
            return ResponseModel.fail(
                msg=AircraftConsts.ADD_TYPE_ERROR,
                data={"error": str(e)}
            )

    @staticmethod
    def get_aircraft_type_by_id(typeid: str) -> ResponseModel:
        """根据ID获取飞机类型记录"""
        if not typeid:
            return ResponseModel.fail(
                msg=AircraftConsts.INVALID_TYPE_DATA,
                data={"error": "飞机类型ID不能为空"}
            )
        result: Optional[AircraftTypeDTO] = AircraftTypeMapper.get_by_id(typeid)
        if result:
            return ResponseModel.success(
                msg=AircraftConsts.GET_TYPE_SUCCESS,
                data=result.model_dump()
            )
        return ResponseModel.fail(
            msg=AircraftConsts.GET_TYPE_NOT_FOUND,
            data={"error": f"未找到ID为{typeid}的飞机类型"}
        )

    @staticmethod
    def update_aircraft_type(typeid: str, update_data: AircraftTypeUpdateDTO) -> ResponseModel:
        """更新飞机类型记录"""
        if not typeid:
            return ResponseModel.fail(
                msg=AircraftConsts.INVALID_TYPE_DATA,
                data={"error": "飞机类型ID不能为空"}
            )
        if update_data.type_name:
            type_ = AircraftTypeMapper.search(update_data.type_name)
            if len(type_.data) > 0 and type_.data[0].typeid != typeid:
                return ResponseModel.fail(
                    msg=AircraftConsts.AIRCRAFT_TYPE_ALREADY_EXISTS
                )
        result: Optional[AircraftTypeDTO] = AircraftTypeMapper.update(typeid, update_data)
        if result:
            return ResponseModel.success(
                msg=AircraftConsts.UPDATE_TYPE_SUCCESS,
                data=result.model_dump()
            )
        return ResponseModel.fail(
            msg=AircraftConsts.UPDATE_TYPE_ERROR,
            data={"error": f"未找到ID为{typeid}的飞机类型或更新失败"}
        )

    @staticmethod
    def delete_aircraft_type(typeid: str) -> ResponseModel:
        """删除飞机类型记录"""
        if not typeid:
            return ResponseModel.fail(
                msg=AircraftConsts.INVALID_TYPE_DATA,
                data={"error": "飞机类型ID不能为空"}
            )

        success = AircraftTypeMapper.delete(typeid)
        if success:
            return ResponseModel.success(
                msg=AircraftConsts.DELETE_TYPE_SUCCESS,
                data=True
            )
        return ResponseModel.fail(
            msg=AircraftConsts.DELETE_TYPE_ERROR,
            data={"error": f"未找到ID为{typeid}的飞机类型或删除失败"}
        )

    @staticmethod
    def search_aircraft_type(
            type_name: Optional[str] = None,
            description: Optional[str] = None,
            page_num: int = 1,
            page_size: int = 10
    ) -> ResponseModel:

        """分页查询飞机类型记录"""
        if page_num < 1 or page_size < 1:
            return ResponseModel.fail(
                msg=AircraftConsts.INVALID_TYPE_DATA,
                data={"error": "页码和每页大小必须大于0"}
            )

        result = AircraftTypeMapper.search(
            type_name=type_name,
            pageNum=page_num,
            pageSize=page_size,
            description=description,
            fuzzySearch=True
        )
        return ResponseModel.success(
            msg=AircraftConsts.SEARCH_TYPE_SUCCESS,
            data=result.model_dump()
        )

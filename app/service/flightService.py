# app/services/flightService.py
from typing import Optional

from sqlalchemy.exc import IntegrityError

from app.DTO.flights import FlightCreateDTO, FlightUpdateDTO, FlightDTO, FlightDetailDTO
from app.consts.Flight import FlightConsts
from app.mapper.flight.flightMapper import FlightMapper
from app.models.response import ResponseModel


class FlightService:
    @staticmethod
    def create_flight(flight_data: FlightCreateDTO) -> ResponseModel:
        """创建航班记录"""
        # 参数校验
        if not flight_data.aircraft_id:
            return ResponseModel.fail(
                msg=FlightConsts.INVALID_FLIGHT_DATA,
                data={"error": "飞机ID不能为空"}
            )

        try:
            result = FlightMapper.create(flight_data)
            return ResponseModel.success(
                msg=FlightConsts.ADD_FLIGHT_SUCCESS,
                data=result.model_dump()
            )
        except IntegrityError as e:
            return ResponseModel.fail(
                msg=FlightConsts.ADD_FLIGHT_ERROR,
                data={"error": "添加失败,可能是对应航站楼和飞机id不正确导致的"}
            )
        except Exception as e:
            return ResponseModel.fail(
                msg=FlightConsts.ADD_FLIGHT_ERROR,
                data={"error": str(e)}
            )

    @staticmethod
    def get_flight_by_id(flight_id: str) -> ResponseModel:
        """根据ID获取航班记录，包含详细信息"""
        if not flight_id:
            return ResponseModel.fail(
                msg=FlightConsts.INVALID_FLIGHT_DATA,
                data={"error": "航班ID不能为空"}
            )

        result: Optional[FlightDetailDTO] = FlightMapper.get_by_id(flight_id)
        if result:
            return ResponseModel.success(
                msg=FlightConsts.GET_FLIGHT_SUCCESS,
                data=result.model_dump()
            )
        return ResponseModel.fail(
            msg=FlightConsts.GET_FLIGHT_NOT_FOUND,
            data={"error": f"未找到ID为{flight_id}的航班"}
        )

    @staticmethod
    def update_flight(flight_id: str, update_data: FlightUpdateDTO) -> ResponseModel:
        """更新航班记录"""
        if not flight_id:
            return ResponseModel.fail(
                msg=FlightConsts.INVALID_FLIGHT_DATA,
                data={"error": "航班ID不能为空"}
            )

        try:
            result: Optional[FlightDTO] = FlightMapper.update(flight_id, update_data)
            if result:
                return ResponseModel.success(
                    msg=FlightConsts.UPDATE_FLIGHT_SUCCESS,
                    data=result.model_dump()
                )
            return ResponseModel.fail(
                msg=FlightConsts.UPDATE_FLIGHT_ERROR,
                data={"error": f"未找到ID为{flight_id}的航班或更新失败"}
            )
        except IntegrityError as e:
            return ResponseModel.fail(
                msg=FlightConsts.UPDATE_FLIGHT_ERROR,
                data={"error": str(e)}
            )
        except Exception as e:
            return ResponseModel.fail(
                msg=FlightConsts.UPDATE_FLIGHT_ERROR,
                data={"error": str(e)}
            )

    @staticmethod
    def delete_flight(flight_id: str) -> ResponseModel:
        """删除航班记录"""
        if not flight_id:
            return ResponseModel.fail(
                msg=FlightConsts.INVALID_FLIGHT_DATA,
                data={"error": "航班ID不能为空"}
            )

        success = FlightMapper.delete(flight_id)
        if success:
            return ResponseModel.success(
                msg=FlightConsts.DELETE_FLIGHT_SUCCESS,
                data=None
            )
        return ResponseModel.fail(
            msg=FlightConsts.DELETE_FLIGHT_ERROR,
            data={"error": f"未找到ID为{flight_id}的航班或删除失败"}
        )

    @staticmethod
    def search_flight(
            aircraft_id: Optional[str] = None,
            terminal_id: Optional[str] = None,
            flight_status: Optional[str] = None,
            health_status: Optional[str] = None,
            approval_status: Optional[str] = None,
            page_num: int = 1,
            page_size: int = 10
    ) -> ResponseModel:
        """分页查询航班记录，包含详细信息"""
        if page_num < 1 or page_size < 1:
            return ResponseModel.fail(
                msg=FlightConsts.INVALID_FLIGHT_DATA,
                data={"error": "页码和每页大小必须大于0"}
            )

        result = FlightMapper.search(
            aircraft_id=aircraft_id,
            terminal_id=terminal_id,
            flight_status=flight_status,
            health_status=health_status,
            approval_status=approval_status,
            pageNum=page_num,
            pageSize=page_size
        )
        return ResponseModel.success(
            msg=FlightConsts.SEARCH_FLIGHT_SUCCESS,
            data=result.model_dump()
        )

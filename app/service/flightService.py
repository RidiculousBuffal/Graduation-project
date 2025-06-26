from typing import Optional

from sqlalchemy.exc import IntegrityError

from app.DTO.flights import FlightCreateDTO, FlightUpdateDTO, FlightDTO, FlightDetailDTO
from app.consts.Flight import FlightConsts
from app.exceptions.flights import FlightTimeConflictError, FlightTimestampOrderError, FlightActualVsEstimatedError
from app.mapper.flight.flightMapper import FlightMapper
from app.models.response import ResponseModel


class FlightService:
    @staticmethod
    def create_flight(flight_data: FlightCreateDTO) -> ResponseModel:
        """创建航班记录"""
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
        except FlightTimeConflictError as e:
            return ResponseModel.fail(
                msg=FlightConsts.TIME_CONFLICT_ERROR,
                data={"error": str(e)}
            )
        except FlightTimestampOrderError as e:
            return ResponseModel.fail(
                msg=FlightConsts.TIMESTAMP_ORDER_ERROR,
                data={"error": str(e)}
            )
        except FlightActualVsEstimatedError as e:
            return ResponseModel.fail(
                msg=FlightConsts.ACTUAL_VS_ESTIMATED_ERROR,
                data={"error": str(e)}
            )
        except IntegrityError as e:
            return ResponseModel.fail(
                msg=FlightConsts.ADD_FLIGHT_ERROR,
                data={"error": "添加失败，可能是对应航站楼,飞机ID,或者是状态码不正确导致的"}
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
        except FlightTimeConflictError as e:
            return ResponseModel.fail(
                msg=FlightConsts.TIME_CONFLICT_ERROR,
                data={"error": str(e)}
            )
        except FlightTimestampOrderError as e:
            return ResponseModel.fail(
                msg=FlightConsts.TIMESTAMP_ORDER_ERROR,
                data={"error": str(e)}
            )
        except FlightActualVsEstimatedError as e:
            return ResponseModel.fail(
                msg=FlightConsts.ACTUAL_VS_ESTIMATED_ERROR,
                data={"error": str(e)}
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
                data=True
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
            aircraft_name: Optional[str] = None,
            terminal_name: Optional[str] = None,
            estimated_departure_start: Optional[str] = None,
            estimated_departure_end: Optional[str] = None,
            estimated_arrival_start: Optional[str] = None,
            estimated_arrival_end: Optional[str] = None,
            actual_departure_start: Optional[str] = None,
            actual_departure_end: Optional[str] = None,
            actual_arrival_start: Optional[str] = None,
            actual_arrival_end: Optional[str] = None,
            page_num: int = 1,
            page_size: int = 10
    ) -> ResponseModel:
        """分页查询航班记录，包含详细信息，支持按航站楼名称、飞机名称及时间段查询"""
        if page_num < 1 or page_size < 1:
            return ResponseModel.fail(
                msg=FlightConsts.INVALID_FLIGHT_DATA,
                data={"error": "页码和每页大小必须大于0"}
            )

        try:
            result = FlightMapper.search(
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
                pageNum=page_num,
                pageSize=page_size
            )
            return ResponseModel.success(
                msg=FlightConsts.SEARCH_FLIGHT_SUCCESS,
                data=result.model_dump()
            )
        except Exception as e:
            return ResponseModel.fail(
                msg=FlightConsts.SEARCH_FLIGHT_ERROR,
                data={"error": str(e)}
            )

    @staticmethod
    def getFlightAircraftImageId(flightId: str):
        try:
            res = FlightMapper.get_all_related_aircraft_image_by_flight_id(flightId)
            return ResponseModel.success(
                msg=FlightConsts.SEARCH_FLIGHT_SUCCESS,
                data=res
            )
        except Exception as e:
            return ResponseModel.fail(
                msg=FlightConsts.SEARCH_FLIGHT_ERROR,
                data={"error": str(e)}
            )

    @staticmethod
    def AutoCompleteFlightId(payload: str):
        try:
            res = FlightMapper.AutoCompleteFlightId(payload, payload)
            return ResponseModel.success(
                msg=FlightConsts.SEARCH_FLIGHT_SUCCESS,
                data=res
            )
        except Exception as e:
            return ResponseModel.fail(
                msg=FlightConsts.SEARCH_FLIGHT_ERROR,
                data={"error": str(e)}
            )

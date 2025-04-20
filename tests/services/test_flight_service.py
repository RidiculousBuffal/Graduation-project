from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.exc import IntegrityError

from app.DTO.flights import FlightCreateDTO, FlightUpdateDTO
from app.consts.Flight import FlightConsts
from app.exceptions.flights import FlightTimeConflictError, FlightTimestampOrderError, FlightActualVsEstimatedError
from app.models.response import ResponseModel
from app.service.flightService import FlightService


class TestFlightService:
    @pytest.fixture
    def mock_flight_dto(self):
        flight_dto = MagicMock()
        flight_dto.flight_id = "123e4567-e89b-12d3-a456-426614174000"
        flight_dto.aircraft_id = "aircraft_1"
        flight_dto.model_dump.return_value = {
            "flight_id": "123e4567-e89b-12d3-a456-426614174000",
            "aircraft_id": "aircraft_1"
        }
        return flight_dto

    @pytest.fixture
    def mock_flight_detail_dto(self):
        flight_detail_dto = MagicMock()
        flight_detail_dto.flight_id = "123e4567-e89b-12d3-a456-426614174000"
        flight_detail_dto.aircraft_id = "aircraft_1"
        flight_detail_dto.aircraft_name = "TestAircraft"
        flight_detail_dto.model_dump.return_value = {
            "flight_id": "123e4567-e89b-12d3-a456-426614174000",
            "aircraft_id": "aircraft_1",
            "aircraft_name": "TestAircraft"
        }
        return flight_detail_dto

    @pytest.fixture
    def mock_paged_response(self):
        paged_response = MagicMock()
        flight_detail = MagicMock(
            flight_id="123",
            aircraft_id="aircraft_1",
            aircraft_name="TestAircraft"
        )
        paged_response.data = [flight_detail]
        paged_response.pagination = MagicMock(current_page=1, page_size=10, total=1, total_pages=1)
        paged_response.model_dump.return_value = {
            "data": [{"flight_id": "123", "aircraft_id": "aircraft_1", "aircraft_name": "TestAircraft"}],
            "pagination": {"current_page": 1, "page_size": 10, "total": 1, "total_pages": 1}
        }
        return paged_response

    @patch('app.service.flightService.FlightMapper')
    def test_create_flight_success(self, MockFlightMapper, mock_flight_dto, app):
        """测试创建航班成功场景"""
        MockFlightMapper.create.return_value = mock_flight_dto
        create_dto = FlightCreateDTO(aircraft_id="aircraft_1")

        response = FlightService.create_flight(create_dto)

        assert isinstance(response, ResponseModel)
        assert response.code == 0
        assert response.msg == FlightConsts.ADD_FLIGHT_SUCCESS
        assert response.data == mock_flight_dto.model_dump()
        MockFlightMapper.create.assert_called_once()

    @patch('app.service.flightService.FlightMapper')
    def test_create_flight_invalid_data(self, MockFlightMapper, app):
        """测试创建航班失败 - 无效数据场景"""
        create_dto = FlightCreateDTO(aircraft_id="")

        response = FlightService.create_flight(create_dto)

        assert response.code == 1
        assert response.msg == FlightConsts.INVALID_FLIGHT_DATA
        assert "飞机ID不能为空" in str(response.data["error"])
        MockFlightMapper.create.assert_not_called()

    @patch('app.service.flightService.FlightMapper')
    def test_create_flight_time_conflict(self, MockFlightMapper, app):
        """测试创建航班失败 - 时间冲突场景"""
        MockFlightMapper.create.side_effect = FlightTimeConflictError("时间冲突错误")
        create_dto = FlightCreateDTO(aircraft_id="aircraft_1")

        response = FlightService.create_flight(create_dto)

        assert response.code == 1
        assert response.msg == FlightConsts.TIME_CONFLICT_ERROR
        assert "时间冲突错误" in str(response.data["error"])
        MockFlightMapper.create.assert_called_once()

    @patch('app.service.flightService.FlightMapper')
    def test_create_flight_timestamp_order_error(self, MockFlightMapper, app):
        """测试创建航班失败 - 时间顺序错误场景"""
        MockFlightMapper.create.side_effect = FlightTimestampOrderError("到达时间早于起飞时间")
        create_dto = FlightCreateDTO(aircraft_id="aircraft_1")

        response = FlightService.create_flight(create_dto)

        assert response.code == 1
        assert response.msg == FlightConsts.TIMESTAMP_ORDER_ERROR
        assert "到达时间早于起飞时间" in str(response.data["error"])
        MockFlightMapper.create.assert_called_once()

    @patch('app.service.flightService.FlightMapper')
    def test_create_flight_actual_vs_estimated_error(self, MockFlightMapper, app):
        """测试创建航班失败 - 实际时间早于预计时间场景"""
        MockFlightMapper.create.side_effect = FlightActualVsEstimatedError("实际时间早于预计时间")
        create_dto = FlightCreateDTO(aircraft_id="aircraft_1")

        response = FlightService.create_flight(create_dto)

        assert response.code == 1
        assert response.msg == FlightConsts.ACTUAL_VS_ESTIMATED_ERROR
        assert "实际时间早于预计时间" in str(response.data["error"])
        MockFlightMapper.create.assert_called_once()

    @patch('app.service.flightService.FlightMapper')
    def test_create_flight_integrity_error(self, MockFlightMapper, app):
        """测试创建航班失败 - 数据库完整性错误场景"""
        MockFlightMapper.create.side_effect = IntegrityError("Integrity error", None, None)
        create_dto = FlightCreateDTO(aircraft_id="aircraft_1")

        response = FlightService.create_flight(create_dto)

        assert response.code == 1
        assert response.msg == FlightConsts.ADD_FLIGHT_ERROR
        assert "添加失败，可能是对应航站楼,飞机ID,或者是状态码不正确导致的" in str(response.data["error"])
        MockFlightMapper.create.assert_called_once()

    @patch('app.service.flightService.FlightMapper')
    def test_get_flight_by_id_success(self, MockFlightMapper, mock_flight_detail_dto, app):
        """测试获取航班成功场景"""
        MockFlightMapper.get_by_id.return_value = mock_flight_detail_dto
        flight_id = "123e4567-e89b-12d3-a456-426614174000"

        response = FlightService.get_flight_by_id(flight_id)

        assert response.code == 0
        assert response.msg == FlightConsts.GET_FLIGHT_SUCCESS
        assert response.data == mock_flight_detail_dto.model_dump()
        MockFlightMapper.get_by_id.assert_called_once_with(flight_id)

    @patch('app.service.flightService.FlightMapper')
    def test_get_flight_by_id_not_found(self, MockFlightMapper, app):
        """测试获取航班失败 - 未找到场景"""
        MockFlightMapper.get_by_id.return_value = None
        flight_id = "nonexistent_id"

        response = FlightService.get_flight_by_id(flight_id)

        assert response.code == 1
        assert response.msg == FlightConsts.GET_FLIGHT_NOT_FOUND
        assert f"未找到ID为{flight_id}的航班" in str(response.data["error"])
        MockFlightMapper.get_by_id.assert_called_once_with(flight_id)

    @patch('app.service.flightService.FlightMapper')
    def test_update_flight_success(self, MockFlightMapper, mock_flight_dto, app):
        """测试更新航班成功场景"""
        MockFlightMapper.update.return_value = mock_flight_dto
        flight_id = "123e4567-e89b-12d3-a456-426614174000"
        update_dto = FlightUpdateDTO(flight_status="delayed")

        response = FlightService.update_flight(flight_id, update_dto)

        assert response.code == 0
        assert response.msg == FlightConsts.UPDATE_FLIGHT_SUCCESS
        assert response.data == mock_flight_dto.model_dump()
        MockFlightMapper.update.assert_called_once_with(flight_id, update_dto)

    @patch('app.service.flightService.FlightMapper')
    def test_update_flight_time_conflict(self, MockFlightMapper, app):
        """测试更新航班失败 - 时间冲突场景"""
        MockFlightMapper.update.side_effect = FlightTimeConflictError("时间冲突错误")
        flight_id = "123e4567-e89b-12d3-a456-426614174000"
        update_dto = FlightUpdateDTO(flight_status="delayed")

        response = FlightService.update_flight(flight_id, update_dto)

        assert response.code == 1
        assert response.msg == FlightConsts.TIME_CONFLICT_ERROR
        assert "时间冲突错误" in str(response.data["error"])
        MockFlightMapper.update.assert_called_once_with(flight_id, update_dto)

    @patch('app.service.flightService.FlightMapper')
    def test_update_flight_timestamp_order_error(self, MockFlightMapper, app):
        """测试更新航班失败 - 时间顺序错误场景"""
        MockFlightMapper.update.side_effect = FlightTimestampOrderError("到达时间早于起飞时间")
        flight_id = "123e4567-e89b-12d3-a456-426614174000"
        update_dto = FlightUpdateDTO(flight_status="delayed")

        response = FlightService.update_flight(flight_id, update_dto)

        assert response.code == 1
        assert response.msg == FlightConsts.TIMESTAMP_ORDER_ERROR
        assert "到达时间早于起飞时间" in str(response.data["error"])
        MockFlightMapper.update.assert_called_once_with(flight_id, update_dto)

    @patch('app.service.flightService.FlightMapper')
    def test_update_flight_actual_vs_estimated_error(self, MockFlightMapper, app):
        """测试更新航班失败 - 实际时间早于预计时间场景"""
        MockFlightMapper.update.side_effect = FlightActualVsEstimatedError("实际时间早于预计时间")
        flight_id = "123e4567-e89b-12d3-a456-426614174000"
        update_dto = FlightUpdateDTO(flight_status="delayed")

        response = FlightService.update_flight(flight_id, update_dto)

        assert response.code == 1
        assert response.msg == FlightConsts.ACTUAL_VS_ESTIMATED_ERROR
        assert "实际时间早于预计时间" in str(response.data["error"])
        MockFlightMapper.update.assert_called_once_with(flight_id, update_dto)

    @patch('app.service.flightService.FlightMapper')
    def test_delete_flight_success(self, MockFlightMapper, app):
        """测试删除航班成功场景"""
        MockFlightMapper.delete.return_value = True
        flight_id = "123e4567-e89b-12d3-a456-426614174000"

        response = FlightService.delete_flight(flight_id)

        assert response.code == 0
        assert response.msg == FlightConsts.DELETE_FLIGHT_SUCCESS
        assert response.data is None
        MockFlightMapper.delete.assert_called_once_with(flight_id)

    @patch('app.service.flightService.FlightMapper')
    def test_delete_flight_not_found(self, MockFlightMapper, app):
        """测试删除航班失败 - 未找到场景"""
        MockFlightMapper.delete.return_value = False
        flight_id = "nonexistent_id"

        response = FlightService.delete_flight(flight_id)

        assert response.code == 1
        assert response.msg == FlightConsts.DELETE_FLIGHT_ERROR
        assert f"未找到ID为{flight_id}的航班或删除失败" in str(response.data["error"])
        MockFlightMapper.delete.assert_called_once_with(flight_id)

    @patch('app.service.flightService.FlightMapper')
    def test_search_flight_success(self, MockFlightMapper, mock_paged_response, app):
        """测试查询航班列表成功场景"""
        MockFlightMapper.search.return_value = mock_paged_response
        page_num = 1
        page_size = 10

        response = FlightService.search_flight(page_num=page_num, page_size=page_size)

        assert response.code == 0
        assert response.msg == FlightConsts.SEARCH_FLIGHT_SUCCESS
        assert response.data == mock_paged_response.model_dump()
        MockFlightMapper.search.assert_called_once()

    @patch('app.service.flightService.FlightMapper')
    def test_search_flight_invalid_pagination(self, MockFlightMapper, app):
        """测试查询航班列表失败 - 无效分页参数场景"""
        page_num = 0
        page_size = 10

        response = FlightService.search_flight(page_num=page_num, page_size=page_size)

        assert response.code == 1
        assert response.msg == FlightConsts.INVALID_FLIGHT_DATA
        assert "页码和每页大小必须大于0" in str(response.data["error"])
        MockFlightMapper.search.assert_not_called()

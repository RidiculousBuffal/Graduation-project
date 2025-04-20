from unittest.mock import MagicMock, patch
import pytest
from app.consts.Flight import FlightConsts
from app.models.response import ResponseModel
from app.service.flightService import FlightService
from app.DTO.flights import FlightCreateDTO, FlightUpdateDTO

class TestFlightService:
    @pytest.fixture
    def mock_flight_dto(self):
        flight_dto = MagicMock()
        flight_dto.flight_id = "123e4567-e89b-12d3-a456-426614174000"
        flight_dto.aircraft_id = "aircraft_1"
        flight_dto.terminal_id = "terminal_1"
        flight_dto.flight_status = "scheduled"
        flight_dto.health_status = "healthy"
        flight_dto.approval_status = "pending"
        flight_dto.model_dump.return_value = {
            "flight_id": "123e4567-e89b-12d3-a456-426614174000",
            "aircraft_id": "aircraft_1",
            "terminal_id": "terminal_1",
            "flight_status": "scheduled",
            "health_status": "healthy",
            "approval_status": "pending"
        }
        return flight_dto

    @pytest.fixture
    def mock_flight_detail_dto(self):
        flight_detail_dto = MagicMock()
        flight_detail_dto.flight_id = "123e4567-e89b-12d3-a456-426614174000"
        flight_detail_dto.aircraft_id = "aircraft_1"
        flight_detail_dto.aircraft_name = "TestAircraft"
        flight_detail_dto.terminal_id = "terminal_1"
        flight_detail_dto.terminal_name = "TestTerminal"
        flight_detail_dto.flight_status = "scheduled"
        flight_detail_dto.health_status = "healthy"
        flight_detail_dto.approval_status = "pending"
        flight_detail_dto.model_dump.return_value = {
            "flight_id": "123e4567-e89b-12d3-a456-426614174000",
            "aircraft_id": "aircraft_1",
            "aircraft_name": "TestAircraft",
            "terminal_id": "terminal_1",
            "terminal_name": "TestTerminal",
            "flight_status": "scheduled",
            "health_status": "healthy",
            "approval_status": "pending"
        }
        return flight_detail_dto

    @pytest.fixture
    def mock_paged_response(self):
        paged_response = MagicMock()
        flight_detail = MagicMock(
            flight_id="123",
            aircraft_id="aircraft_1",
            aircraft_name="TestAircraft",
            terminal_id="terminal_1",
            terminal_name="TestTerminal",
            flight_status="scheduled"
        )
        paged_response.data = [flight_detail]
        paged_response.pagination = MagicMock(current_page=1, page_size=10, total=1, total_pages=1)
        paged_response.model_dump.return_value = {
            "data": [{
                "flight_id": "123",
                "aircraft_id": "aircraft_1",
                "aircraft_name": "TestAircraft",
                "terminal_id": "terminal_1",
                "terminal_name": "TestTerminal",
                "flight_status": "scheduled"
            }],
            "pagination": {"current_page": 1, "page_size": 10, "total": 1, "total_pages": 1}
        }
        return paged_response

    @patch('app.service.flightService.FlightMapper')
    def test_create_flight_success(self, MockFlightMapper, mock_flight_dto, app):
        # Setup mocks
        MockFlightMapper.create.return_value = mock_flight_dto
        create_dto = FlightCreateDTO(aircraft_id="aircraft_1", terminal_id="terminal_1")

        # Call the function to test
        response = FlightService.create_flight(create_dto)

        # Assertions
        assert isinstance(response, ResponseModel)
        assert response.code == 0
        assert response.msg == FlightConsts.ADD_FLIGHT_SUCCESS
        assert response.data == mock_flight_dto.model_dump()
        MockFlightMapper.create.assert_called_once()

    @patch('app.service.flightService.FlightMapper')
    def test_create_flight_invalid_data(self, MockFlightMapper, app):
        # Setup mocks
        create_dto = FlightCreateDTO(aircraft_id="")

        # Call the function to test
        response = FlightService.create_flight(create_dto)

        # Assertions
        assert response.code == 1
        assert response.msg == FlightConsts.INVALID_FLIGHT_DATA
        assert "飞机ID不能为空" in str(response.data["error"])
        MockFlightMapper.create.assert_not_called()

    @patch('app.service.flightService.FlightMapper')
    def test_get_flight_by_id_success(self, MockFlightMapper, mock_flight_detail_dto, app):
        # Setup mocks
        MockFlightMapper.get_by_id.return_value = mock_flight_detail_dto
        flight_id = "123e4567-e89b-12d3-a456-426614174000"

        # Call the function to test
        response = FlightService.get_flight_by_id(flight_id)

        # Assertions
        assert response.code == 0
        assert response.msg == FlightConsts.GET_FLIGHT_SUCCESS
        assert response.data == mock_flight_detail_dto.model_dump()
        assert "aircraft_name" in response.data  # 验证包含详细信息
        assert "terminal_name" in response.data  # 验证包含详细信息
        MockFlightMapper.get_by_id.assert_called_once_with(flight_id)

    @patch('app.service.flightService.FlightMapper')
    def test_get_flight_by_id_not_found(self, MockFlightMapper, app):
        # Setup mocks
        MockFlightMapper.get_by_id.return_value = None
        flight_id = "nonexistent_id"

        # Call the function to test
        response = FlightService.get_flight_by_id(flight_id)

        # Assertions
        assert response.code == 1
        assert response.msg == FlightConsts.GET_FLIGHT_NOT_FOUND
        assert f"未找到ID为{flight_id}的航班" in str(response.data["error"])
        MockFlightMapper.get_by_id.assert_called_once_with(flight_id)

    @patch('app.service.flightService.FlightMapper')
    def test_update_flight_success(self, MockFlightMapper, mock_flight_dto, app):
        # Setup mocks
        MockFlightMapper.update.return_value = mock_flight_dto
        flight_id = "123e4567-e89b-12d3-a456-426614174000"
        update_dto = FlightUpdateDTO(flight_status="delayed")

        # Call the function to test
        response = FlightService.update_flight(flight_id, update_dto)

        # Assertions
        assert response.code == 0
        assert response.msg == FlightConsts.UPDATE_FLIGHT_SUCCESS
        assert response.data == mock_flight_dto.model_dump()
        MockFlightMapper.update.assert_called_once_with(flight_id, update_dto)

    @patch('app.service.flightService.FlightMapper')
    def test_update_flight_not_found(self, MockFlightMapper, app):
        # Setup mocks
        MockFlightMapper.update.return_value = None
        flight_id = "nonexistent_id"
        update_dto = FlightUpdateDTO(flight_status="delayed")

        # Call the function to test
        response = FlightService.update_flight(flight_id, update_dto)

        # Assertions
        assert response.code == 1
        assert response.msg == FlightConsts.UPDATE_FLIGHT_ERROR
        assert f"未找到ID为{flight_id}的航班或更新失败" in str(response.data["error"])
        MockFlightMapper.update.assert_called_once_with(flight_id, update_dto)

    @patch('app.service.flightService.FlightMapper')
    def test_delete_flight_success(self, MockFlightMapper, app):
        # Setup mocks
        MockFlightMapper.delete.return_value = True
        flight_id = "123e4567-e89b-12d3-a456-426614174000"

        # Call the function to test
        response = FlightService.delete_flight(flight_id)

        # Assertions
        assert response.code == 0
        assert response.msg == FlightConsts.DELETE_FLIGHT_SUCCESS
        assert response.data is None
        MockFlightMapper.delete.assert_called_once_with(flight_id)

    @patch('app.service.flightService.FlightMapper')
    def test_delete_flight_not_found(self, MockFlightMapper, app):
        # Setup mocks
        MockFlightMapper.delete.return_value = False
        flight_id = "nonexistent_id"

        # Call the function to test
        response = FlightService.delete_flight(flight_id)

        # Assertions
        assert response.code == 1
        assert response.msg == FlightConsts.DELETE_FLIGHT_ERROR
        assert f"未找到ID为{flight_id}的航班或删除失败" in str(response.data["error"])
        MockFlightMapper.delete.assert_called_once_with(flight_id)

    @patch('app.service.flightService.FlightMapper')
    def test_search_flight_success(self, MockFlightMapper, mock_paged_response, app):
        # Setup mocks
        MockFlightMapper.search.return_value = mock_paged_response
        aircraft_id = "aircraft_1"
        flight_status = "scheduled"
        page_num = 1
        page_size = 10

        # Call the function to test
        response = FlightService.search_flight(
            aircraft_id=aircraft_id,
            flight_status=flight_status,
            page_num=page_num,
            page_size=page_size
        )

        # Assertions
        assert response.code == 0
        assert response.msg == FlightConsts.SEARCH_FLIGHT_SUCCESS
        assert response.data == mock_paged_response.model_dump()
        assert "aircraft_name" in response.data["data"][0]  # 验证包含详细信息
        assert "terminal_name" in response.data["data"][0]  # 验证包含详细信息
        MockFlightMapper.search.assert_called_once_with(
            aircraft_id=aircraft_id,
            terminal_id=None,
            flight_status=flight_status,
            health_status=None,
            approval_status=None,
            pageNum=page_num,
            pageSize=page_size
        )

    @patch('app.service.flightService.FlightMapper')
    def test_search_flight_invalid_pagination(self, MockFlightMapper, app):
        # Setup mocks
        page_num = 0
        page_size = 10

        # Call the function to test
        response = FlightService.search_flight(page_num=page_num, page_size=page_size)

        # Assertions
        assert response.code == 1
        assert response.msg == FlightConsts.INVALID_FLIGHT_DATA
        assert "页码和每页大小必须大于0" in str(response.data["error"])
        MockFlightMapper.search.assert_not_called()
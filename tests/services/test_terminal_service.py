from unittest.mock import MagicMock, patch
import pytest
from app.consts.Terminals import TerminalConsts
from app.models.response import ResponseModel
from app.service.terminalService import TerminalService
from app.DTO.terminals import TerminalCreateDTO, TerminalUpdateDTO

class TestTerminalService:
    @pytest.fixture
    def mock_terminal_dto(self):
        terminal_dto = MagicMock()
        terminal_dto.terminal_id = "123e4567-e89b-12d3-a456-426614174000"
        terminal_dto.terminal_name = "TestTerminal"
        terminal_dto.description = "Test Description"
        terminal_dto.model_dump.return_value = {
            "terminal_id": "123e4567-e89b-12d3-a456-426614174000",
            "terminal_name": "TestTerminal",
            "description": "Test Description"
        }
        return terminal_dto

    @pytest.fixture
    def mock_paged_response(self):
        paged_response = MagicMock()
        paged_response.data = [MagicMock(terminal_id="123", terminal_name="TestTerminal", description="Test Description")]
        paged_response.pagination = MagicMock(current_page=1, page_size=10, total=1, total_pages=1)
        paged_response.model_dump.return_value = {
            "data": [{"terminal_id": "123", "terminal_name": "TestTerminal", "description": "Test Description"}],
            "pagination": {"current_page": 1, "page_size": 10, "total": 1, "total_pages": 1}
        }
        return paged_response

    @patch('app.service.terminalService.TerminalMapper')
    def test_create_terminal_success(self, MockTerminalMapper, mock_terminal_dto, app):
        # Setup mocks
        MockTerminalMapper.search.return_value = MagicMock(data=[])
        MockTerminalMapper.create.return_value = mock_terminal_dto
        create_dto = TerminalCreateDTO(terminal_name="TestTerminal", description="Test Description")

        # Call the function to test
        response = TerminalService.create_terminal(create_dto)

        # Assertions
        assert isinstance(response, ResponseModel)
        assert response.code == 0
        assert response.msg == TerminalConsts.ADD_TERMINAL_SUCCESS
        assert response.data == mock_terminal_dto.model_dump()
        MockTerminalMapper.search.assert_called_once_with(terminal_name="TestTerminal")
        MockTerminalMapper.create.assert_called_once()

    @patch('app.service.terminalService.TerminalMapper')
    def test_create_terminal_existing_name(self, MockTerminalMapper, mock_terminal_dto, app):
        # Setup mocks
        MockTerminalMapper.search.return_value = MagicMock(data=[mock_terminal_dto])
        create_dto = TerminalCreateDTO(terminal_name="TestTerminal", description="Test Description")

        # Call the function to test
        response = TerminalService.create_terminal(create_dto)

        # Assertions
        assert response.code == 1
        assert response.msg == TerminalConsts.TERMINAL_ALREADY_EXISTS
        MockTerminalMapper.search.assert_called_once_with(terminal_name="TestTerminal")

    @patch('app.service.terminalService.TerminalMapper')
    def test_create_terminal_invalid_data(self, MockTerminalMapper, app):
        # Setup mocks
        create_dto = TerminalCreateDTO(terminal_name="", description="Test Description")

        # Call the function to test
        response = TerminalService.create_terminal(create_dto)

        # Assertions
        assert response.code == 1
        assert response.msg == TerminalConsts.INVALID_TERMINAL_DATA
        assert "航站楼名称不能为空" in str(response.data["error"])
        MockTerminalMapper.search.assert_not_called()

    @patch('app.service.terminalService.TerminalMapper')
    def test_get_terminal_by_id_success(self, MockTerminalMapper, mock_terminal_dto, app):
        # Setup mocks
        MockTerminalMapper.get_by_id.return_value = mock_terminal_dto
        terminal_id = "123e4567-e89b-12d3-a456-426614174000"

        # Call the function to test
        response = TerminalService.get_terminal_by_id(terminal_id)

        # Assertions
        assert response.code == 0
        assert response.msg == TerminalConsts.GET_TERMINAL_SUCCESS
        assert response.data == mock_terminal_dto.model_dump()
        MockTerminalMapper.get_by_id.assert_called_once_with(terminal_id)

    @patch('app.service.terminalService.TerminalMapper')
    def test_get_terminal_by_id_not_found(self, MockTerminalMapper, app):
        # Setup mocks
        MockTerminalMapper.get_by_id.return_value = None
        terminal_id = "nonexistent_id"

        # Call the function to test
        response = TerminalService.get_terminal_by_id(terminal_id)

        # Assertions
        assert response.code == 1
        assert response.msg == TerminalConsts.GET_TERMINAL_NOT_FOUND
        assert f"未找到ID为{terminal_id}的航站楼" in str(response.data["error"])
        MockTerminalMapper.get_by_id.assert_called_once_with(terminal_id)

    @patch('app.service.terminalService.TerminalMapper')
    def test_update_terminal_success(self, MockTerminalMapper, mock_terminal_dto, app):
        # Setup mocks
        MockTerminalMapper.search.return_value = MagicMock(data=[])
        MockTerminalMapper.update.return_value = mock_terminal_dto
        terminal_id = "123e4567-e89b-12d3-a456-426614174000"
        update_dto = TerminalUpdateDTO(terminal_name="UpdatedTerminal", description="Updated Description")

        # Call the function to test
        response = TerminalService.update_terminal(terminal_id, update_dto)

        # Assertions
        assert response.code == 0
        assert response.msg == TerminalConsts.UPDATE_TERMINAL_SUCCESS
        assert response.data == mock_terminal_dto.model_dump()
        MockTerminalMapper.search.assert_called_once_with(terminal_name="UpdatedTerminal")
        MockTerminalMapper.update.assert_called_once_with(terminal_id, update_dto)

    @patch('app.service.terminalService.TerminalMapper')
    def test_update_terminal_existing_name(self, MockTerminalMapper, mock_terminal_dto, app):
        # Setup mocks
        MockTerminalMapper.search.return_value = MagicMock(data=[MagicMock(terminal_id="different_id")])
        terminal_id = "123e4567-e89b-12d3-a456-426614174000"
        update_dto = TerminalUpdateDTO(terminal_name="UpdatedTerminal", description="Updated Description")

        # Call the function to test
        response = TerminalService.update_terminal(terminal_id, update_dto)

        # Assertions
        assert response.code == 1
        assert response.msg == TerminalConsts.TERMINAL_ALREADY_EXISTS
        MockTerminalMapper.search.assert_called_once_with(terminal_name="UpdatedTerminal")
        MockTerminalMapper.update.assert_not_called()

    @patch('app.service.terminalService.TerminalMapper')
    def test_delete_terminal_success(self, MockTerminalMapper, app):
        # Setup mocks
        MockTerminalMapper.delete.return_value = True
        terminal_id = "123e4567-e89b-12d3-a456-426614174000"

        # Call the function to test
        response = TerminalService.delete_terminal(terminal_id)

        # Assertions
        assert response.code == 0
        assert response.msg == TerminalConsts.DELETE_TERMINAL_SUCCESS
        assert response.data is None
        MockTerminalMapper.delete.assert_called_once_with(terminal_id)

    @patch('app.service.terminalService.TerminalMapper')
    def test_delete_terminal_not_found(self, MockTerminalMapper, app):
        # Setup mocks
        MockTerminalMapper.delete.return_value = False
        terminal_id = "nonexistent_id"

        # Call the function to test
        response = TerminalService.delete_terminal(terminal_id)

        # Assertions
        assert response.code == 1
        assert response.msg == TerminalConsts.DELETE_TERMINAL_ERROR
        assert f"未找到ID为{terminal_id}的航站楼或删除失败" in str(response.data["error"])
        MockTerminalMapper.delete.assert_called_once_with(terminal_id)

    @patch('app.service.terminalService.TerminalMapper')
    def test_search_terminal_success(self, MockTerminalMapper, mock_paged_response, app):
        # Setup mocks
        MockTerminalMapper.search.return_value = mock_paged_response
        terminal_name = "TestTerminal"
        page_num = 1
        page_size = 10

        # Call the function to test
        response = TerminalService.search_terminal(terminal_name=terminal_name, page_num=page_num, page_size=page_size)

        # Assertions
        assert response.code == 0
        assert response.msg == TerminalConsts.SEARCH_TERMINAL_SUCCESS
        assert response.data == mock_paged_response.model_dump()
        MockTerminalMapper.search.assert_called_once_with(terminal_name=terminal_name, pageNum=page_num, pageSize=page_size)

    @patch('app.service.terminalService.TerminalMapper')
    def test_search_terminal_invalid_pagination(self, MockTerminalMapper, app):
        # Setup mocks
        page_num = 0
        page_size = 10

        # Call the function to test
        response = TerminalService.search_terminal(page_num=page_num, page_size=page_size)

        # Assertions
        assert response.code == 1
        assert response.msg == TerminalConsts.INVALID_TERMINAL_DATA
        assert "页码和每页大小必须大于0" in str(response.data["error"])
        MockTerminalMapper.search.assert_not_called()
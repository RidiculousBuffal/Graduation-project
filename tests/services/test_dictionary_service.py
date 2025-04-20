from unittest.mock import MagicMock, patch

import pytest

from app.consts.Dictionary import DictionaryConsts
from app.service.dictionaryService import DictionaryService


class TestDictionaryService:
    @pytest.fixture
    def mock_dictionary_detail_dto(self):
        dto = MagicMock()
        dto.dict_key = "status"
        dto.dict_name = "状态类"
        dto.parent_key = None
        dto.description = "所有状态类字典的总分类"
        dto.children = []
        dto.model_dump.return_value = {
            "dict_key": "status",
            "dict_name": "状态类",
            "parent_key": None,
            "description": "所有状态类字典的总分类",
            "children": []
        }
        return dto

    @pytest.fixture
    def mock_flight_status_detail_dto(self):
        dto = MagicMock()
        dto.dict_key = "flight_status"
        dto.dict_name = "飞行状态"
        dto.parent_key = "status"
        dto.description = "飞机飞行流程状态"
        # 修正 children 列表，每个 child 都设置 model_dump.return_value
        children = [
            MagicMock(dict_key="scheduled", dict_name="已排班", parent_key="flight_status"),
            MagicMock(dict_key="boarding", dict_name="登机中", parent_key="flight_status"),
            MagicMock(dict_key="departed", dict_name="已起飞", parent_key="flight_status"),
            MagicMock(dict_key="arrived", dict_name="已到达", parent_key="flight_status"),
            MagicMock(dict_key="delayed", dict_name="延误", parent_key="flight_status"),
            MagicMock(dict_key="cancelled", dict_name="已取消", parent_key="flight_status"),
        ]
        for child in children:
            child.model_dump.return_value = {
                "dict_key": child.dict_key,
                "dict_name": child.dict_name,
                "parent_key": child.parent_key,
                "description": "",
                "children": []
            }
        dto.children = children
        dto.model_dump.return_value = {
            "dict_key": "flight_status",
            "dict_name": "飞行状态",
            "parent_key": "status",
            "description": "飞机飞行流程状态",
            "children": [child.model_dump.return_value for child in children]
        }
        return dto

    @pytest.fixture
    def mock_dictionary_paged_response(self):
        response = MagicMock()
        dictionary_detail = MagicMock(dict_key="status", dict_name="状态类")
        dictionary_detail.model_dump.return_value = {
            "dict_key": "status",
            "dict_name": "状态类",
            "parent_key": None,
            "description": ""
        }
        response.data = [dictionary_detail]
        response.pagination = MagicMock(current_page=1, page_size=10, total=1, total_pages=1)
        response.model_dump.return_value = {
            "data": [dictionary_detail.model_dump.return_value],
            "pagination": {"current_page": 1, "page_size": 10, "total": 1, "total_pages": 1}
        }
        return response

    @patch('app.service.dictionaryService.DictionaryMapper')
    def test_get_dictionary_by_key_success(self, MockDictionaryMapper, mock_dictionary_detail_dto, app):
        """测试按键获取字典成功场景 - 查询 'status'"""
        MockDictionaryMapper.get_by_key.return_value = mock_dictionary_detail_dto
        dict_key = "status"

        response = DictionaryService.get_dictionary_by_key(dict_key)

        assert response.code == 0
        assert response.msg == DictionaryConsts.GET_DICTIONARY_SUCCESS
        assert response.data == mock_dictionary_detail_dto.model_dump()
        assert response.data["dict_key"] == "status"
        assert response.data["dict_name"] == "状态类"
        MockDictionaryMapper.get_by_key.assert_called_once_with(dict_key)

    @patch('app.service.dictionaryService.DictionaryMapper')
    def test_get_dictionary_by_key_not_found(self, MockDictionaryMapper, app):
        """测试按键获取字典失败 - 未找到场景"""
        MockDictionaryMapper.get_by_key.return_value = None
        dict_key = "nonexistent_key"

        response = DictionaryService.get_dictionary_by_key(dict_key)

        assert response.code == 1
        assert response.msg == DictionaryConsts.GET_DICTIONARY_NOT_FOUND
        assert f"未找到键为{dict_key}的字典" in str(response.data["error"])
        MockDictionaryMapper.get_by_key.assert_called_once_with(dict_key)

    @patch('app.service.dictionaryService.DictionaryMapper')
    def test_get_dictionary_by_key_invalid_input(self, MockDictionaryMapper, app):
        """测试按键获取字典失败 - 无效输入场景"""
        dict_key = ""

        response = DictionaryService.get_dictionary_by_key(dict_key)

        assert response.code == 1
        assert response.msg == DictionaryConsts.INVALID_DICTIONARY_DATA
        assert "字典键不能为空" in str(response.data["error"])
        MockDictionaryMapper.get_by_key.assert_not_called()

    @patch('app.service.dictionaryService.DictionaryMapper')
    def test_get_children_by_parent_key_success_flight_status(self, MockDictionaryMapper, mock_flight_status_detail_dto,
                                                              app):
        """测试获取子字典成功场景 - 查询 'flight_status' 的子字典"""
        MockDictionaryMapper.get_children_by_parent_key.return_value = mock_flight_status_detail_dto.children
        parent_key = "flight_status"

        response = DictionaryService.get_children_by_parent_key(parent_key)

        assert response.code == 0
        assert response.msg == DictionaryConsts.GET_CHILDREN_SUCCESS
        assert len(response.data) == 6  # scheduled, boarding, departed, arrived, delayed, cancelled
        assert any(child["dict_key"] == "scheduled" for child in response.data)
        assert any(child["dict_key"] == "cancelled" for child in response.data)
        MockDictionaryMapper.get_children_by_parent_key.assert_called_once_with(parent_key)

    @patch('app.service.dictionaryService.DictionaryMapper')
    def test_get_children_by_parent_key_success_status(self, MockDictionaryMapper, mock_dictionary_detail_dto, app):
        """测试获取子字典成功场景 - 查询 'status' 的子字典"""
        children = [
            MagicMock(dict_key="flight_status", dict_name="飞行状态", parent_key="status"),
            MagicMock(dict_key="health_status", dict_name="健康状态", parent_key="status"),
            MagicMock(dict_key="approval_status", dict_name="审批状态", parent_key="status"),
            MagicMock(dict_key="task_status", dict_name="任务状态", parent_key="status"),
            MagicMock(dict_key="inspection_status", dict_name="检查状态", parent_key="status")
        ]
        for child in children:
            child.model_dump.return_value = {
                "dict_key": child.dict_key,
                "dict_name": child.dict_name,
                "parent_key": child.parent_key,
                "description": "",
                "children": []
            }
        MockDictionaryMapper.get_children_by_parent_key.return_value = children
        parent_key = "status"

        response = DictionaryService.get_children_by_parent_key(parent_key)

        assert response.code == 0
        assert response.msg == DictionaryConsts.GET_CHILDREN_SUCCESS
        assert len(response.data) == 5  # flight_status, health_status, approval_status, task_status, inspection_status
        assert any(child["dict_key"] == "flight_status" for child in response.data)
        assert any(child["dict_key"] == "inspection_status" for child in response.data)
        MockDictionaryMapper.get_children_by_parent_key.assert_called_once_with(parent_key)

    @patch('app.service.dictionaryService.DictionaryMapper')
    def test_get_children_by_parent_key_invalid_input(self, MockDictionaryMapper, app):
        """测试获取子字典失败 - 无效输入场景"""
        parent_key = ""

        response = DictionaryService.get_children_by_parent_key(parent_key)

        assert response.code == 1
        assert response.msg == DictionaryConsts.INVALID_DICTIONARY_DATA
        assert "父字典键不能为空" in str(response.data["error"])
        MockDictionaryMapper.get_children_by_parent_key.assert_not_called()

    @patch('app.service.dictionaryService.DictionaryMapper')
    def test_search_dictionary_success(self, MockDictionaryMapper, mock_dictionary_paged_response, app):
        """测试分页查询字典成功场景"""
        MockDictionaryMapper.search.return_value = mock_dictionary_paged_response
        page_num = 1
        page_size = 10

        response = DictionaryService.search_dictionary(page_num=page_num, page_size=page_size)

        assert response.code == 0
        assert response.msg == DictionaryConsts.SEARCH_DICTIONARY_SUCCESS
        assert response.data == mock_dictionary_paged_response.model_dump()
        MockDictionaryMapper.search.assert_called_once()

    @patch('app.service.dictionaryService.DictionaryMapper')
    def test_search_dictionary_with_filters(self, MockDictionaryMapper, mock_dictionary_paged_response, app):
        """测试分页查询字典成功场景 - 带过滤条件"""
        MockDictionaryMapper.search.return_value = mock_dictionary_paged_response
        page_num = 1
        page_size = 10
        dict_name = "状态"
        parent_key = "status"

        response = DictionaryService.search_dictionary(
            dict_name=dict_name,
            parent_key=parent_key,
            page_num=page_num,
            page_size=page_size
        )

        assert response.code == 0
        assert response.msg == DictionaryConsts.SEARCH_DICTIONARY_SUCCESS
        assert response.data == mock_dictionary_paged_response.model_dump()
        MockDictionaryMapper.search.assert_called_once_with(
            dict_name=dict_name,
            parent_key=parent_key,
            pageNum=page_num,
            pageSize=page_size
        )

    @patch('app.service.dictionaryService.DictionaryMapper')
    def test_search_dictionary_invalid_pagination(self, MockDictionaryMapper, app):
        """测试分页查询字典失败 - 无效分页参数场景"""
        page_num = 0
        page_size = 10

        response = DictionaryService.search_dictionary(page_num=page_num, page_size=page_size)

        assert response.code == 1
        assert response.msg == DictionaryConsts.INVALID_DICTIONARY_DATA
        assert "页码和每页大小必须大于0" in str(response.data["error"])
        MockDictionaryMapper.search.assert_not_called()

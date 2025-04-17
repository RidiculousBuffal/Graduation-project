from unittest.mock import patch

import pytest
from sqlalchemy.exc import IntegrityError

from app.DTO.aircrafts import (
    AircraftReferenceImageCreateDTO,
    AircraftReferenceImageUpdateDTO,
    AircraftReferenceImageDTO,
    AircraftReferenceImagePagedResponseDTO,
    AircraftReferenceImageJson,
    FileDTO,
    AircraftReferenceImagePoint
)
from app.DTO.pagination import PaginationDTO
from app.consts.Aircrafts import AircraftConsts
from app.service.aircraftReferenceImageService import AircraftReferenceImageService


@pytest.fixture
def mock_mapper():
    """为 AircraftReferenceImageMapper 创建模拟对象"""
    with patch('app.service.aircraftReferenceImageService.AircraftReferenceImageMapper') as mock:
        yield mock


@pytest.fixture
def sample_image_dto():
    """创建示例 AircraftReferenceImageDTO 对象"""
    file_dto = FileDTO(
        download_url="http://example.com/file",
        filename="test_image.jpg",
        ipfs_cid="QmTestCid",
        ipfs_path="/ipfs/test",
        mfs_path="/mfs/test",
        mime_type="image/jpeg",
        size=1024,
        stored_filename="test_stored.jpg",
        success=True,
        uploaded_at="2023-10-01T12:00:00"
    )
    point_data = [
        AircraftReferenceImagePoint(id=1, x=10.5, y=20.5),
        AircraftReferenceImagePoint(id=2, x=30.5, y=40.5)
    ]
    image_json = AircraftReferenceImageJson(
        fileInfo=file_dto,
        pointInfo=point_data
    )
    return AircraftReferenceImageDTO(
        image_id="123e4567-e89b-12d3-a456-426614174000",
        image_name="TestImage",
        image_description="Test Image Description",
        image_json=image_json,
        aircraft_id="10b97346-b40b-48ce-af8c-eb6448a8e82a"
    )


@pytest.fixture
def sample_paged_response(sample_image_dto):
    """创建示例 AircraftReferenceImagePagedResponseDTO 对象"""
    return AircraftReferenceImagePagedResponseDTO(
        pagination=PaginationDTO(total=2,
                                 current_page=1,
                                 page_size=10, total_pages=1),
        data=[sample_image_dto for _ in range(2)]
    )


def test_create_image_success(mock_mapper, sample_image_dto):
    """测试创建图片记录 - 成功场景"""
    create_dto = AircraftReferenceImageCreateDTO(
        image_name="TestImage",
        image_description="Test Image Description",
        image_json=sample_image_dto.image_json,
        aircraft_id="10b97346-b40b-48ce-af8c-eb6448a8e82a"
    )
    mock_mapper.create.return_value = sample_image_dto

    response = AircraftReferenceImageService.create_image(create_dto)

    assert response.code == 0
    assert response.msg == AircraftConsts.ADD_IMAGE_SUCCESS
    assert response.data == sample_image_dto.model_dump()
    mock_mapper.create.assert_called_once_with(create_dto)


def test_create_image_invalid_data(mock_mapper):
    """测试创建图片记录 - 无效数据场景"""
    create_dto = AircraftReferenceImageCreateDTO(
        image_name="",
        image_description="Test Image Description",
        image_json=AircraftReferenceImageJson(fileInfo=FileDTO(
            download_url="http://example.com/file", filename="test.jpg", ipfs_cid="QmTestCid",
            ipfs_path="/ipfs/test", mfs_path="/mfs/test", mime_type="image/jpeg", size=1024,
            stored_filename="test_stored.jpg", success=True, uploaded_at="2023-10-01T12:00:00"
        ), pointInfo=[]),
        aircraft_id=""
    )

    response = AircraftReferenceImageService.create_image(create_dto)

    assert response.code == 1
    assert response.msg == AircraftConsts.INVALID_IMAGE_DATA
    assert "图片名称和飞机ID不能为空" in str(response.data["error"])
    mock_mapper.create.assert_not_called()


def test_create_image_integrity_error(mock_mapper):
    """测试创建图片记录 - 数据库完整性错误场景"""
    create_dto = AircraftReferenceImageCreateDTO(
        image_name="TestImage",
        image_description="Test Image Description",
        image_json=AircraftReferenceImageJson(fileInfo=FileDTO(
            download_url="http://example.com/file", filename="test.jpg", ipfs_cid="QmTestCid",
            ipfs_path="/ipfs/test", mfs_path="/mfs/test", mime_type="image/jpeg", size=1024,
            stored_filename="test_stored.jpg", success=True, uploaded_at="2023-10-01T12:00:00"
        ), pointInfo=[]),
        aircraft_id="10b97346-b40b-48ce-af8c-eb6448a8e82a"
    )
    mock_mapper.create.side_effect = IntegrityError("mock error", None, None)

    response = AircraftReferenceImageService.create_image(create_dto)

    assert response.code == 1
    assert response.msg == AircraftConsts.ADD_IMAGE_ERROR
    assert "mock error" in str(response.data["error"])
    mock_mapper.create.assert_called_once_with(create_dto)


def test_get_image_by_id_success(mock_mapper, sample_image_dto):
    """测试按ID获取图片记录 - 成功场景"""
    image_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_mapper.get_by_id.return_value = sample_image_dto

    response = AircraftReferenceImageService.get_image_by_id(image_id)

    assert response.code == 0
    assert response.msg == AircraftConsts.GET_IMAGE_SUCCESS
    assert response.data == sample_image_dto.model_dump()
    mock_mapper.get_by_id.assert_called_once_with(image_id)


def test_get_image_by_id_not_found(mock_mapper):
    """测试按ID获取图片记录 - 未找到场景"""
    image_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_mapper.get_by_id.return_value = None

    response = AircraftReferenceImageService.get_image_by_id(image_id)

    assert response.code == 1
    assert response.msg == AircraftConsts.GET_IMAGE_NOT_FOUND
    assert f"未找到ID为{image_id}的飞机参考图片" in str(response.data["error"])
    mock_mapper.get_by_id.assert_called_once_with(image_id)


def test_get_image_by_id_invalid_id(mock_mapper):
    """测试按ID获取图片记录 - 无效ID场景"""
    image_id = ""

    response = AircraftReferenceImageService.get_image_by_id(image_id)

    assert response.code == 1
    assert response.msg == AircraftConsts.INVALID_IMAGE_DATA
    assert "图片ID不能为空" in str(response.data["error"])
    mock_mapper.get_by_id.assert_not_called()


def test_update_image_success(mock_mapper, sample_image_dto):
    """测试更新图片记录 - 成功场景"""
    image_id = "123e4567-e89b-12d3-a456-426614174000"
    update_dto = AircraftReferenceImageUpdateDTO(
        image_name="UpdatedImage",
        image_description="Updated Description"
    )
    mock_mapper.update.return_value = sample_image_dto

    response = AircraftReferenceImageService.update_image(image_id, update_dto)

    assert response.code == 0
    assert response.msg == AircraftConsts.UPDATE_IMAGE_SUCCESS
    assert response.data == sample_image_dto.model_dump()
    mock_mapper.update.assert_called_once_with(image_id, update_dto)


def test_update_image_not_found(mock_mapper):
    """测试更新图片记录 - 未找到场景"""
    image_id = "123e4567-e89b-12d3-a456-426614174000"
    update_dto = AircraftReferenceImageUpdateDTO(
        image_name="UpdatedImage",
        image_description="Updated Description"
    )
    mock_mapper.update.return_value = None

    response = AircraftReferenceImageService.update_image(image_id, update_dto)

    assert response.code == 1
    assert response.msg == AircraftConsts.UPDATE_IMAGE_ERROR
    assert f"未找到ID为{image_id}的飞机参考图片或更新失败" in str(response.data["error"])
    mock_mapper.update.assert_called_once_with(image_id, update_dto)


def test_update_image_invalid_id(mock_mapper):
    """测试更新图片记录 - 无效ID场景"""
    image_id = ""
    update_dto = AircraftReferenceImageUpdateDTO(
        image_name="UpdatedImage",
        image_description="Updated Description"
    )

    response = AircraftReferenceImageService.update_image(image_id, update_dto)

    assert response.code == 1
    assert response.msg == AircraftConsts.INVALID_IMAGE_DATA
    assert "图片ID不能为空" in str(response.data["error"])
    mock_mapper.update.assert_not_called()


def test_delete_image_success(mock_mapper):
    """测试删除图片记录 - 成功场景"""
    image_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_mapper.delete.return_value = True

    response = AircraftReferenceImageService.delete_image(image_id)

    assert response.code == 0
    assert response.msg == AircraftConsts.DELETE_IMAGE_SUCCESS
    assert response.data is None
    mock_mapper.delete.assert_called_once_with(image_id)


def test_delete_image_not_found(mock_mapper):
    """测试删除图片记录 - 未找到场景"""
    image_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_mapper.delete.return_value = False

    response = AircraftReferenceImageService.delete_image(image_id)

    assert response.code == 1
    assert response.msg == AircraftConsts.DELETE_IMAGE_ERROR
    assert f"未找到ID为{image_id}的飞机参考图片或删除失败" in str(response.data["error"])
    mock_mapper.delete.assert_called_once_with(image_id)


def test_delete_image_invalid_id(mock_mapper):
    """测试删除图片记录 - 无效ID场景"""
    image_id = ""

    response = AircraftReferenceImageService.delete_image(image_id)

    assert response.code == 1
    assert response.msg == AircraftConsts.INVALID_IMAGE_DATA
    assert "图片ID不能为空" in str(response.data["error"])
    mock_mapper.delete.assert_not_called()


def test_search_image_success(mock_mapper, sample_paged_response):
    """测试分页查询图片记录 - 成功场景"""
    image_name = "TestImage"
    aircraft_id = "10b97346-b40b-48ce-af8c-eb6448a8e82a"
    aircraft_name = "TestAircraft"
    page_num = 1
    page_size = 10
    mock_mapper.search.return_value = sample_paged_response

    response = AircraftReferenceImageService.search_image(
        image_name=image_name,
        aircraft_id=aircraft_id,
        aircraft_name=aircraft_name,
        page_num=page_num,
        page_size=page_size
    )

    assert response.code == 0
    assert response.msg == AircraftConsts.SEARCH_IMAGE_SUCCESS
    assert response.data == sample_paged_response.model_dump()
    mock_mapper.search.assert_called_once_with(
        image_name=image_name,
        aircraft_id=aircraft_id,
        aircraft_name=aircraft_name,
        page_num=page_num,
        page_size=page_size
    )


def test_search_image_invalid_pagination(mock_mapper):
    """测试分页查询图片记录 - 无效分页参数场景"""
    page_num = 0
    page_size = 10

    response = AircraftReferenceImageService.search_image(
        page_num=page_num,
        page_size=page_size
    )

    assert response.code == 1
    assert response.msg == AircraftConsts.INVALID_IMAGE_DATA
    assert "页码和每页大小必须大于0" in str(response.data["error"])
    mock_mapper.search.assert_not_called()

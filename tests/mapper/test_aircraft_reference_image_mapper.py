from app.DTO.aircrafts import (
    AircraftReferenceImageCreateDTO,
    AircraftReferenceImageUpdateDTO,
    AircraftReferenceImageJson,
    AircraftReferenceImagePoint
)
from app.DTO.file import FileDTO
from app.mapper.aircraft.aircraftMapper import AircraftMapper
from app.mapper.aircraft.aircraftReferenceImageMapper import AircraftReferenceImageMapper
from app.mapper.aircraft.aircraftTypeMapper import AircraftTypeMapper
from app.DTO.aircrafts import AircraftTypeCreateDTO, AircraftCreateDTO

def test_aircraft_reference_image_mapper_crud(app):
    with app.app_context():
        # 先创建关联的 AircraftType 和 Aircraft
        type_create_dto = AircraftTypeCreateDTO(
            type_name="TestAircraftType",
            description="Test Aircraft Type Description"
        )
        created_type = AircraftTypeMapper.create(type_create_dto)

        aircraft_create_dto = AircraftCreateDTO(
            aircraft_name="TestAircraft",
            age=5,
            typeid=created_type.typeid
        )
        created_aircraft = AircraftMapper.create(aircraft_create_dto)

        # 测试创建 AircraftReferenceImage
        print("\n=== 测试 AircraftReferenceImageMapper 创建功能 ===")
        file_dto = FileDTO(
            download_url="http://example.com/file",
            filename="test_image.jpg",
            ipfs_cid="QmTestCid",
            ipfs_path="/ipfs/test",
            mfs_path="/mfs/test",
            mime_type="image/jpeg",
            size=1024,
            stored_filename="test Stored.jpg",
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
        image_create_dto = AircraftReferenceImageCreateDTO(
            image_name="TestImage",
            image_description="Test Image Description",
            image_json=image_json,
            aircraft_id=created_aircraft.aircraft_id
        )
        print(f"输入值: Create DTO = {image_create_dto}")
        created_image = AircraftReferenceImageMapper.create(image_create_dto)
        print(f"返回值: Created Image = {created_image}")
        assert created_image.image_name == "TestImage"
        assert created_image.image_description == "Test Image Description"
        assert created_image.aircraft_id == created_aircraft.aircraft_id
        assert len(created_image.image_json.pointInfo) == 2
        assert created_image.image_json.fileInfo.filename == "test_image.jpg"

        # 测试查询 AircraftReferenceImage by ID
        print("\n=== 测试 AircraftReferenceImageMapper 查询功能 (by ID) ===")
        print(f"输入值: image_id = {created_image.image_id}")
        retrieved_image = AircraftReferenceImageMapper.get_by_id(created_image.image_id)
        print(f"返回值: Retrieved Image = {retrieved_image}")
        assert retrieved_image.image_id == created_image.image_id
        assert retrieved_image.image_name == "TestImage"
        assert retrieved_image.aircraft_id == created_aircraft.aircraft_id
        assert len(retrieved_image.image_json.pointInfo) == 2

        # 测试更新 AircraftReferenceImage
        print("\n=== 测试 AircraftReferenceImageMapper 更新功能 ===")
        updated_file_dto = FileDTO(
            download_url="http://example.com/updated_file",
            filename="updated_image.jpg",
            ipfs_cid="QmUpdatedCid",
            ipfs_path="/ipfs/updated",
            mfs_path="/mfs/updated",
            mime_type="image/png",
            size=2048,
            stored_filename="updated_stored.jpg",
            success=True,
            uploaded_at="2023-10-02T12:00:00"
        )
        updated_point_data = [
            AircraftReferenceImagePoint(id=1, x=15.5, y=25.5)
        ]
        updated_image_json = AircraftReferenceImageJson(
            fileInfo=updated_file_dto,
            pointInfo=updated_point_data
        )
        image_update_dto = AircraftReferenceImageUpdateDTO(
            image_name="UpdatedImage",
            image_description="Updated Image Description",
            image_json=updated_image_json
        )
        print(f"输入值: image_id = {created_image.image_id}, Update DTO = {image_update_dto}")
        updated_image = AircraftReferenceImageMapper.update(created_image.image_id, image_update_dto)
        print(f"返回值: Updated Image = {updated_image}")
        assert updated_image.image_name == "UpdatedImage"
        assert updated_image.image_description == "Updated Image Description"
        assert len(updated_image.image_json.pointInfo) == 1
        assert updated_image.image_json.fileInfo.filename == "updated_image.jpg"

        # 测试分页查询 AircraftReferenceImage
        print("\n=== 测试 AircraftReferenceImageMapper 分页查询功能 ===")
        print(f"输入值: image_name = 'UpdatedImage', aircraft_name = 'TestAircraft', page_num = 1, page_size = 10")
        search_result = AircraftReferenceImageMapper.search(
            image_name="UpdatedImage",
            aircraft_name="TestAircraft",
            page_num=1,
            page_size=10
        )
        print(f"返回值: Search Result = {search_result}")
        assert len(search_result.data) == 1
        assert search_result.data[0].image_name == "UpdatedImage"
        assert search_result.data[0].aircraft_name == "TestAircraft"
        assert search_result.pagination.current_page == 1
        assert search_result.pagination.total == 1

        # 测试分页查询 - 空结果
        print("\n=== 测试 AircraftReferenceImageMapper 分页查询功能 (空结果) ===")
        print(f"输入值: image_name = 'NonExistentImage', page_num = 1, page_size = 10")
        empty_search_result = AircraftReferenceImageMapper.search(
            image_name="NonExistentImage",
            page_num=1,
            page_size=10
        )
        print(f"返回值: Empty Search Result = {empty_search_result}")
        assert len(empty_search_result.data) == 0
        assert empty_search_result.pagination.total == 0

        # 测试查询不存在的 ID
        print("\n=== 测试 AircraftReferenceImageMapper 查询功能 (不存在的 ID) ===")
        print(f"输入值: image_id = 999999")
        non_existent_image = AircraftReferenceImageMapper.get_by_id("999999")
        print(f"返回值: Retrieved Image = {non_existent_image}")
        assert non_existent_image is None

        # 测试删除 AircraftReferenceImage
        print("\n=== 测试 AircraftReferenceImageMapper 删除功能 ===")
        print(f"输入值: image_id = {created_image.image_id}")
        delete_result = AircraftReferenceImageMapper.delete(created_image.image_id)
        print(f"返回值: Delete Result = {delete_result}")
        assert delete_result is True
        assert AircraftReferenceImageMapper.get_by_id(created_image.image_id) is None

        # 测试删除不存在的 ID
        print("\n=== 测试 AircraftReferenceImageMapper 删除功能 (不存在的 ID) ===")
        print(f"输入值: image_id = 999999")
        failed_delete_result = AircraftReferenceImageMapper.delete("999999")
        print(f"返回值: Delete Result = {failed_delete_result}")
        assert failed_delete_result is False
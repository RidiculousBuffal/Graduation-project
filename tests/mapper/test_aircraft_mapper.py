# tests/test_aircraft_mapper.py

from app.DTO.aircrafts import AircraftTypeCreateDTO, AircraftTypeUpdateDTO, AircraftCreateDTO, AircraftUpdateDTO
from app.mapper.aircraft.aircraftMapper import AircraftMapper
from app.mapper.aircraft.aircraftTypeMapper import AircraftTypeMapper


# 测试 AircraftTypeMapper
def test_aircraft_type_mapper_crud(app):
    with app.app_context():
        # 测试创建 AircraftType
        print("\n=== 测试 AircraftTypeMapper 创建功能 ===")
        create_dto = AircraftTypeCreateDTO(
            type_name="TestType",
            description="Test Description"
        )
        print(f"输入值: Create DTO = {create_dto}")
        created_type = AircraftTypeMapper.create(create_dto)
        print(f"返回值: Created AircraftType = {created_type}")
        assert created_type.type_name == "TestType"
        assert created_type.description == "Test Description"

        # 测试查询 AircraftType by ID
        print("\n=== 测试 AircraftTypeMapper 查询功能 (by ID) ===")
        print(f"输入值: typeid = {created_type.typeid}")
        retrieved_type = AircraftTypeMapper.get_by_id(created_type.typeid)
        print(f"返回值: Retrieved AircraftType = {retrieved_type}")
        assert retrieved_type.typeid == created_type.typeid
        assert retrieved_type.type_name == "TestType"

        # 测试更新 AircraftType
        print("\n=== 测试 AircraftTypeMapper 更新功能 ===")
        update_dto = AircraftTypeUpdateDTO(
            type_name="UpdatedType",
            description="Updated Description"
        )
        print(f"输入值: typeid = {created_type.typeid}, Update DTO = {update_dto}")
        updated_type = AircraftTypeMapper.update(created_type.typeid, update_dto)
        print(f"返回值: Updated AircraftType = {updated_type}")
        assert updated_type.type_name == "UpdatedType"
        assert updated_type.description == "Updated Description"

        # 测试分页查询 AircraftType
        print("\n=== 测试 AircraftTypeMapper 分页查询功能 ===")
        print(f"输入值: type_name = 'UpdatedType', pageNum = 1, pageSize = 10")
        search_result = AircraftTypeMapper.search(type_name="UpdatedType", pageNum=1, pageSize=10)
        print(f"返回值: Search Result = {search_result}")
        assert search_result.data[0].type_name == "UpdatedType"
        assert search_result.pagination.current_page == 1
        assert search_result.pagination.total == 1

        # 测试删除 AircraftType
        print("\n=== 测试 AircraftTypeMapper 删除功能 ===")
        print(f"输入值: typeid = {created_type.typeid}")
        delete_result = AircraftTypeMapper.delete(created_type.typeid)
        print(f"返回值: Delete Result = {delete_result}")
        assert delete_result is True
        assert AircraftTypeMapper.get_by_id(created_type.typeid) is None


# 测试 AircraftMapper
def test_aircraft_mapper_crud(app):
    with app.app_context():
        # 先创建关联的 AircraftType
        type_create_dto = AircraftTypeCreateDTO(
            type_name="AircraftType1",
            description="Aircraft Type Description"
        )
        created_type = AircraftTypeMapper.create(type_create_dto)

        # 测试创建 Aircraft
        print("\n=== 测试 AircraftMapper 创建功能 ===")
        aircraft_create_dto = AircraftCreateDTO(
            aircraft_name="TestAircraft",
            age=5,
            typeid=created_type.typeid
        )
        print(f"输入值: Create DTO = {aircraft_create_dto}")
        created_aircraft = AircraftMapper.create(aircraft_create_dto)
        print(f"返回值: Created Aircraft = {created_aircraft}")
        assert created_aircraft.aircraft_name == "TestAircraft"
        assert created_aircraft.age == 5
        assert created_aircraft.typeid == created_type.typeid
        assert created_aircraft.type_name == "AircraftType1"

        # 测试查询 Aircraft by ID
        print("\n=== 测试 AircraftMapper 查询功能 (by ID) ===")
        print(f"输入值: aircraft_id = {created_aircraft.aircraft_id}")
        retrieved_aircraft = AircraftMapper.get_by_id(created_aircraft.aircraft_id)
        print(f"返回值: Retrieved Aircraft = {retrieved_aircraft}")
        assert retrieved_aircraft.aircraft_id == created_aircraft.aircraft_id
        assert retrieved_aircraft.aircraft_name == "TestAircraft"

        # 测试更新 Aircraft
        print("\n=== 测试 AircraftMapper 更新功能 ===")
        aircraft_update_dto = AircraftUpdateDTO(
            aircraft_name="UpdatedAircraft",
            age=10,
            typeid=created_type.typeid
        )
        print(f"输入值: aircraft_id = {created_aircraft.aircraft_id}, Update DTO = {aircraft_update_dto}")
        updated_aircraft = AircraftMapper.update(created_aircraft.aircraft_id, aircraft_update_dto)
        print(f"返回值: Updated Aircraft = {updated_aircraft}")
        assert updated_aircraft.aircraft_name == "UpdatedAircraft"
        assert updated_aircraft.age == 10

        # 测试分页查询 Aircraft
        print("\n=== 测试 AircraftMapper 分页查询功能 ===")
        print(f"输入值: aircraftName = 'UpdatedAircraft', pageNum = 1, pageSize = 10")
        search_result = AircraftMapper.searchAircraft(
            aircraftName="UpdatedAircraft",
            pageNum=1,
            pageSize=10
        )
        print(f"返回值: Search Result = {search_result}")
        assert search_result.data[0].aircraft_name == "UpdatedAircraft"
        assert search_result.pagination.current_page == 1
        assert search_result.pagination.total == 1

        # 测试删除 Aircraft
        print("\n=== 测试 AircraftMapper 删除功能 ===")
        print(f"输入值: aircraft_id = {created_aircraft.aircraft_id}")
        delete_result = AircraftMapper.delete(created_aircraft.aircraft_id)
        print(f"返回值: Delete Result = {delete_result}")
        assert delete_result is True
        assert AircraftMapper.get_by_id(created_aircraft.aircraft_id) is None

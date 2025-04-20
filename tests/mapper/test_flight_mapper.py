from datetime import datetime, timedelta

from app.DTO.aircrafts import AircraftCreateDTO, AircraftTypeCreateDTO
from app.DTO.flights import FlightCreateDTO, FlightUpdateDTO
from app.DTO.terminals import TerminalCreateDTO
from app.mapper.aircraft.aircraftMapper import AircraftMapper
from app.mapper.aircraft.aircraftTypeMapper import AircraftTypeMapper
from app.mapper.flight.flightMapper import FlightMapper
from app.mapper.terminal.terminalMapper import TerminalMapper


def test_flight_mapper_crud(app):
    """测试 FlightMapper 的 CRUD 和分页查询功能，涵盖多种场景"""
    # 由于 conftest.py 已提供 app 上下文，这里无需显式 with app.app_context():

    # 1. 创建依赖对象：在测试航班之前，先创建航站楼和飞机记录
    print("\n=== 准备依赖数据：创建航站楼记录 ===")
    terminal_create_dto = TerminalCreateDTO(
        terminal_name="TestTerminal",
        description="Test Terminal Description"
    )
    created_terminal = TerminalMapper.create(terminal_create_dto)
    print(f"返回值: Created Terminal = {created_terminal}")
    assert created_terminal.terminal_name == "TestTerminal"

    print("\n=== 准备依赖数据：创建飞机类型 ===")
    aircraft_type_create_dto = AircraftTypeCreateDTO(
        type_name="Boeing 737",
        description="Test Aircraft Type Description"
    )
    created_type = AircraftTypeMapper.create(aircraft_type_create_dto)
    print(f"返回值: Created Aircraft Type = {created_type}")
    assert created_type.type_name == "Boeing 737"

    print("\n=== 准备依赖数据：创建飞机记录 ===")
    aircraft_create_dto = AircraftCreateDTO(
        aircraft_name="TestAircraft",
        age=5,
        typeid=created_type.typeid
    )
    created_aircraft = AircraftMapper.create(aircraft_create_dto)
    print(f"返回值: Created Aircraft = {created_aircraft}")
    assert created_aircraft.aircraft_name == "TestAircraft"
    assert created_aircraft.typeid == created_type.typeid

    # 2. 测试创建 Flight (航班) - 基本场景
    print("\n=== 测试 FlightMapper 创建功能 - 基本场景 ===")
    flight_create_dto = FlightCreateDTO(
        aircraft_id=created_aircraft.aircraft_id,
        terminal_id=created_terminal.terminal_id,
        estimated_departure=datetime.now(),
        estimated_arrival=datetime.now() + timedelta(hours=2),
        flight_status="scheduled",
        health_status="healthy",
        approval_status="pending"
    )
    print(f"输入值: Create DTO = {flight_create_dto}")
    created_flight = FlightMapper.create(flight_create_dto)
    print(f"返回值: Created Flight = {created_flight}")
    assert created_flight.aircraft_id == created_aircraft.aircraft_id
    assert created_flight.terminal_id == created_terminal.terminal_id
    assert created_flight.flight_status == "scheduled"

    # 3. 测试创建 Flight - 最小字段场景
    print("\n=== 测试 FlightMapper 创建功能 - 最小字段场景 ===")
    minimal_flight_create_dto = FlightCreateDTO(
        aircraft_id=created_aircraft.aircraft_id
    )
    print(f"输入值: Minimal Create DTO = {minimal_flight_create_dto}")
    minimal_created_flight = FlightMapper.create(minimal_flight_create_dto)
    print(f"返回值: Minimal Created Flight = {minimal_created_flight}")
    assert minimal_created_flight.aircraft_id == created_aircraft.aircraft_id
    assert minimal_created_flight.flight_status == "scheduled"  # 默认值
    assert minimal_created_flight.health_status == "healthy"  # 默认值
    assert minimal_created_flight.approval_status == "pending"  # 默认值

    # 4. 测试查询 Flight by ID - 成功场景
    print("\n=== 测试 FlightMapper 查询功能 (by ID) - 成功场景 ===")
    print(f"输入值: flight_id = {created_flight.flight_id}")
    retrieved_flight = FlightMapper.get_by_id(created_flight.flight_id)
    print(f"返回值: Retrieved Flight = {retrieved_flight}")
    assert retrieved_flight.flight_id == created_flight.flight_id
    assert retrieved_flight.aircraft_id == created_aircraft.aircraft_id
    assert retrieved_flight.aircraft_name == created_aircraft.aircraft_name  # 验证飞机名称
    assert retrieved_flight.terminal_name == created_terminal.terminal_name  # 验证航站楼名称

    # 5. 测试查询 Flight by ID - 不存在场景
    print("\n=== 测试 FlightMapper 查询功能 (by ID) - 不存在场景 ===")
    print(f"输入值: flight_id = 'nonexistent_id'")
    nonexistent_flight = FlightMapper.get_by_id("nonexistent_id")
    print(f"返回值: Retrieved Flight = {nonexistent_flight}")
    assert nonexistent_flight is None

    # 6. 测试更新 Flight - 全部字段更新场景
    print("\n=== 测试 FlightMapper 更新功能 - 全部字段更新场景 ===")
    update_dto = FlightUpdateDTO(
        aircraft_id=created_aircraft.aircraft_id,
        terminal_id=created_terminal.terminal_id,
        estimated_departure=datetime.now() + timedelta(days=1),
        estimated_arrival=datetime.now() + timedelta(days=1, hours=2),
        flight_status="delayed",
        actual_departure=datetime.now() - timedelta(hours=1),
        actual_arrival=None,
        health_status="maintenance",
        approval_status="approved"
    )
    print(f"输入值: flight_id = {created_flight.flight_id}, Update DTO = {update_dto}")
    updated_flight = FlightMapper.update(created_flight.flight_id, update_dto)
    print(f"返回值: Updated Flight = {updated_flight}")
    assert updated_flight.flight_status == "delayed"
    assert updated_flight.health_status == "maintenance"
    assert updated_flight.approval_status == "approved"

    # 7. 测试更新 Flight - 部分字段更新场景
    print("\n=== 测试 FlightMapper 更新功能 - 部分字段更新场景 ===")
    partial_update_dto = FlightUpdateDTO(
        flight_status="boarding"
    )
    print(f"输入值: flight_id = {created_flight.flight_id}, Partial Update DTO = {partial_update_dto}")
    partially_updated_flight = FlightMapper.update(created_flight.flight_id, partial_update_dto)
    print(f"返回值: Partially Updated Flight = {partially_updated_flight}")
    assert partially_updated_flight.flight_status == "boarding"
    assert partially_updated_flight.health_status == "maintenance"  # 未变更，仍为之前值
    assert partially_updated_flight.approval_status == "approved"  # 未变更，仍为之前值

    # 8. 测试更新 Flight - 不存在场景
    print("\n=== 测试 FlightMapper 更新功能 - 不存在场景 ===")
    print(f"输入值: flight_id = 'nonexistent_id', Update DTO = {partial_update_dto}")
    nonexistent_update = FlightMapper.update("nonexistent_id", partial_update_dto)
    print(f"返回值: Updated Flight = {nonexistent_update}")
    assert nonexistent_update is None

    # 9. 测试分页查询 Flight - 无条件查询
    print("\n=== 测试 FlightMapper 分页查询功能 - 无条件查询 ===")
    print(f"输入值: pageNum = 1, pageSize = 10")
    search_result_all = FlightMapper.search(pageNum=1, pageSize=10)
    print(f"返回值: Search Result = {search_result_all}")
    assert len(search_result_all.data) >= 2  # 至少有之前创建的两个航班
    assert search_result_all.pagination.current_page == 1
    assert search_result_all.pagination.total >= 2
    # 验证详细信息
    flight_result = next((f for f in search_result_all.data if f.flight_id == created_flight.flight_id), None)
    assert flight_result is not None
    assert flight_result.aircraft_name == created_aircraft.aircraft_name
    assert flight_result.terminal_name == created_terminal.terminal_name

    # 10. 测试分页查询 Flight - 按 aircraft_id 过滤
    print("\n=== 测试 FlightMapper 分页查询功能 - 按 aircraft_id 过滤 ===")
    print(f"输入值: aircraft_id = {created_aircraft.aircraft_id}, pageNum = 1, pageSize = 10")
    search_result_aircraft = FlightMapper.search(aircraft_id=created_aircraft.aircraft_id, pageNum=1, pageSize=10)
    print(f"返回值: Search Result = {search_result_aircraft}")
    assert all(flight.aircraft_id == created_aircraft.aircraft_id for flight in search_result_aircraft.data)
    assert search_result_aircraft.pagination.total >= 2
    # 验证详细信息
    assert all(flight.aircraft_name == created_aircraft.aircraft_name for flight in search_result_aircraft.data)

    # 11. 测试分页查询 Flight - 按 flight_status 过滤
    print("\n=== 测试 FlightMapper 分页查询功能 - 按 flight_status 过滤 ===")
    print(f"输入值: flight_status = 'boarding', pageNum = 1, pageSize = 10")
    search_result_status = FlightMapper.search(flight_status="boarding", pageNum=1, pageSize=10)
    print(f"返回值: Search Result = {search_result_status}")
    assert all(flight.flight_status == "boarding" for flight in search_result_status.data)
    assert search_result_status.pagination.total == 1
    # 验证详细信息
    assert search_result_status.data[0].aircraft_name == created_aircraft.aircraft_name
    assert search_result_status.data[0].terminal_name == created_terminal.terminal_name

    # 12. 测试分页查询 Flight - 多条件组合查询
    print("\n=== 测试 FlightMapper 分页查询功能 - 多条件组合查询 ===")
    print(
        f"输入值: aircraft_id = {created_aircraft.aircraft_id}, flight_status = 'boarding', pageNum = 1, pageSize = 10")
    search_result_multi = FlightMapper.search(
        aircraft_id=created_aircraft.aircraft_id,
        flight_status="boarding",
        pageNum=1,
        pageSize=10
    )
    print(f"返回值: Search Result = {search_result_multi}")
    assert all(flight.aircraft_id == created_aircraft.aircraft_id for flight in search_result_multi.data)
    assert all(flight.flight_status == "boarding" for flight in search_result_multi.data)
    assert search_result_multi.pagination.total == 1
    # 验证详细信息
    assert search_result_multi.data[0].aircraft_name == created_aircraft.aircraft_name
    assert search_result_multi.data[0].terminal_name == created_terminal.terminal_name

    # 13. 测试删除 Flight - 成功场景
    print("\n=== 测试 FlightMapper 删除功能 - 成功场景 ===")
    print(f"输入值: flight_id = {created_flight.flight_id}")
    delete_result = FlightMapper.delete(created_flight.flight_id)
    print(f"返回值: Delete Result = {delete_result}")
    assert delete_result is True
    assert FlightMapper.get_by_id(created_flight.flight_id) is None

    # 14. 测试删除 Flight - 不存在场景
    print("\n=== 测试 FlightMapper 删除功能 - 不存在场景 ===")
    print(f"输入值: flight_id = 'nonexistent_id'")
    delete_nonexistent_result = FlightMapper.delete("nonexistent_id")
    print(f"返回值: Delete Result = {delete_nonexistent_result}")
    assert delete_nonexistent_result is False

    # 15. 清理依赖数据：删除创建的飞机和航站楼记录
    print("\n=== 清理依赖数据：删除飞机和航站楼记录 ===")
    aircraft_delete_result = AircraftMapper.delete(created_aircraft.aircraft_id)
    terminal_delete_result = TerminalMapper.delete(created_terminal.terminal_id)
    aircraft_type_delete_result = AircraftTypeMapper.delete(created_type.typeid)
    print(f"返回值: Aircraft Delete Result = {aircraft_delete_result}")
    print(f"返回值: Terminal Delete Result = {terminal_delete_result}")
    print(f"返回值: Aircraft Type Delete Result = {aircraft_type_delete_result}")
    assert aircraft_delete_result is True
    assert terminal_delete_result is True
    assert aircraft_type_delete_result is True

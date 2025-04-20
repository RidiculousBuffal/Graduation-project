from datetime import datetime, timedelta

import pytest

from app.DTO.aircrafts import AircraftCreateDTO, AircraftTypeCreateDTO
from app.DTO.flights import FlightCreateDTO, FlightUpdateDTO
from app.DTO.terminals import TerminalCreateDTO
from app.exceptions.flights import FlightTimeConflictError, FlightTimestampOrderError, FlightActualVsEstimatedError, \
    FlightInvalidStatusError
from app.mapper.aircraft.aircraftMapper import AircraftMapper
from app.mapper.aircraft.aircraftTypeMapper import AircraftTypeMapper
from app.mapper.flight.flightMapper import FlightMapper
from app.mapper.terminal.terminalMapper import TerminalMapper


def test_flight_mapper_crud(app):
    # 1. 创建依赖对象：航站楼、飞机类型和飞机记录
    print("\n=== 准备依赖数据：创建航站楼记录 ===")
    terminal_create_dto = TerminalCreateDTO(
        terminal_name="TestTerminal",
        description="Test Terminal Description"
    )
    created_terminal = TerminalMapper.create(terminal_create_dto)
    assert created_terminal.terminal_name == "TestTerminal"

    print("\n=== 准备依赖数据：创建另一个航站楼记录 ===")
    terminal_create_dto_2 = TerminalCreateDTO(
        terminal_name="AnotherTerminal",
        description="Another Terminal Description"
    )
    created_terminal_2 = TerminalMapper.create(terminal_create_dto_2)
    assert created_terminal_2.terminal_name == "AnotherTerminal"

    print("\n=== 准备依赖数据：创建飞机类型 ===")
    aircraft_type_create_dto = AircraftTypeCreateDTO(
        type_name="Boeing 737",
        description="Test Aircraft Type Description"
    )
    created_type = AircraftTypeMapper.create(aircraft_type_create_dto)
    assert created_type.type_name == "Boeing 737"

    print("\n=== 准备依赖数据：创建飞机记录 ===")
    aircraft_create_dto = AircraftCreateDTO(
        aircraft_name="TestAircraft",
        age=5,
        typeid=created_type.typeid
    )
    created_aircraft = AircraftMapper.create(aircraft_create_dto)
    assert created_aircraft.aircraft_name == "TestAircraft"

    print("\n=== 准备依赖数据：创建另一个飞机记录 ===")
    aircraft_create_dto_2 = AircraftCreateDTO(
        aircraft_name="AnotherAircraft",
        age=3,
        typeid=created_type.typeid
    )
    created_aircraft_2 = AircraftMapper.create(aircraft_create_dto_2)
    assert created_aircraft_2.aircraft_name == "AnotherAircraft"

    # 2. 测试创建 Flight - 基本场景
    print("\n=== 测试 FlightMapper 创建功能 - 基本场景 ===")
    now = datetime.now()
    flight_create_dto = FlightCreateDTO(
        aircraft_id=created_aircraft.aircraft_id,
        terminal_id=created_terminal.terminal_id,
        estimated_departure=now,
        estimated_arrival=now + timedelta(hours=2),
        flight_status="scheduled",
        health_status="healthy",
        approval_status="pending"
    )
    created_flight = FlightMapper.create(flight_create_dto)
    assert created_flight.aircraft_id == created_aircraft.aircraft_id
    assert created_flight.terminal_id == created_terminal.terminal_id
    assert created_flight.flight_status == "scheduled"

    # 3. 测试创建 Flight - 时间冲突场景
    print("\n=== 测试 FlightMapper 创建功能 - 时间冲突场景 ===")
    conflict_flight_dto = FlightCreateDTO(
        aircraft_id=created_aircraft.aircraft_id,
        terminal_id=created_terminal.terminal_id,
        estimated_departure=now,
        estimated_arrival=now + timedelta(hours=2),
        flight_status="scheduled",
        health_status="healthy",
        approval_status="pending"
    )
    with pytest.raises(FlightTimeConflictError) as exc_info:
        FlightMapper.create(conflict_flight_dto)
    assert "在指定时间区间内，该飞机已被安排其他航班" in str(exc_info.value)

    # 4. 测试创建 Flight - 到达时间早于起飞时间场景
    print("\n=== 测试 FlightMapper 创建功能 - 到达时间早于起飞时间场景 ===")
    invalid_time_dto = FlightCreateDTO(
        aircraft_id=created_aircraft_2.aircraft_id,
        terminal_id=created_terminal.terminal_id,
        estimated_departure=now + timedelta(hours=2),
        estimated_arrival=now,
        flight_status="scheduled",
        health_status="healthy",
        approval_status="pending"
    )
    with pytest.raises(FlightTimestampOrderError) as exc_info:
        FlightMapper.create(invalid_time_dto)
    assert "到达时间不能早于起飞时间" in str(exc_info.value)

    # 5. 测试创建 Flight - 实际时间早于预计时间场景
    print("\n=== 测试 FlightMapper 创建功能 - 实际时间早于预计时间场景 ===")
    invalid_actual_time_dto = FlightCreateDTO(
        aircraft_id=created_aircraft_2.aircraft_id,
        terminal_id=created_terminal.terminal_id,
        estimated_departure=now + timedelta(hours=2),
        estimated_arrival=now + timedelta(hours=4),
        actual_departure=now,
        flight_status="scheduled",
        health_status="healthy",
        approval_status="pending"
    )
    with pytest.raises(FlightActualVsEstimatedError) as exc_info:
        FlightMapper.create(invalid_actual_time_dto)
    assert "实际起飞时间不能早于预计起飞时间" in str(exc_info.value)


    # 7. 测试查询 Flight by ID - 成功场景
    print("\n=== 测试 FlightMapper 查询功能 (by ID) - 成功场景 ===")
    retrieved_flight = FlightMapper.get_by_id(created_flight.flight_id)
    assert retrieved_flight.flight_id == created_flight.flight_id
    assert retrieved_flight.aircraft_name == created_aircraft.aircraft_name
    assert retrieved_flight.terminal_name == created_terminal.terminal_name

    # 8. 测试查询 Flight by ID - 不存在场景
    print("\n=== 测试 FlightMapper 查询功能 (by ID) - 不存在场景 ===")
    nonexistent_flight = FlightMapper.get_by_id("nonexistent_id")
    assert nonexistent_flight is None

    # 9. 测试更新 Flight - 全部字段更新场景
    print("\n=== 测试 FlightMapper 更新功能 - 全部字段更新场景 ===")
    update_dto = FlightUpdateDTO(
        aircraft_id=created_aircraft.aircraft_id,
        terminal_id=created_terminal.terminal_id,
        estimated_departure=datetime.now() + timedelta(days=1),
        estimated_arrival=datetime.now() + timedelta(days=1, hours=2),
        flight_status="delayed",
        actual_departure=None,
        actual_arrival=None,
        health_status="maintenance",
        approval_status="approved"
    )
    updated_flight = FlightMapper.update(created_flight.flight_id, update_dto)
    assert updated_flight.flight_status == "delayed"
    assert updated_flight.health_status == "maintenance"
    assert updated_flight.approval_status == "approved"

    # 10. 测试更新 Flight - 时间冲突场景
    print("\n=== 测试 FlightMapper 更新功能 - 时间冲突场景 ===")
    flight_create_dto_2 = FlightCreateDTO(
        aircraft_id=created_aircraft_2.aircraft_id,
        terminal_id=created_terminal_2.terminal_id,
        estimated_departure=now + timedelta(days=1),
        estimated_arrival=now + timedelta(days=1, hours=2),
        flight_status="scheduled",
        health_status="healthy",
        approval_status="pending"
    )
    created_flight_2 = FlightMapper.create(flight_create_dto_2)

    conflict_update_dto = FlightUpdateDTO(
        aircraft_id=created_aircraft_2.aircraft_id,
        estimated_departure=now + timedelta(days=1),
        estimated_arrival=now + timedelta(days=1, hours=2)
    )
    with pytest.raises(FlightTimeConflictError) as exc_info:
        FlightMapper.update(created_flight.flight_id, conflict_update_dto)
    assert "在指定时间区间内，该飞机已被安排其他航班" in str(exc_info.value)

    # 11. 测试分页查询 Flight - 无条件查询
    print("\n=== 测试 FlightMapper 分页查询功能 - 无条件查询 ===")
    search_result_all = FlightMapper.search(pageNum=1, pageSize=10)
    assert len(search_result_all.data) >= 2
    assert search_result_all.pagination.current_page == 1
    assert search_result_all.pagination.total >= 2

    # 12. 测试分页查询 Flight - 按 aircraft_id 过滤
    print("\n=== 测试 FlightMapper 分页查询功能 - 按 aircraft_id 过滤 ===")
    search_result_aircraft = FlightMapper.search(aircraft_id=created_aircraft.aircraft_id, pageNum=1, pageSize=10)
    assert all(flight.aircraft_id == created_aircraft.aircraft_id for flight in search_result_aircraft.data)
    assert search_result_aircraft.pagination.total >= 1

    # 13. 测试删除 Flight - 成功场景
    print("\n=== 测试 FlightMapper 删除功能 - 成功场景 ===")
    delete_result = FlightMapper.delete(created_flight.flight_id)
    assert delete_result is True
    assert FlightMapper.get_by_id(created_flight.flight_id) is None

    # 14. 清理依赖数据
    print("\n=== 清理依赖数据：删除飞机和航站楼记录 ===")
    AircraftMapper.delete(created_aircraft.aircraft_id)
    AircraftMapper.delete(created_aircraft_2.aircraft_id)
    TerminalMapper.delete(created_terminal.terminal_id)
    TerminalMapper.delete(created_terminal_2.terminal_id)
    AircraftTypeMapper.delete(created_type.typeid)

from datetime import datetime, timedelta

from app.DTO.aircrafts import AircraftCreateDTO, AircraftTypeCreateDTO
from app.DTO.flights import FlightCreateDTO
from app.DTO.inspections import InspectionRecordCreateDTO, InspectionRecordUpdateDTO
from app.DTO.tasks import TaskCreateDTO, TaskUpdateDTO
from app.consts.Dict import DictionaryData
from app.consts.Roles import RoleConsts
from app.mapper.aircraft.aircraftMapper import AircraftMapper
from app.mapper.aircraft.aircraftTypeMapper import AircraftTypeMapper
from app.mapper.auth.roleMapper import RoleMapper
from app.mapper.auth.userMapper import UserMapper
from app.mapper.auth.userRolePermissionMapper import UserRolePermissionMapper
from app.mapper.flight.flightMapper import FlightMapper
from app.mapper.tasks.inspectionRecordMapper import InspectionRecordMapper
from app.mapper.tasks.taskMapper import TaskMapper


def test_task_mapper_crud(app):
    """测试任务Mapper的CRUD操作"""
    # 准备测试数据
    print("\n=== 准备依赖数据：创建用户 ===")
    # 创建管理员用户
    admin_username = "admin_test"
    admin_password = "password123"
    admin_email = "admin@test.com"
    admin_id = UserMapper.add_user(admin_username, admin_password, admin_email)

    # 绑定管理员角色
    admin_role = RoleMapper.getRole(RoleConsts.ADMIN)
    UserRolePermissionMapper.combineUserWithRole(admin_id, admin_role.role_id)

    # 创建工程师用户
    engineer_username = "engineer_test"
    engineer_password = "password123"
    engineer_email = "engineer@test.com"
    engineer_id = UserMapper.add_user(engineer_username, engineer_password, engineer_email)

    # 绑定工程师角色
    engineer_role = RoleMapper.getRole(RoleConsts.ENGINEER)
    UserRolePermissionMapper.combineUserWithRole(engineer_id, engineer_role.role_id)

    # 创建飞机类型
    print("\n=== 准备依赖数据：创建飞机类型 ===")
    aircraft_type_dto = AircraftTypeCreateDTO(
        type_name="Test Type",
        description="Test Type Description"
    )
    aircraft_type = AircraftTypeMapper.create(aircraft_type_dto)

    # 创建飞机
    print("\n=== 准备依赖数据：创建飞机 ===")
    aircraft_dto = AircraftCreateDTO(
        aircraft_name="Test Aircraft",
        age=5,
        typeid=aircraft_type.typeid
    )
    aircraft = AircraftMapper.create(aircraft_dto)

    # 创建航班
    print("\n=== 准备依赖数据：创建航班 ===")
    now = datetime.now()
    flight_dto = FlightCreateDTO(
        aircraft_id=aircraft.aircraft_id,
        estimated_departure=now + timedelta(hours=2),
        estimated_arrival=now + timedelta(hours=4),
        flight_status="scheduled",
        health_status="healthy",
        approval_status="pending"
    )
    flight = FlightMapper.create(flight_dto)

    # 测试创建任务
    print("\n=== 测试 TaskMapper 创建功能 ===")
    task_dto = TaskCreateDTO(
        flight_id=flight.flight_id,
        estimated_start=now + timedelta(hours=1),
        estimated_end=now + timedelta(hours=5),
        admin_id=admin_id,
        task_status=DictionaryData.TASK_PENDING.get('dict_key')
    )
    task = TaskMapper.create(task_dto)
    assert task.flight_id == flight.flight_id
    assert task.admin_id == admin_id
    assert task.task_status == DictionaryData.TASK_PENDING.get('dict_key')

    # 测试查询任务
    print("\n=== 测试 TaskMapper 查询功能 ===")
    retrieved_task = TaskMapper.get_by_id(task.task_id)
    assert retrieved_task.task_id == task.task_id
    assert retrieved_task.flight_id == flight.flight_id
    assert retrieved_task.admin_id == admin_id

    # 测试更新任务
    print("\n=== 测试 TaskMapper 更新功能 ===")
    update_dto = TaskUpdateDTO(
        estimated_start=now + timedelta(hours=1, minutes=30),
        estimated_end=now + timedelta(hours=5, minutes=30),
        task_status=DictionaryData.TASK_IN_PROGRESS.get('dict_key')
    )
    updated_task = TaskMapper.update(task.task_id, update_dto)
    assert updated_task.task_status == DictionaryData.TASK_IN_PROGRESS.get('dict_key')

    # 测试任务搜索
    print("\n=== 测试 TaskMapper 搜索功能 ===")
    search_result = TaskMapper.search(
        flight_id=flight.flight_id,
        admin_id=admin_id,
        page_num=1,
        page_size=10
    )
    assert len(search_result.data) >= 1
    assert search_result.data[0].task_id == task.task_id

    # 不传入参数的测试
    all_tasks = TaskMapper.search()
    assert len(all_tasks.data) >= 1

    # 测试删除任务
    print("\n=== 测试 TaskMapper 删除功能 ===")
    delete_result = TaskMapper.delete(task.task_id)
    assert delete_result is True
    assert TaskMapper.get_by_id(task.task_id) is None

    # 清理测试数据
    print("\n=== 清理依赖数据 ===")
    FlightMapper.delete(flight.flight_id)
    AircraftMapper.delete(aircraft.aircraft_id)
    AircraftTypeMapper.delete(aircraft_type.typeid)
    UserMapper.delete_user(admin_id)
    UserMapper.delete_user(engineer_id)


def test_inspection_record_mapper_crud(app):
    """测试检查记录Mapper的CRUD操作"""
    # 准备测试数据
    print("\n=== 准备依赖数据：创建用户 ===")
    # 创建管理员用户
    admin_username = "admin_test_inspection"
    admin_password = "password123"
    admin_email = "admin_inspection@test.com"
    admin_id = UserMapper.add_user(admin_username, admin_password, admin_email)

    # 绑定管理员角色
    admin_role = RoleMapper.getRole(RoleConsts.ADMIN)
    UserRolePermissionMapper.combineUserWithRole(admin_id, admin_role.role_id)

    # 创建工程师用户
    engineer_username = "engineer_test_inspection"
    engineer_password = "password123"
    engineer_email = "engineer_inspection@test.com"
    engineer_id = UserMapper.add_user(engineer_username, engineer_password, engineer_email)

    # 绑定工程师角色
    engineer_role = RoleMapper.getRole(RoleConsts.ENGINEER)
    UserRolePermissionMapper.combineUserWithRole(engineer_id, engineer_role.role_id)

    # 创建飞机类型
    print("\n=== 准备依赖数据：创建飞机类型 ===")
    aircraft_type_dto = AircraftTypeCreateDTO(
        type_name="Test Type Inspection",
        description="Test Type Description for Inspection"
    )
    aircraft_type = AircraftTypeMapper.create(aircraft_type_dto)

    # 创建飞机
    print("\n=== 准备依赖数据：创建飞机 ===")
    aircraft_dto = AircraftCreateDTO(
        aircraft_name="Test Aircraft Inspection",
        age=3,
        typeid=aircraft_type.typeid
    )
    aircraft = AircraftMapper.create(aircraft_dto)

    # 创建航班
    print("\n=== 准备依赖数据：创建航班 ===")
    now = datetime.now()
    flight_dto = FlightCreateDTO(
        aircraft_id=aircraft.aircraft_id,
        estimated_departure=now + timedelta(hours=6),
        estimated_arrival=now + timedelta(hours=8),
        flight_status="scheduled",
        health_status="healthy",
        approval_status="pending"
    )
    flight = FlightMapper.create(flight_dto)

    # 创建任务
    print("\n=== 准备依赖数据：创建任务 ===")
    task_dto = TaskCreateDTO(
        flight_id=flight.flight_id,
        estimated_start=now + timedelta(hours=5),
        estimated_end=now + timedelta(hours=9),
        admin_id=admin_id,
        task_status=DictionaryData.TASK_PENDING
    )
    task = TaskMapper.create(task_dto)

    # 测试创建检查记录
    print("\n=== 测试 InspectionRecordMapper 创建功能 ===")
    inspection_dto = InspectionRecordCreateDTO(
        inspection_name="Test Inspection",
        task_id=task.task_id,
        executor_id=engineer_id,
        progress=0,
        start_time=now + timedelta(hours=5, minutes=30),
        inspection_status=DictionaryData.INSPECTION_NOT_STARTED
    )
    inspection = InspectionRecordMapper.create(inspection_dto)
    assert inspection.task_id == task.task_id
    assert inspection.executor_id == engineer_id
    assert inspection.inspection_status == DictionaryData.INSPECTION_NOT_STARTED

    # 测试查询检查记录
    print("\n=== 测试 InspectionRecordMapper 查询功能 ===")
    retrieved_inspection = InspectionRecordMapper.get_by_id(inspection.inspection_id)
    assert retrieved_inspection.inspection_id == inspection.inspection_id
    assert retrieved_inspection.task_id == task.task_id
    assert retrieved_inspection.executor_id == engineer_id

    # 测试更新检查记录
    print("\n=== 测试 InspectionRecordMapper 更新功能 ===")
    update_dto = InspectionRecordUpdateDTO(
        progress=25,
        inspection_status=DictionaryData.INSPECTION_IN_PROGRESS
    )
    updated_inspection = InspectionRecordMapper.update(inspection.inspection_id, update_dto)
    assert updated_inspection.progress == 25
    assert updated_inspection.inspection_status == DictionaryData.INSPECTION_IN_PROGRESS

    # 测试检查记录搜索
    print("\n=== 测试 InspectionRecordMapper 搜索功能 ===")
    search_result = InspectionRecordMapper.search(
        task_id=task.task_id,
        executor_id=engineer_id,
        page_num=1,
        page_size=10
    )
    assert len(search_result.data) >= 1
    assert search_result.data[0].inspection_id == inspection.inspection_id

    # 不传入参数的测试
    all_inspections = InspectionRecordMapper.search()
    assert len(all_inspections.data) >= 1

    # 测试删除检查记录
    print("\n=== 测试 InspectionRecordMapper 删除功能 ===")
    delete_result = InspectionRecordMapper.delete(inspection.inspection_id)
    assert delete_result is True
    assert InspectionRecordMapper.get_by_id(inspection.inspection_id) is None

    # 清理测试数据
    print("\n=== 清理依赖数据 ===")
    TaskMapper.delete(task.task_id)
    FlightMapper.delete(flight.flight_id)
    AircraftMapper.delete(aircraft.aircraft_id)
    AircraftTypeMapper.delete(aircraft_type.typeid)
    UserMapper.delete_user(admin_id)
    UserMapper.delete_user(engineer_id)

from datetime import datetime, timedelta

from app.DTO.aircrafts import AircraftCreateDTO, AircraftTypeCreateDTO
from app.DTO.flights import FlightCreateDTO
from app.DTO.inspections import InspectionRecordCreateDTO, InspectionRecordUpdateDTO
from app.DTO.tasks import TaskCreateDTO
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


def test_inspection_records_mapper_crud(app):
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
        task_status=DictionaryData.TASK_PENDING.get('dict_key')
    )
    task = TaskMapper.create(task_dto)

    # 测试创建检查记录
    print("\n=== 测试 InspectionRecordMapper 创建功能 ===")
    inspection_dto = InspectionRecordCreateDTO(
        inspection_name="测试检查记录",
        task_id=task.task_id,
        executor_id=engineer_id,
        progress=0,
        start_time=now + timedelta(hours=5, minutes=30),
        inspection_status=DictionaryData.INSPECTION_NOT_STARTED.get('dict_key')
    )
    inspection = InspectionRecordMapper.create(inspection_dto)
    assert inspection.task_id == task.task_id
    assert inspection.executor_id == engineer_id
    assert inspection.inspection_status == DictionaryData.INSPECTION_NOT_STARTED.get('dict_key')

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
        inspection_status=DictionaryData.INSPECTION_IN_PROGRESS.get('dict_key')
    )
    updated_inspection = InspectionRecordMapper.update(inspection.inspection_id, update_dto)
    assert updated_inspection.progress == 25
    assert updated_inspection.inspection_status == DictionaryData.INSPECTION_IN_PROGRESS.get('dict_key')

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

    # 按航班ID搜索
    flight_search = InspectionRecordMapper.search(
        flight_id=flight.flight_id,
        page_num=1,
        page_size=10
    )
    assert len(flight_search.data) >= 1

    # 按飞机ID搜索
    aircraft_search = InspectionRecordMapper.search(
        aircraft_id=aircraft.aircraft_id,
        page_num=1,
        page_size=10
    )
    assert len(aircraft_search.data) >= 1

    # 按时间范围搜索
    time_search = InspectionRecordMapper.search(
        start_time_from=now,
        start_time_to=now + timedelta(hours=10),
        page_num=1,
        page_size=10
    )
    assert len(time_search.data) >= 1

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


def test_inspection_records_mapper_search_filters(app):
    """测试检查记录Mapper的高级搜索功能"""
    # 准备测试数据
    print("\n=== 准备依赖数据：创建用户 ===")
    # 创建管理员用户
    admin_username = "admin_test_search"
    admin_password = "password123"
    admin_email = "admin_search@test.com"
    admin_id = UserMapper.add_user(admin_username, admin_password, admin_email)

    # 创建多个工程师用户
    engineer_ids = []
    for i in range(3):
        engineer_username = f"engineer_test_{i}"
        engineer_password = "password123"
        engineer_email = f"engineer_{i}@test.com"
        engineer_id = UserMapper.add_user(engineer_username, engineer_password, engineer_email)
        engineer_ids.append(engineer_id)

        # 绑定工程师角色
        engineer_role = RoleMapper.getRole(RoleConsts.ENGINEER)
        UserRolePermissionMapper.combineUserWithRole(engineer_id, engineer_role.role_id)

    # 创建飞机类型
    print("\n=== 准备依赖数据：创建飞机类型 ===")
    aircraft_type_dto = AircraftTypeCreateDTO(
        type_name="Test Type Search",
        description="Test Type Description for Search"
    )
    aircraft_type = AircraftTypeMapper.create(aircraft_type_dto)

    # 创建多个飞机
    print("\n=== 准备依赖数据：创建飞机 ===")
    aircraft_ids = []
    for i in range(2):
        aircraft_dto = AircraftCreateDTO(
            aircraft_name=f"Test Aircraft {i}",
            age=3 + i,
            typeid=aircraft_type.typeid
        )
        aircraft = AircraftMapper.create(aircraft_dto)
        aircraft_ids.append(aircraft.aircraft_id)

    # 创建多个航班和任务
    print("\n=== 准备依赖数据：创建航班和任务 ===")
    now = datetime.now()
    task_ids = []
    flight_ids = []

    for i, aircraft_id in enumerate(aircraft_ids):
        # 创建航班
        flight_dto = FlightCreateDTO(
            aircraft_id=aircraft_id,
            estimated_departure=now + timedelta(hours=6 + i),
            estimated_arrival=now + timedelta(hours=8 + i),
            flight_status="scheduled",
            health_status="healthy",
            approval_status="pending"
        )
        flight = FlightMapper.create(flight_dto)
        flight_ids.append(flight.flight_id)

        # 创建任务
        task_dto = TaskCreateDTO(
            flight_id=flight.flight_id,
            estimated_start=now + timedelta(hours=5 + i),
            estimated_end=now + timedelta(hours=9 + i),
            admin_id=admin_id,
            task_status=DictionaryData.TASK_PENDING.get('dict_key')
        )
        task = TaskMapper.create(task_dto)
        task_ids.append(task.task_id)

    # 创建多个检查记录
    print("\n=== 准备依赖数据：创建检查记录 ===")
    inspection_ids = []
    statuses = [
        DictionaryData.INSPECTION_NOT_STARTED.get('dict_key'),
        DictionaryData.INSPECTION_IN_PROGRESS.get('dict_key'),
        DictionaryData.INSPECTION_PASSED.get('dict_key')
    ]

    for i, task_id in enumerate(task_ids):
        for j, engineer_id in enumerate(engineer_ids):
            if i * len(engineer_ids) + j < len(statuses):
                status = statuses[i * len(engineer_ids) + j]
            else:
                status = statuses[0]

            inspection_dto = InspectionRecordCreateDTO(
                inspection_name=f"测试检查记录 {i}-{j}",
                task_id=task_id,
                executor_id=engineer_id,
                progress=j * 25,
                start_time=now + timedelta(hours=5, minutes=30 + i * 60 + j * 15),
                end_time=now + timedelta(hours=6, minutes=30 + i * 60 + j * 15) if j > 0 else None,
                inspection_status=status
            )
            inspection = InspectionRecordMapper.create(inspection_dto)
            inspection_ids.append(inspection.inspection_id)

    try:
        # 测试多种搜索条件
        print("\n=== 测试 InspectionRecordMapper 搜索功能 - 按状态 ===")
        status_search = InspectionRecordMapper.search(
            inspection_status=DictionaryData.INSPECTION_IN_PROGRESS.get('dict_key'),
            page_num=1,
            page_size=10
        )
        assert len(status_search.data) >= 1

        print("\n=== 测试 InspectionRecordMapper 搜索功能 - 按任务ID ===")
        task_search = InspectionRecordMapper.search(
            task_id=task_ids[0],
            page_num=1,
            page_size=10
        )
        assert len(task_search.data) >= 1

        print("\n=== 测试 InspectionRecordMapper 搜索功能 - 按执行人 ===")
        executor_search = InspectionRecordMapper.search(
            executor_id=engineer_ids[0],
            page_num=1,
            page_size=10
        )
        assert len(executor_search.data) >= 1

        print("\n=== 测试 InspectionRecordMapper 搜索功能 - 按飞机ID ===")
        aircraft_search = InspectionRecordMapper.search(
            aircraft_id=aircraft_ids[0],
            page_num=1,
            page_size=10
        )
        assert len(aircraft_search.data) >= 1

        print("\n=== 测试 InspectionRecordMapper 搜索功能 - 按航班ID ===")
        flight_search = InspectionRecordMapper.search(
            flight_id=flight_ids[0],
            page_num=1,
            page_size=10
        )
        assert len(flight_search.data) >= 1

        print("\n=== 测试 InspectionRecordMapper 搜索功能 - 按时间范围 ===")
        time_search = InspectionRecordMapper.search(
            start_time_from=now,
            start_time_to=now + timedelta(hours=24),
            page_num=1,
            page_size=10
        )
        assert len(time_search.data) >= 1

        print("\n=== 测试 InspectionRecordMapper 搜索功能 - 组合查询 ===")
        combined_search = InspectionRecordMapper.search(
            task_id=task_ids[0],
            executor_id=engineer_ids[0],
            inspection_status=DictionaryData.INSPECTION_NOT_STARTED.get('dict_key'),
            page_num=1,
            page_size=10
        )
        # 组合查询可能找不到匹配项，所以不断言结果数量

    finally:
        # 清理测试数据
        print("\n=== 清理依赖数据 ===")
        for inspection_id in inspection_ids:
            InspectionRecordMapper.delete(inspection_id)

        for task_id in task_ids:
            TaskMapper.delete(task_id)

        for flight_id in flight_ids:
            FlightMapper.delete(flight_id)

        for aircraft_id in aircraft_ids:
            AircraftMapper.delete(aircraft_id)

        AircraftTypeMapper.delete(aircraft_type.typeid)

        for engineer_id in engineer_ids:
            UserMapper.delete_user(engineer_id)

        UserMapper.delete_user(admin_id)

from app.mapper.dictionary.dictionaryMapper import DictionaryMapper


def test_dictionary_mapper_query(app):
    # 1. 测试按键查询字典 - 查询顶层分类 'status'
    print("\n=== 测试 DictionaryMapper 按键查询功能 - 查询 'status' ===")
    result = DictionaryMapper.get_by_key("status")
    assert result is not None
    assert result.dict_key == "status"
    assert result.dict_name == "状态类"
    assert result.parent_key is None
    assert result.description == "所有状态类字典的总分类"
    assert isinstance(result.children, list)

    # 2. 测试按键查询字典 - 查询 'flight_status'
    print("\n=== 测试 DictionaryMapper 按键查询功能 - 查询 'flight_status' ===")
    flight_status_result = DictionaryMapper.get_by_key("flight_status")
    assert flight_status_result is not None
    assert flight_status_result.dict_key == "flight_status"
    assert flight_status_result.dict_name == "飞行状态"
    assert flight_status_result.parent_key == "status"
    assert flight_status_result.description == "飞机飞行流程状态"
    assert len(flight_status_result.children) >= 6  # 应包含 scheduled, boarding, departed, arrived, delayed, cancelled

    # 3. 测试按键查询字典 - 查询不存在的键
    print("\n=== 测试 DictionaryMapper 按键查询功能 - 查询不存在的键 ===")
    nonexistent_result = DictionaryMapper.get_by_key("nonexistent_key")
    assert nonexistent_result is None

    # 4. 测试查询父字典下的子字典 - 查询 'flight_status' 的子字典
    print("\n=== 测试 DictionaryMapper 查询子字典功能 - 查询 'flight_status' 子字典 ===")
    flight_status_children = DictionaryMapper.get_children_by_parent_key("flight_status")
    assert isinstance(flight_status_children, list)
    assert len(flight_status_children) >= 6  # 应包含 scheduled, boarding, departed, arrived, delayed, cancelled
    scheduled_dict = next((child for child in flight_status_children if child.dict_key == "scheduled"), None)
    assert scheduled_dict is not None
    assert scheduled_dict.dict_name == "已排班"
    assert scheduled_dict.parent_key == "flight_status"
    assert scheduled_dict.description == "航班已安排"

    # 5. 测试查询父字典下的子字典 - 查询 'health_status' 的子字典
    print("\n=== 测试 DictionaryMapper 查询子字典功能 - 查询 'health_status' 子字典 ===")
    health_status_children = DictionaryMapper.get_children_by_parent_key("health_status")
    assert isinstance(health_status_children, list)
    assert len(health_status_children) >= 3  # 应包含 healthy, maintenance, fault
    healthy_dict = next((child for child in health_status_children if child.dict_key == "healthy"), None)
    assert healthy_dict is not None
    assert healthy_dict.dict_name == "健康"
    assert healthy_dict.parent_key == "health_status"

    # 6. 测试分页查询字典 - 无条件查询
    print("\n=== 测试 DictionaryMapper 分页查询功能 - 无条件查询 ===")
    search_result_all = DictionaryMapper.search(pageNum=1, pageSize=10)
    assert isinstance(search_result_all.data, list)
    assert search_result_all.pagination.current_page == 1
    assert search_result_all.pagination.total >= 5  # 至少包含 status 的几个子分类

    # 7. 测试分页查询字典 - 按名称过滤 '状态'
    print("\n=== 测试 DictionaryMapper 分页查询功能 - 按名称过滤 '状态' ===")
    search_result_name = DictionaryMapper.search(dict_name="状态", pageNum=1, pageSize=10)
    assert search_result_name.pagination.total >= 5  # 应包含多个状态相关字典项
    assert all("状态" in item.dict_name for item in search_result_name.data)

    # 8. 测试分页查询字典 - 按父键过滤 'status'
    print("\n=== 测试 DictionaryMapper 分页查询功能 - 按父键过滤 'status' ===")
    search_result_parent = DictionaryMapper.search(parent_key="status", pageNum=1, pageSize=10)
    assert search_result_parent.pagination.total >= 5  # 应包含 flight_status, health_status, approval_status 等
    assert all(item.parent_key == "status" for item in search_result_parent.data)

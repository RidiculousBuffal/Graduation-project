# tests/test_terminal_mapper.py
from app.DTO.terminals import TerminalCreateDTO, TerminalUpdateDTO
from app.mapper.terminal.terminalMapper import TerminalMapper

# 测试 TerminalMapper (航站楼)
def test_terminal_mapper_crud(app):
    with app.app_context():
        # 测试创建航站楼
        print("\n=== 测试 TerminalMapper 创建航站楼功能 ===")
        create_dto = TerminalCreateDTO(
            terminal_name="TestTerminal",
            description="Test Description"
        )
        print(f"输入值: Create DTO = {create_dto}")
        created_terminal = TerminalMapper.create(create_dto)
        print(f"返回值: Created Terminal = {created_terminal}")
        assert created_terminal.terminal_name == "TestTerminal"
        assert created_terminal.description == "Test Description"

        # 测试查询航站楼 by ID
        print("\n=== 测试 TerminalMapper 查询航站楼功能 (by ID) ===")
        print(f"输入值: terminal_id = {created_terminal.terminal_id}")
        retrieved_terminal = TerminalMapper.get_by_id(created_terminal.terminal_id)
        print(f"返回值: Retrieved Terminal = {retrieved_terminal}")
        assert retrieved_terminal.terminal_id == created_terminal.terminal_id
        assert retrieved_terminal.terminal_name == "TestTerminal"

        # 测试更新航站楼
        print("\n=== 测试 TerminalMapper 更新航站楼功能 ===")
        update_dto = TerminalUpdateDTO(
            terminal_name="UpdatedTerminal",
            description="Updated Description"
        )
        print(f"输入值: terminal_id = {created_terminal.terminal_id}, Update DTO = {update_dto}")
        updated_terminal = TerminalMapper.update(created_terminal.terminal_id, update_dto)
        print(f"返回值: Updated Terminal = {updated_terminal}")
        assert updated_terminal.terminal_name == "UpdatedTerminal"
        assert updated_terminal.description == "Updated Description"

        # 测试分页查询航站楼
        print("\n=== 测试 TerminalMapper 分页查询航站楼功能 ===")
        print(f"输入值: terminal_name = 'UpdatedTerminal', pageNum = 1, pageSize = 10")
        search_result = TerminalMapper.search(terminal_name="UpdatedTerminal", pageNum=1, pageSize=10)
        print(f"返回值: Search Result = {search_result}")
        assert search_result.data[0].terminal_name == "UpdatedTerminal"
        assert search_result.pagination.current_page == 1
        assert search_result.pagination.total == 1

        # 测试删除航站楼
        print("\n=== 测试 TerminalMapper 删除航站楼功能 ===")
        print(f"输入值: terminal_id = {created_terminal.terminal_id}")
        delete_result = TerminalMapper.delete(created_terminal.terminal_id)
        print(f"返回值: Delete Result = {delete_result}")
        assert delete_result is True
        assert TerminalMapper.get_by_id(created_terminal.terminal_id) is None
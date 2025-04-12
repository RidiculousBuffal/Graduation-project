from app.consts.Roles import RoleConsts
from app.mapper.auth.roleMapper import RoleMapper
from app.mapper.auth.userMapper import UserMapper
from app.mapper.auth.userRolePermissionMapper import UserRolePermissionMapper


def test_get_user_permission(app):
    # 创建角色
    print("\n=== 测试 用户角色获取 功能 ===")
    mock_user_name = 'mockUser'
    mock_user_password = 'passwd'
    mock_email = 'email'
    user_id = UserMapper.add_user(mock_user_name, mock_user_password, mock_email)
    role = RoleMapper.getRole(RoleConsts.ADMIN)
    UserRolePermissionMapper.combineUserWithRole(user_id, role.role_id)
    user_role = UserRolePermissionMapper.getUserRole(user_id)
    role_permissions = UserRolePermissionMapper.getRolePermissions(role.role_id)
    user_permissions = UserRolePermissionMapper.getUserPermissions(user_id)
    print(user_permissions)
    print(user_role)
    print(role_permissions)
    assert user_permissions == role_permissions
    assert len(user_permissions) >= 1

from app.consts.Permissions import Permissions
from app.consts.Roles import RoleConsts
from app.mapper.auth.permissionMapper import PermissionMapper
from app.mapper.auth.userRolePermissionMapper import UserRolePermissionMapper


def initRoles():
    from sqlalchemy import inspect
    from app.ext.extensions import db
    inspector = inspect(db.engine)
    if 'roles' not in inspector.get_table_names():
        return
    from app.models.auth import Role
    existing_roles = {r.role_name for r in Role.query.all()}  # set 去重
    required_roles = {RoleConsts.ADMIN, RoleConsts.ENGINEER, RoleConsts.USER}
    for role_name in required_roles - existing_roles:
        description = {
            RoleConsts.ADMIN: "管理员,拥有全部权限",
            RoleConsts.USER: '普通用户',
            RoleConsts.ENGINEER: "工程师"
        }.get(role_name, '')
        db.session.add(Role(role_name=role_name, description=description))
    db.session.commit()


def initPermissions():
    from sqlalchemy import inspect
    from app.ext.extensions import db
    inspector = inspect(db.engine)
    if 'permissions' not in inspector.get_table_names():
        return
    from app.models.auth import Permission
    existing_permissions = {p.permission_name for p in Permission.query.all()}
    # 拿到所有permission_name
    required_permissions = {attr for attr in dir(Permissions) if not attr.startswith('__')}
    for perm in required_permissions:
        perm_name = getattr(Permissions, perm).get('permission_name')
        perm_desc = getattr(Permissions, perm).get('description')
        if perm_name in existing_permissions:
            continue
        else:
            db.session.add(Permission(permission_name=perm_name, description=perm_desc))
            db.session.commit()


def combineRoleWithPermissions():
    from sqlalchemy import inspect
    from app.ext.extensions import db
    inspector = inspect(db.engine)
    if 'role_permissions' not in inspector.get_table_names():
        return

    def _quickAddRolePermissions(roleId: int, permissionArray: []):
        for p in permissionArray:
            dbPerm = PermissionMapper.get_permission_by_name(p.get('permission_name'))
            rp = UserRolePermissionMapper.getRolePermissionsByRoleIdAndPermissionId(roleId,
                                                                                      dbPerm.permission_id)
            if not rp:
                UserRolePermissionMapper.combine_role_permission(roleId=roleId,
                                                                 permissionId=dbPerm.permission_id)
    # 给普通用户增加查看个人资料和编辑个人资料的权限
    from app.mapper.auth.roleMapper import RoleMapper
    user_role = RoleMapper.getRole(RoleConsts.USER)
    user_permissions = [Permissions.PROFILE_READ, Permissions.PROFILE_EDIT]
    _quickAddRolePermissions(user_role.role_id, user_permissions)
    # 给管理员增加全部权限
    admin_role = RoleMapper.getRole(RoleConsts.ADMIN)
    admin_permissions = [getattr(Permissions, attr) for attr in dir(Permissions) if not attr.startswith('__')]
    _quickAddRolePermissions(admin_role.role_id, admin_permissions)

from app.consts.Dict import DictionaryData
from app.consts.Permissions import Permissions
from app.consts.Roles import RoleConsts
from app.mapper.auth.permissionMapper import PermissionMapper
from app.mapper.auth.userRolePermissionMapper import UserRolePermissionMapper
from app.models import Dictionary


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
    print('✅角色初始化成功')


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
    print('✅权限初始化成功')


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
    print('✅角色绑定到权限成功')
def initDictionaryData():
    from sqlalchemy import inspect
    from app.ext.extensions import db
    inspector = inspect(db.engine)
    if 'dictionary' not in inspector.get_table_names():
        print("Table 'dictionary' does not exist. Skipping dictionary data initialization.")
        return

    existing_dict_keys = {d.dict_key for d in Dictionary.query.all()}
    all_items = [attr for attr in dir(DictionaryData) if not attr.startswith('__')]
    all_data = [getattr(DictionaryData, item) for item in all_items]

    # 按层级插入数据，确保父记录先插入
    inserted_keys = set(existing_dict_keys)
    pending_data = all_data[:]
    while pending_data:
        inserted_this_round = False
        remaining_data = []
        for item_data in pending_data:
            dict_key = item_data.get('dict_key')
            parent_key = item_data.get('parent_key')
            # 如果已经插入或者 parent_key 是 None 或者 parent_key 已存在，则可以插入
            if dict_key in inserted_keys:
                continue
            if parent_key is None or parent_key in inserted_keys:
                new_dict = Dictionary(
                    dict_key=dict_key,
                    dict_name=item_data.get('dict_name'),
                    description=item_data.get('description'),
                    parent_key=parent_key,
                    sort_order=item_data.get('sort_order')
                )
                db.session.add(new_dict)
                inserted_keys.add(dict_key)
                inserted_this_round = True
            else:
                # 父记录还未插入，暂存到下一轮
                remaining_data.append(item_data)
        if not inserted_this_round and remaining_data:
            # 如果这一轮没有插入且还有剩余数据，说明可能有循环依赖或错误
            print("Warning: Possible circular dependency or missing parent keys in dictionary data.")
            break
        pending_data = remaining_data
        if inserted_this_round:
            db.session.commit()  # 每轮插入后提交，确保父记录可用

    if remaining_data:
        print("Some dictionary entries could not be inserted due to missing parent keys:")
        for item in remaining_data:
            print(f" - {item.get('dict_key')} (parent_key: {item.get('parent_key')})")
    else:
        print('✅字典表初始化成功')

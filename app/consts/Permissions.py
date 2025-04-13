class Permissions:
    USER_ADD = {
        "permission_name": "USER.ADD",
        "description": "增加用户"
    }
    USER_READ = {
        "permission_name": "USER.READ",
        "description": "查看用户"
    }
    USER_DELETE = {
        "permission_name": "USER.DELETE",
        "description": "删除用户"
    }
    USER_UPDATE = {
        "permission_name": "USER.UPDATE",
        "description": "更新用户信息"
    }
    PROFILE_READ = {
        "permission_name": "PROFILE.READ",
        "description": "查看个人资料"
    }
    PROFILE_EDIT = {
        "permission_name": "PROFILE.EDIT",
        "description": "编辑个人资料"
    }
    # 飞机相关
    AIRCRAFT_READ = {
        "permission_name": "AIRCRAFT.READ",
        "description": "查看飞机信息"
    }
    AIRCRAFT_DELETE = {
        "permission_name": "AIRCRAFT.DELETE",
        "description": "删除飞机信息"
    }
    AIRCRAFT_ADD = {
        "permission_name": "AIRCRAFT.ADD",
        "description": "添加飞机信息"
    }
    AIRCRAFT_UPDATE = {
        "permission_name": "AIRCRAFT.UPDATE",
        "description": "更新飞机信息"
    }
    AIRCRAFT_TYPE_ADD = {
        "permission_name": "AIRCRAFT.TYPE.ADD",
        "description": "添加飞机类型"
    }
    AIRCRAFT_TYPE_READ = {
        "permission_name": "AIRCRAFT.TYPE.READ",
        "description": "查看飞机类型"
    }
    AIRCRAFT_TYPE_DELETE = {
        "permission_name": "AIRCRAFT.TYPE.DELETE",
        "description": "删除飞机类型"
    }
    AIRCRAFT_TYPE_UPDATE = {
        "permission_name": "AIRCRAFT.TYPE.UPDATE",
        "description": "更新飞机类型"
    }

    FILE_UPLOAD = {
        "permission_name":"IPFS.FILE.UPLOAD",
        "description":"上传文件到IPFS"
    }

if __name__ == '__main__':
    # 获取所有权限字典
    required_permissions = [getattr(Permissions,attr) for attr in dir(Permissions) if not attr.startswith('__')]
    print(required_permissions)
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
        "permission_name": "IPFS.FILE.UPLOAD",
        "description": "上传文件到IPFS"
    }
    AIRCRAFT_IMAGE_ADD = {
        "permission_name": "AIRCRAFT.IMAGE.ADD",
        "description": "添加飞机参考图片权限"
    }
    AIRCRAFT_IMAGE_READ = {
        "permission_name": "AIRCRAFT.IMAGE.READ",
        "description": "读取飞机参考图片权限"
    }
    AIRCRAFT_IMAGE_UPDATE = {
        "permission_name": "AIRCRAFT.IMAGE.UPDATE",
        "description": "更新飞机参考图片权限"
    }
    AIRCRAFT_IMAGE_DELETE = {
        "permission_name": "AIRCRAFT.IMAGE.DELETE",
        "description": "删除飞机参考图片权限"
    }

    TERMINAL_ADD = {
        "permission_name": "TERMINAL.ADD",
        "description": "添加航站楼信息"
    }
    TERMINAL_READ = {
        "permission_name": "TERMINAL.READ",
        "description": "查看航站楼信息"
    }
    TERMINAL_UPDATE = {
        "permission_name": "TERMINAL.UPDATE",
        "description": "更新航站楼信息"
    }
    TERMINAL_DELETE = {
        "permission_name": "TERMINAL.DELETE",
        "description": "删除航站楼信息"
    }
    FLIGHT_ADD = {
        "permission_name": "FLIGHT.ADD",
        "description": "添加航班信息"
    }
    FLIGHT_READ = {
        "permission_name": "FLIGHT.READ",
        "description": "查看航班信息"
    }
    FLIGHT_UPDATE = {
        "permission_name": "FLIGHT.UPDATE",
        "description": "更新航班信息"
    }
    FLIGHT_DELETE = {
        "permission_name": "FLIGHT.DELETE",
        "description": "删除航班信息"
    }

if __name__ == '__main__':
    # 获取所有权限字典
    required_permissions = [getattr(Permissions, attr) for attr in dir(Permissions) if not attr.startswith('__')]
    print(required_permissions)

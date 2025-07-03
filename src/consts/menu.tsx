import {type MenuProps} from "antd";
import type {permissionType} from "../store/user/types.ts";
import {DashboardOutlined} from "@ant-design/icons";
import {Bug, Cable, Plane, Settings, Terminal, TerminalIcon, TicketsPlane, User, WarehouseIcon} from "lucide-react";
import {Permissions} from "./permissions.ts";


type MenuItem = Required<MenuProps>['items'][number];

type M = {
    key: string,
    label: string,
    icon?: React.ReactNode | null,
    permission: Omit<permissionType[number], 'permission_id'> | null,
    children?: M[],
}

export class MyMenu {
    private static menu: M[] = [{
        key: "dashboard",
        label: "仪表盘",
        icon: <DashboardOutlined/>,
        permission: null
    }, {
        key: "aircraft",
        label: "飞机管理",
        icon: <Plane/>,
        permission: null,
        children: [
            {key: "list", label: "飞机列表", permission: Permissions.AIRCRAFT_READ},
            {key: "type", label: "类型管理", permission: Permissions.AIRCRAFT_TYPE_READ},
            {key: "image", label: "底图管理", permission: Permissions.AIRCRAFT_IMAGE_READ},
        ]
    }, {
        key: "terminal",
        label: "航站楼管理",
        icon: <WarehouseIcon/>,
        permission: Permissions.TERMINAL_READ,
    }, {
        key: "flight",
        label: "航班管理",
        icon: <TicketsPlane/>,
        permission: Permissions.FLIGHT_READ,
    }, {
        key: "tasks",
        label: "任务编排",
        icon: <Cable/>,
        permission: Permissions.TASK_READ,
    }, {
        key: "inspection",
        label: "检测中心",
        icon: <Bug/>,
        permission: null,
        children: [
            {
                key: "hall",
                label: "检测列表",
                permission: Permissions.INSPECTION_READ
            }
        ]
    }, {
        key: "user",
        label: "用户设置",
        icon: <User/>,
        permission: null,
        children: [{
            key: "my",
            label: "个人信息修改",
            permission: Permissions.PROFILE_READ,
        }, {
            key: "security",
            label: "账户安全",
            permission: Permissions.PROFILE_READ
        }],
    }, {
        key: "admin",
        label: "系统管理",
        icon: <Settings/>,
        permission: null,
        children: [{
            key: "userlist",
            label: "用户管理",
            permission: Permissions.USER_READ_ALL
        }, {
            key: "rolePermission",
            label: "角色/权限管理",
            permission: Permissions.PERMISSIONS_MANAGEMENT
        }, {
            key: "log",
            label: "系统日志",
            permission: Permissions.LOG_READ
        }]
    }]


    public static getMenu(user_permissions: permissionType): M[] {
        const res: M[] = []
        for (const m of this.menu) {
            if (m.permission === null) {
                if (m.children) {
                    const children: M[] = []
                    for (const child of m.children) {
                        if (child.permission) {
                            const hasPermission = user_permissions.some(p => p.permission_name === child.permission?.permission_name)
                            if (hasPermission) {
                                children.push(child)
                            }
                        }
                    }
                    if (children.length > 0) {
                        res.push({...m, children})
                    }
                } else {
                    res.push(m)
                }
            } else {
                const hasPermission = user_permissions.some(p => p.permission_name === m.permission?.permission_name)
                if (hasPermission) {
                    res.push(m)
                }
            }
        }
        return res
    }
}
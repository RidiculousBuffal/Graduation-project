import React from 'react';
import {Table, Button, Tag, Space, Tooltip, type TableProps} from 'antd';
import {EyeOutlined, EditOutlined, KeyOutlined, ReloadOutlined} from '@ant-design/icons';
import type {AdminUserDTOWithRolesAndPermissions} from '@/store/admin/types';
import type {Pagination} from '@/publicTypes/pagination';
import {useUserStore} from "@/store/user/userStore.ts";

interface UserTableProps {
    users: AdminUserDTOWithRolesAndPermissions[];
    pagination: Pagination;
    loading: boolean;
    onViewDetail: (user: AdminUserDTOWithRolesAndPermissions) => void;
    onEditUser: (user: AdminUserDTOWithRolesAndPermissions) => void;
    onChangePassword: (user: AdminUserDTOWithRolesAndPermissions) => void;
    onPageChange: (page: number, pageSize: number) => void;
    onRefresh: () => void;
}

const UserTable: React.FC<UserTableProps> = ({
                                                 users,
                                                 pagination,
                                                 loading,
                                                 onViewDetail,
                                                 onEditUser,
                                                 onChangePassword,
                                                 onPageChange,
                                                 onRefresh,
                                             }) => {
    const columns: TableProps<AdminUserDTOWithRolesAndPermissions>['columns'] = [
        {
            title: '用户ID',
            dataIndex: 'user_id',
            key: 'user_id',
            width: 120,
        },
        {
            title: '用户名',
            dataIndex: 'username',
            key: 'username',
            width: 120,
        },
        {
            title: '姓名',
            dataIndex: 'name',
            key: 'name',
            width: 100,
        },
        {
            title: '邮箱',
            dataIndex: 'email',
            key: 'email',
            width: 180,
        },
        {
            title: '部门',
            dataIndex: 'department',
            key: 'department',
            width: 120,
        },
        {
            title: '状态',
            dataIndex: 'status',
            key: 'status',
            width: 80,
            render: (status: boolean) => (
                <Tag color={status ? 'green' : 'red'}>
                    {status ? '正常' : '禁用'}
                </Tag>
            ),
        },
        {
            title: '最后登录',
            dataIndex: 'last_login',
            key: 'last_login',
            width: 160,
            render: (date: Date) => date ? new Date(date).toLocaleString() : '-',
        },
        {
            title: '创建时间',
            dataIndex: 'created_at',
            key: 'created_at',
            width: 160,
            render: (date: Date) => date ? new Date(date).toLocaleString() : '-',
        },
        {
            title: '操作',
            key: 'actions',
            width: 200,
            fixed: 'right' as const,
            render: (_: any, record: AdminUserDTOWithRolesAndPermissions) => (
                <Space size="small">
                    <Tooltip title="查看详情">
                        <Button
                            type="text"
                            size="small"
                            icon={<EyeOutlined/>}
                            onClick={() => onViewDetail(record)}
                        />
                    </Tooltip>
                    <Tooltip title="编辑用户">
                        <Button
                            disabled={record.user_id == useUserStore.getState().user.user_id}
                            type="text"
                            size="small"
                            icon={<EditOutlined/>}
                            onClick={() => onEditUser(record)}
                        />
                    </Tooltip>
                    <Tooltip title="修改密码">
                        <Button
                            type="text"
                            size="small"
                            icon={<ReloadOutlined/>}
                            onClick={() => onChangePassword(record)}
                        />
                    </Tooltip>
                </Space>
            ),
        },
    ];

    return (
        <div className="user-table">
            <div className="table-header">
                <h3>用户列表</h3>
                <Button
                    type="text"
                    icon={<ReloadOutlined/>}
                    onClick={onRefresh}
                    loading={loading}
                >
                    刷新
                </Button>
            </div>

            <Table
                columns={columns}
                dataSource={users}
                rowKey="user_id"
                loading={loading}
                scroll={{x: 1200}}
                pagination={{
                    current: pagination.current_page,
                    pageSize: pagination.page_size,
                    total: pagination.total,
                    showSizeChanger: true,
                    showQuickJumper: true,
                    showTotal: (total, range) =>
                        `第 ${range[0]}-${range[1]} 条/共 ${total} 条`,
                    onChange: onPageChange,
                    onShowSizeChange: onPageChange,
                }}
            />
        </div>
    );
};

export default UserTable;
import React, {useEffect, useState} from 'react';
import {Card, Button} from 'antd';
import {PlusOutlined} from '@ant-design/icons';
import {useAdminStore} from '@/store/admin/adminStore';
import {AdminService} from '@/services/AdminService';
import UserSearchForm from './UserSearchForm';
import UserTable from './UserTable';
import UserDetailModal from './UserDetailModal';
import EditUserModal from './EditUserModal';
import ChangePasswordModal from './ChangePasswordModal';
import CreateUserModal from './CreateUserModal';
import type {AdminUserDTOWithRolesAndPermissions} from '@/store/admin/types';
import './UserManagement.css';

const UserManagement: React.FC = () => {
    const {users, usersPagination} = useAdminStore();
    const [selectedUser, setSelectedUser] = useState<AdminUserDTOWithRolesAndPermissions | null>(null);
    const [detailModalVisible, setDetailModalVisible] = useState(false);
    const [editModalVisible, setEditModalVisible] = useState(false);
    const [passwordModalVisible, setPasswordModalVisible] = useState(false);
    const [createModalVisible, setCreateModalVisible] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadUsers();
    }, []);

    const loadUsers = async (searchParams = {}) => {
        setLoading(true);
        try {
            await AdminService.getUsersList(searchParams);
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = (values: any) => {
        loadUsers(values);
    };

    const handleViewDetail = (user: AdminUserDTOWithRolesAndPermissions) => {
        setSelectedUser(user);
        setDetailModalVisible(true);
    };

    const handleEditUser = (user: AdminUserDTOWithRolesAndPermissions) => {
        setSelectedUser(user);
        setEditModalVisible(true);
    };

    const handleChangePassword = (user: AdminUserDTOWithRolesAndPermissions) => {
        setSelectedUser(user);
        setPasswordModalVisible(true);
    };

    const handleCreateUser = () => {
        setCreateModalVisible(true);
    };

    const handlePageChange = (page: number, pageSize: number) => {
        useAdminStore.getState().setUsersPagination({
            ...usersPagination,
            current_page: page,
            page_size: pageSize,
        });
        loadUsers();
    };

    return (
        <div className="user-management">
            <Card>
                <div className="user-management-header">
                    <UserSearchForm onSearch={handleSearch}/>
                    <Button
                        type="primary"
                        icon={<PlusOutlined/>}
                        onClick={handleCreateUser}
                    >
                        新增用户
                    </Button>
                </div>

                <UserTable
                    users={users}
                    pagination={usersPagination}
                    loading={loading}
                    onViewDetail={handleViewDetail}
                    onEditUser={handleEditUser}
                    onChangePassword={handleChangePassword}
                    onPageChange={handlePageChange}
                    onRefresh={() => loadUsers()}
                />
            </Card>

            <UserDetailModal
                visible={detailModalVisible}
                user={selectedUser}
                onClose={() => setDetailModalVisible(false)}
            />

            <EditUserModal
                visible={editModalVisible}
                user={selectedUser}
                onClose={() => setEditModalVisible(false)}
                onSuccess={() => {
                    setEditModalVisible(false);
                    loadUsers();
                }}
            />

            <ChangePasswordModal
                visible={passwordModalVisible}
                user={selectedUser}
                onClose={() => setPasswordModalVisible(false)}
                onSuccess={() => {
                    setPasswordModalVisible(false);
                    loadUsers();
                }}
            />

            <CreateUserModal
                visible={createModalVisible}
                onClose={() => setCreateModalVisible(false)}
                onSuccess={() => {
                    setCreateModalVisible(false);
                    loadUsers();
                }}
            />
        </div>
    );
};

export default UserManagement;
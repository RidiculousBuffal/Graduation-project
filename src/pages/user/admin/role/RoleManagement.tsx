import React, {useCallback, useEffect, useState} from 'react';
import {Card, Button, List, Tag, Space, Modal} from 'antd';
import {PlusOutlined, EditOutlined, DeleteOutlined, EyeOutlined} from '@ant-design/icons';
import {useAdminStore} from '@/store/admin/adminStore';
import {AdminService} from '@/services/AdminService';
import RolePermissionModal from './RolePermissionModal';
import EditRolePermissionModal from './EditRolePermissionModal';
import CreateRoleModal from './CreateRoleModal';
import type {RolePermission} from '@/store/admin/types';
import './RoleManagement.css';

const RoleManagement: React.FC = () => {
    const {roles} = useAdminStore();
    const [selectedRole, setSelectedRole] = useState<RolePermission | null>(null);
    const [permissionModalVisible, setPermissionModalVisible] = useState(false);
    const [editModalVisible, setEditModalVisible] = useState(false);
    const [createModalVisible, setCreateModalVisible] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadRoles();
    }, []);

    const loadRoles = async () => {
        setLoading(true);
        try {
            await AdminService.getRolesPermsList();
        } finally {
            setLoading(false);
        }
    };

    const handleViewPermissions = useCallback((role: RolePermission) => {
        setSelectedRole(role);
        setPermissionModalVisible(true);
    }, [])

    const handleEditPermissions = useCallback((role: RolePermission) => {
        setSelectedRole(role);
        setEditModalVisible(true);
    }, [])

    const handleDeleteRole = useCallback((role: RolePermission) => {
        Modal.confirm({
            title: '确认删除',
            content: `确定要删除角色 "${role.role.role_name}" 吗？`,
            onOk: async () => {
                try {
                    await AdminService.deleteRole(role.role.role_id);
                    loadRoles();
                } catch (error) {
                    console.error('删除角色失败:', error);
                }
            },
        });
    }, [])

    const handleCreateRole = useCallback(() => {
        setCreateModalVisible(true);
    }, [])

    return (
        <div className="role-management">
            <Card>
                <div className="role-management-header">
                    <h3>角色列表</h3>
                    <Button
                        type="primary"
                        icon={<PlusOutlined/>}
                        onClick={handleCreateRole}
                    >
                        添加角色
                    </Button>
                </div>

                <List
                    loading={loading}
                    dataSource={roles}
                    renderItem={(item) => (
                        <List.Item
                            actions={[
                                <Button
                                    type="text"
                                    icon={<EyeOutlined/>}
                                    onClick={() => handleViewPermissions(item)}
                                >
                                    查看权限
                                </Button>,
                                <Button
                                    type="text"
                                    icon={<EditOutlined/>}
                                    onClick={() => handleEditPermissions(item)}
                                    disabled={item.role.role_name == 'ADMIN'}
                                >
                                    编辑权限
                                </Button>,
                                <Button
                                    type="text"
                                    danger
                                    icon={<DeleteOutlined/>}
                                    onClick={() => handleDeleteRole(item)}
                                    disabled={item.role.role_name == 'ADMIN'}
                                >
                                    删除
                                </Button>,
                            ]}
                        >
                            <List.Item.Meta
                                title={
                                    <Space>
                                        <span>{item.role.role_name}</span>
                                        <Tag color="blue">{item.permissions.length} 个权限</Tag>
                                    </Space>
                                }
                                description={item.role.description}
                            />
                        </List.Item>
                    )}
                />
            </Card>

            <RolePermissionModal
                visible={permissionModalVisible}
                role={selectedRole}
                onClose={() => setPermissionModalVisible(false)}
            />

            <EditRolePermissionModal
                visible={editModalVisible}
                role={selectedRole}
                onClose={() => setEditModalVisible(false)}
                onSuccess={() => {
                    setEditModalVisible(false);
                    loadRoles();
                }}
            />

            <CreateRoleModal
                visible={createModalVisible}
                onClose={() => setCreateModalVisible(false)}
                onSuccess={() => {
                    setCreateModalVisible(false);
                    loadRoles();
                }}
            />
        </div>
    );
};

export default RoleManagement;
import React, {memo, useCallback, useEffect, useState} from 'react';
import {Modal, Checkbox, message, Row, Col} from 'antd';
import {AdminService} from '@/services/AdminService';
import type {RolePermission, Permission} from '@/store/admin/types';

interface EditRolePermissionModalProps {
    visible: boolean;
    role: RolePermission | null;
    onClose: () => void;
    onSuccess: () => void;
}

const EditRolePermissionModal: React.FC<EditRolePermissionModalProps> = ({
                                                                             visible,
                                                                             role,
                                                                             onClose,
                                                                             onSuccess,
                                                                         }) => {
    const [loading, setLoading] = useState(false);
    const [allPermissions, setAllPermissions] = useState<Permission[]>([]);
    const [selectedPermissions, setSelectedPermissions] = useState<number[]>([]);

    useEffect(() => {
        if (visible && role) {
            loadAllPermissions();
            setSelectedPermissions(role.permissions.map(p => p.permission_id));
        }
    }, [visible, role]);

    const loadAllPermissions = async () => {
        try {
            const permissions = await AdminService.getPermissionList();
            if (permissions) {
                setAllPermissions(permissions);
            }
        } catch (error) {
            console.error('获取权限列表失败:', error);
        }
    };

    const handleSubmit = async () => {
        if (!role) return;

        try {
            setLoading(true);
            await AdminService.updateRolePerm({
                roleId: role.role.role_id.toString(),
                permIds: selectedPermissions,
            });
            message.success('权限更新成功');
            onSuccess();
        } catch (error) {
            console.error('更新权限失败:', error);
        } finally {
            setLoading(false);
        }
    };

    const handlePermissionChange = useCallback((permissionIds: number[]) => {
        setSelectedPermissions(permissionIds);
    }, [])

    if (!role) return null;

    return (
        <Modal
            title={`编辑权限 - ${role.role.role_name}`}
            open={visible}
            onCancel={onClose}
            onOk={handleSubmit}
            confirmLoading={loading}
            width={800}
        >
            <div style={{marginBottom: 16}}>
                <p><strong>角色：</strong>{role.role.role_name}</p>
                <p><strong>描述：</strong>{role.role.description}</p>
            </div>

            <Checkbox.Group
                value={selectedPermissions}
                onChange={handlePermissionChange}
                style={{width: '100%'}}
            >
                <Row gutter={[16, 16]}>
                    {allPermissions.map((permission) => (
                        <Col span={8} key={permission.permission_id}>
                            <Checkbox value={permission.permission_id}>
                                <div>
                                    <div style={{fontWeight: 'bold'}}>
                                        {permission.permission_name}
                                    </div>
                                    <div style={{fontSize: '12px', color: '#666'}}>
                                        {permission.description}
                                    </div>
                                </div>
                            </Checkbox>
                        </Col>
                    ))}
                </Row>
            </Checkbox.Group>
        </Modal>
    );
};

export default memo(EditRolePermissionModal);
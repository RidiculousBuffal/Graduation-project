import React from 'react';
import {Modal, List, Tag} from 'antd';
import type {RolePermission} from '@/store/admin/types';
import {memo} from 'react'

interface RolePermissionModalProps {
    visible: boolean;
    role: RolePermission | null;
    onClose: () => void;
}

const RolePermissionModal: React.FC<RolePermissionModalProps> = ({
                                                                     visible,
                                                                     role,
                                                                     onClose,
                                                                 }) => {
    if (!role) return null;

    return (
        <Modal
            title={`角色权限 - ${role.role.role_name}`}
            open={visible}
            onCancel={onClose}
            footer={null}
            width={600}
        >
            <div style={{marginBottom: 16}}>
                <p><strong>角色描述：</strong>{role.role.description}</p>
                <p><strong>权限数量：</strong><Tag color="blue">{role.permissions.length} 个</Tag></p>
            </div>

            <List
                header={<div>权限列表</div>}
                bordered
                dataSource={role.permissions}
                renderItem={(permission) => (
                    <List.Item>
                        <List.Item.Meta
                            title={permission.permission_name}
                            description={permission.description}
                        />
                    </List.Item>
                )}
            />
        </Modal>
    );
};

export default memo(RolePermissionModal);
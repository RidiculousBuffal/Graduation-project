
import React from 'react';
import { Modal, Descriptions, Tag } from 'antd';
import type { AdminUserDTO } from '@/store/admin/types';

interface UserDetailModalProps {
    visible: boolean;
    user: AdminUserDTO | null;
    onClose: () => void;
}

const UserDetailModal: React.FC<UserDetailModalProps> = ({
                                                             visible,
                                                             user,
                                                             onClose,
                                                         }) => {
    if (!user) return null;

    return (
        <Modal
            title="用户详情"
            open={visible}
            onCancel={onClose}
            footer={null}
            width={800}
        >
            <Descriptions bordered column={2}>
                <Descriptions.Item label="用户ID">{user.user_id}</Descriptions.Item>
                <Descriptions.Item label="用户名">{user.username}</Descriptions.Item>
                <Descriptions.Item label="姓名">{user.name || '-'}</Descriptions.Item>
                <Descriptions.Item label="性别">{user.gender || '-'}</Descriptions.Item>
                <Descriptions.Item label="邮箱">{user.email || '-'}</Descriptions.Item>
                <Descriptions.Item label="手机号">{user.phone || '-'}</Descriptions.Item>
                <Descriptions.Item label="部门">{user.department || '-'}</Descriptions.Item>
                <Descriptions.Item label="工作年限">{user.work_years || '-'}</Descriptions.Item>
                <Descriptions.Item label="联系方式" span={2}>
                    {user.contact_info || '-'}
                </Descriptions.Item>
                <Descriptions.Item label="状态">
                    <Tag color={user.status ? 'green' : 'red'}>
                        {user.status ? '正常' : '禁用'}
                    </Tag>
                </Descriptions.Item>
                <Descriptions.Item label="最后登录">
                    {user.last_login ? new Date(user.last_login).toLocaleString() : '-'}
                </Descriptions.Item>
                <Descriptions.Item label="创建时间">
                    {user.created_at ? new Date(user.created_at).toLocaleString() : '-'}
                </Descriptions.Item>
                <Descriptions.Item label="更新时间">
                    {user.updated_at ? new Date(user.updated_at).toLocaleString() : '-'}
                </Descriptions.Item>
            </Descriptions>
        </Modal>
    );
};

export default UserDetailModal;
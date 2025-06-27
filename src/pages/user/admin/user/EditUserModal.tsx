import React, {useEffect, useState, useMemo, useCallback} from 'react';
import {Modal, Form, Input, Select, Switch, message, Row, Col, InputNumber} from 'antd';
import {AdminService} from '@/services/AdminService';
import {updateUserStatus} from '@/api/adminapi';
import type {AdminUserDTOWithRolesAndPermissions, Role} from '@/store/admin/types';
import {useAdminStore} from '@/store/admin/adminStore';

interface EditUserModalProps {
    visible: boolean;
    user: AdminUserDTOWithRolesAndPermissions | null;
    onClose: () => void;
    onSuccess: () => void;
}

const EditUserModal: React.FC<EditUserModalProps> = ({
                                                         visible,
                                                         user,
                                                         onClose,
                                                         onSuccess,
                                                     }) => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const [rolesLoading, setRolesLoading] = useState(false);
    const {roles: rolePermissions} = useAdminStore();

    // 使用 useMemo 缓存角色选项，避免重复计算
    const roleOptions = useMemo(() => {
        return rolePermissions.map(rp => ({
            label: rp.role.role_name,
            value: rp.role.role_id,
        }));
    }, [rolePermissions]);

    // 表单初始化 - 每次模态框打开且用户数据存在时都要重新设置表单值
    useEffect(() => {
        if (visible && user) {
            // 获取用户当前角色的ID数组
            const userRoleIds = user.roles ? user.roles.map(role => role.role_id) : [];

            // 设置表单的所有字段值
            form.setFieldsValue({
                username: user.username,
                name: user.name || '',
                email: user.email || '',
                phone: user.phone || '',
                gender: user.gender || undefined,
                department: user.department || '',
                work_years: user.work_years || null,
                contact_info: user.contact_info || '',
                status: user.status || false,
                roleIds: userRoleIds,
            });
        }
    }, [visible, user, form]);

    // 只在模态框首次打开且角色数据为空时获取角色列表
    useEffect(() => {
        if (visible && rolePermissions.length === 0 && !rolesLoading) {
            setRolesLoading(true);
            AdminService.getRolesPermsList()
                .then(() => {
                    setRolesLoading(false);
                })
                .catch(() => {
                    setRolesLoading(false);
                });
        }
    }, [visible, rolePermissions.length, rolesLoading]);

    const handleSubmit = async () => {
        try {
            setLoading(true);
            const values = await form.validateFields();

            // 构建更新数据 - 确保包含所有字段
            const userInfo = {
                user_id: user?.user_id,
                username: values.username,
                name: values.name,
                email: values.email,
                phone: values.phone,
                gender: values.gender,
                department: values.department,
                work_years: values.work_years,
                contact_info: values.contact_info,
            };

            // 批量处理所有更新操作
            const updatePromises = [];

            // 更新用户基本信息
            updatePromises.push(AdminService.forceUpdateUserInfo(userInfo));

            // 更新用户状态（仅当状态发生变化时）
            if (values.status !== user?.status) {
                updatePromises.push(updateUserStatus({
                    userId: user!.user_id,
                    status: values.status,
                }));
            }

            // 更新用户角色（仅当角色发生变化时）
            const currentRoleIds = user?.roles?.map(role => role.role_id) || [];
            const newRoleIds = values.roleIds || [];

            if (JSON.stringify(currentRoleIds.sort()) !== JSON.stringify(newRoleIds.sort())) {
                updatePromises.push(AdminService.updateUserRole({
                    userId: user!.user_id,
                    roleIds: newRoleIds,
                }));
            }

            // 并发执行所有更新操作
            await Promise.all(updatePromises);

            message.success('用户信息更新成功');
            onSuccess();
        } catch (error) {
            console.error('更新用户信息失败:', error);
            message.error('更新用户信息失败');
        } finally {
            setLoading(false);
        }
    };

    // 模态框关闭时重置表单
    const handleClose = useCallback(() => {
        form.resetFields();
        onClose();
    }, [form, onClose]);

    return (
        <Modal
            title="编辑用户信息"
            open={visible}
            onCancel={handleClose}
            onOk={handleSubmit}
            confirmLoading={loading}
            width={800}
            destroyOnHidden={false} // 改为 false，避免销毁表单状态
        >
            <Form
                form={form}
                layout="vertical"
                autoComplete="off"
                preserve={true} // 改为 true，保留字段值
            >
                <Row gutter={16}>
                    <Col span={12}>
                        <Form.Item
                            label="用户名"
                            name="username"
                            rules={[{required: true, message: '请输入用户名'}]}
                        >
                            <Input disabled/>
                        </Form.Item>
                    </Col>
                    <Col span={12}>
                        <Form.Item
                            label="姓名"
                            name="name"
                        >
                            <Input placeholder="请输入姓名"/>
                        </Form.Item>
                    </Col>
                </Row>

                <Row gutter={16}>
                    <Col span={12}>
                        <Form.Item
                            label="邮箱"
                            name="email"
                            rules={[{type: 'email', message: '请输入有效的邮箱地址'}]}
                        >
                            <Input placeholder="请输入邮箱"/>
                        </Form.Item>
                    </Col>
                    <Col span={12}>
                        <Form.Item
                            label="手机号"
                            name="phone"
                        >
                            <Input placeholder="请输入手机号"/>
                        </Form.Item>
                    </Col>
                </Row>

                <Row gutter={16}>
                    <Col span={12}>
                        <Form.Item
                            label="性别"
                            name="gender"
                        >
                            <Select placeholder="请选择性别" allowClear>
                                <Select.Option value="男">男</Select.Option>
                                <Select.Option value="女">女</Select.Option>
                            </Select>
                        </Form.Item>
                    </Col>
                    <Col span={12}>
                        <Form.Item
                            label="部门"
                            name="department"
                        >
                            <Input placeholder="请输入部门"/>
                        </Form.Item>
                    </Col>
                </Row>

                <Row gutter={16}>
                    <Col span={12}>
                        <Form.Item
                            label="工作年限"
                            name="work_years"
                        >
                            <InputNumber placeholder="请输入工作年限"/>
                        </Form.Item>
                    </Col>
                    <Col span={12}>
                        <Form.Item
                            label="用户角色"
                            name="roleIds"
                        >
                            <Select
                                mode="multiple"
                                placeholder="请选择用户角色"
                                options={roleOptions}
                                loading={rolesLoading}
                                notFoundContent={rolesLoading ? '加载中...' : '暂无数据'}
                            />
                        </Form.Item>
                    </Col>
                </Row>

                <Form.Item
                    label="联系方式"
                    name="contact_info"
                >
                    <Input.TextArea rows={3} placeholder="请输入联系方式"/>
                </Form.Item>

                <Form.Item
                    label="用户状态"
                    name="status"
                    valuePropName="checked"
                >
                    <Switch
                        checkedChildren="启用"
                        unCheckedChildren="禁用"
                    />
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default EditUserModal;
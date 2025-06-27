import React, { useState } from 'react';
import { Modal, Form, Input, message } from 'antd';
import { AdminService } from '@/services/AdminService';
import type { AdminUserDTO } from '@/store/admin/types';

interface ChangePasswordModalProps {
    visible: boolean;
    user: AdminUserDTO | null;
    onClose: () => void;
    onSuccess: () => void;
}

const ChangePasswordModal: React.FC<ChangePasswordModalProps> = ({
                                                                     visible,
                                                                     user,
                                                                     onClose,
                                                                     onSuccess,
                                                                 }) => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        try {
            setLoading(true);
            const values = await form.validateFields();

            await AdminService.forceUpdateUserPassword({
                userId: user!.user_id,
                password: values.password,
            });

            message.success('密码修改成功');
            form.resetFields();
            onSuccess();
        } catch (error) {
            console.error('修改密码失败:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleCancel = () => {
        form.resetFields();
        onClose();
    };

    return (
        <Modal
            title={`修改密码 - ${user?.username}`}
            open={visible}
            onCancel={handleCancel}
            onOk={handleSubmit}
            confirmLoading={loading}
        >
            <Form
                form={form}
                layout="vertical"
                autoComplete="off"
            >
                <Form.Item
                    label="新密码"
                    name="password"
                    rules={[
                        { required: true, message: '请输入新密码' },
                        { min: 6, message: '密码长度至少6位' },
                    ]}
                >
                    <Input.Password placeholder="请输入新密码" />
                </Form.Item>

                <Form.Item
                    label="确认密码"
                    name="confirmPassword"
                    dependencies={['password']}
                    rules={[
                        { required: true, message: '请确认新密码' },
                        ({ getFieldValue }) => ({
                            validator(_, value) {
                                if (!value || getFieldValue('password') === value) {
                                    return Promise.resolve();
                                }
                                return Promise.reject(new Error('两次输入的密码不一致'));
                            },
                        }),
                    ]}
                >
                    <Input.Password placeholder="请再次输入新密码" />
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default ChangePasswordModal;
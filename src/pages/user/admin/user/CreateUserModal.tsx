
import React, {memo, useState } from 'react';
import { Modal, Form, Input, Select, message, Row, Col } from 'antd';
import { AuthService } from '@/services/AuthService';

interface CreateUserModalProps {
    visible: boolean;
    onClose: () => void;
    onSuccess: () => void;
}

const CreateUserModal: React.FC<CreateUserModalProps> = ({
                                                             visible,
                                                             onClose,
                                                             onSuccess,
                                                         }) => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        try {
            setLoading(true);
            const values = await form.validateFields();

            const success = await AuthService.register(
                values.username,
                values.password,
                values.email
            );

            if (success) {
                form.resetFields();
                onSuccess();
            }
        } catch (error) {
            console.error('创建用户失败:', error);
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
            title="新增用户"
            open={visible}
            onCancel={handleCancel}
            onOk={handleSubmit}
            confirmLoading={loading}
            width={600}
        >
            <Form
                form={form}
                layout="vertical"
                autoComplete="off"
            >
                <Row gutter={16}>
                    <Col span={12}>
                        <Form.Item
                            label="用户名"
                            name="username"
                            rules={[
                                { required: true, message: '请输入用户名' },
                                { min: 3, message: '用户名长度至少3位' },
                            ]}
                        >
                            <Input placeholder="请输入用户名" />
                        </Form.Item>
                    </Col>
                    <Col span={12}>
                        <Form.Item
                            label="邮箱"
                            name="email"
                            rules={[
                                { required: true, message: '请输入邮箱' },
                                { type: 'email', message: '请输入有效的邮箱地址' },
                            ]}
                        >
                            <Input placeholder="请输入邮箱" />
                        </Form.Item>
                    </Col>
                </Row>

                <Row gutter={16}>
                    <Col span={12}>
                        <Form.Item
                            label="密码"
                            name="password"
                            rules={[
                                { required: true, message: '请输入密码' },
                                { min: 6, message: '密码长度至少6位' },
                            ]}
                        >
                            <Input.Password placeholder="请输入密码" />
                        </Form.Item>
                    </Col>
                    <Col span={12}>
                        <Form.Item
                            label="确认密码"
                            name="confirmPassword"
                            dependencies={['password']}
                            rules={[
                                { required: true, message: '请确认密码' },
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
                            <Input.Password placeholder="请再次输入密码" />
                        </Form.Item>
                    </Col>
                </Row>
            </Form>
        </Modal>
    );
};

export default memo(CreateUserModal);
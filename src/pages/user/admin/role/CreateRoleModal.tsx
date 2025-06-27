import React, { useState } from 'react';
import { Modal, Form, Input, message } from 'antd';
import { AdminService } from '@/services/AdminService';

interface CreateRoleModalProps {
    visible: boolean;
    onClose: () => void;
    onSuccess: () => void;
}

const CreateRoleModal: React.FC<CreateRoleModalProps> = ({
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

            await AdminService.createRole({
                role_name: values.role_name,
                description: values.description,
            });

            message.success('角色创建成功');
            form.resetFields();
            onSuccess();
        } catch (error) {
            console.error('创建角色失败:', error);
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
            title="添加角色"
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
                    label="角色名称"
                    name="role_name"
                    rules={[
                        { required: true, message: '请输入角色名称' },
                        { min: 2, message: '角色名称长度至少2位' },
                    ]}
                >
                    <Input placeholder="请输入角色名称" />
                </Form.Item>

                <Form.Item
                    label="角色描述"
                    name="description"
                    rules={[{ required: true, message: '请输入角色描述' }]}
                >
                    <Input.TextArea
                        rows={4}
                        placeholder="请输入角色描述"
                    />
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default CreateRoleModal;
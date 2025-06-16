import React from 'react';
import { Modal, Form, Input, message } from 'antd';
import {AircraftTypeService} from "../../../services/AircraftTypeService.ts";


interface AircraftTypeCreateModalProps {
    visible: boolean;
    onCancel: () => void;
    onSuccess: () => void;
}

const AircraftTypeCreateModal: React.FC<AircraftTypeCreateModalProps> = ({
                                                                             visible,
                                                                             onCancel,
                                                                             onSuccess
                                                                         }) => {
    const [form] = Form.useForm();
    const [loading, setLoading] = React.useState(false);

    const handleSubmit = async () => {
        try {
            const values = await form.validateFields();
            setLoading(true);

            await AircraftTypeService.createAircraftType({
                type_name: values.type_name,
                description: values.description || null
            });

            form.resetFields();
            onSuccess();
        } catch (error) {
            message.error('创建失败，请重试');
        } finally {
            setLoading(false);
        }
    };

    const handleCancel = () => {
        form.resetFields();
        onCancel();
    };

    return (
        <Modal
            title="新增飞机类型"
            open={visible}
            onOk={handleSubmit}
            onCancel={handleCancel}
            confirmLoading={loading}
            okText="创建"
            cancelText="取消"
            destroyOnHidden={true}
        >
            <Form
                form={form}
                layout="vertical"
                autoComplete="off"
            >
                <Form.Item
                    label="飞机类型名称"
                    name="type_name"
                    rules={[
                        { required: true, message: '请输入飞机类型名称' },
                        { min: 2, message: '飞机类型名称至少2个字符' },
                        { max: 50, message: '飞机类型名称不能超过50个字符' }
                    ]}
                >
                    <Input placeholder="请输入飞机类型名称" />
                </Form.Item>

                <Form.Item
                    label="描述"
                    name="description"
                    rules={[
                        { max: 1000, message: '描述不能超过1000个字符' }
                    ]}
                >
                    <Input.TextArea
                        rows={4}
                        placeholder="请输入飞机类型描述（支持Markdown格式）"
                    />
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default AircraftTypeCreateModal;
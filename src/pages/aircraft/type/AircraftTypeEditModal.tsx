import React, {useEffect} from 'react';
import {Modal, Form, Input, message} from 'antd';
import {AircraftTypeService} from "../../../services/AircraftTypeService.ts";
import type {aircraftTypeType} from "../../../store/aircraft/types.ts";


interface AircraftTypeEditModalProps {
    visible: boolean;
    aircraftType: aircraftTypeType | null;
    onCancel: () => void;
    onSuccess: () => void;
}

const AircraftTypeEditModal: React.FC<AircraftTypeEditModalProps> = ({
                                                                         visible,
                                                                         aircraftType,
                                                                         onCancel,
                                                                         onSuccess
                                                                     }) => {
    const [form] = Form.useForm();
    const [loading, setLoading] = React.useState(false);

    useEffect(() => {
        if (visible && aircraftType) {
            form.setFieldsValue({
                type_name: aircraftType.type_name,
                description: aircraftType.description || ''
            });
        }
    }, [visible, aircraftType, form]);

    const handleSubmit = async () => {
        if (!aircraftType) return;

        try {
            const values = await form.validateFields();
            setLoading(true);

            await AircraftTypeService.updateTerminal({
                typeid: aircraftType.typeid,
                type_name: values.type_name,
                description: values.description || null
            });
            onSuccess();
        } catch (error) {
            message.error('更新失败，请重试');
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
            title="编辑飞机类型"
            open={visible}
            onOk={handleSubmit}
            onCancel={handleCancel}
            confirmLoading={loading}
            okText="保存"
            cancelText="取消"
            destroyOnClose
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
                        {required: true, message: '请输入飞机类型名称'},
                        {min: 2, message: '飞机类型名称至少2个字符'},
                        {max: 50, message: '飞机类型名称不能超过50个字符'}
                    ]}
                >
                    <Input placeholder="请输入飞机类型名称"/>
                </Form.Item>

                <Form.Item
                    label="描述"
                    name="description"
                    rules={[
                        {max: 1000, message: '描述不能超过1000个字符'}
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

export default AircraftTypeEditModal;
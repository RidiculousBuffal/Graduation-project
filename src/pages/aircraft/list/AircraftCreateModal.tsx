import React, { useState, useEffect } from 'react';
import { Modal, Form, Input, Select, InputNumber, message } from 'antd';
import { AircraftListService } from '../../../services/AircraftListService';
import { AircraftTypeService } from '../../../services/AircraftTypeService';
import { useAircraftStore } from '../../../store/aircraft/aircraftStore';

const { Option } = Select;

interface AircraftCreateModalProps {
    visible: boolean;
    onCancel: () => void;
    onSuccess: () => void;
}

const AircraftCreateModal: React.FC<AircraftCreateModalProps> = ({
                                                                     visible,
                                                                     onCancel,
                                                                     onSuccess
                                                                 }) => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const [aircraftTypes, setAircraftTypes] = useState<any[]>([]);
    const [loadingTypes, setLoadingTypes] = useState(false);

    // 获取飞机类型列表
    const loadAircraftTypes = async () => {
        setLoadingTypes(true);
        try {
            await AircraftTypeService.getAircraftTypeList({ type_name: null, description: null });
            const { aircraftTypes } = useAircraftStore.getState();
            setAircraftTypes(aircraftTypes);
        } catch (error) {
            message.error('获取飞机类型失败');
        } finally {
            setLoadingTypes(false);
        }
    };

    useEffect(() => {
        if (visible) {
            loadAircraftTypes();
        }
    }, [visible]);

    const handleSubmit = async () => {
        try {
            const values = await form.validateFields();
            setLoading(true);

            await AircraftListService.createAircraft({
                aircraft_name: values.aircraft_name,
                age: values.age,
                typeid: values.typeid
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
            title="新增飞机"
            open={visible}
            onOk={handleSubmit}
            onCancel={handleCancel}
            confirmLoading={loading}
            okText="创建"
            cancelText="取消"
            destroyOnClose={true}
        >
            <Form
                form={form}
                layout="vertical"
                autoComplete="off"
            >
                <Form.Item
                    label="飞机名称"
                    name="aircraft_name"
                    rules={[
                        { required: true, message: '请输入飞机名称' },
                        { min: 2, message: '飞机名称至少2个字符' },
                        { max: 50, message: '飞机名称不能超过50个字符' }
                    ]}
                >
                    <Input placeholder="请输入飞机名称" />
                </Form.Item>

                <Form.Item
                    label="机龄"
                    name="age"
                    rules={[
                        { required: true, message: '请输入机龄' },
                        { type: 'number', min: 0, message: '机龄不能小于0' }
                    ]}
                >
                    <InputNumber
                        placeholder="请输入机龄"
                        min={0}
                        style={{ width: '100%' }}
                        addonAfter="年"
                    />
                </Form.Item>

                <Form.Item
                    label="飞机类型"
                    name="typeid"
                    rules={[
                        { required: true, message: '请选择飞机类型' }
                    ]}
                >
                    <Select
                        placeholder="请选择飞机类型"
                        loading={loadingTypes}
                    >
                        {aircraftTypes.map(type => (
                            <Option key={type.typeid} value={type.typeid}>
                                {type.type_name}
                            </Option>
                        ))}
                    </Select>
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default AircraftCreateModal;
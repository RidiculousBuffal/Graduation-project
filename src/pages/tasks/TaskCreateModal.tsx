import React, { useState } from 'react';
import { Modal, Form, DatePicker, message } from 'antd';
import { TaskService } from '@/services/TaskService';
import FlightSelector from '../../components/selectors/FlightSelector.tsx';
import type { autocompleteFlightIdResp } from '@/api/flightapi';


interface TaskCreateModalProps {
    visible: boolean;
    onCancel: () => void;
    onSuccess: () => void;
}

const TaskCreateModal: React.FC<TaskCreateModalProps> = ({
                                                             visible,
                                                             onCancel,
                                                             onSuccess
                                                         }) => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const [selectedFlight, setSelectedFlight] = useState<autocompleteFlightIdResp | null>(null);

    const handleSubmit = async () => {
        try {
            const values = await form.validateFields();
            setLoading(true);

            const payload = {
                flight_id: values.flight_id,
                estimated_start: values.estimated_start.toISOString(),
                estimated_end: values.estimated_end.toISOString(),
            };

            await TaskService.createTask(payload);
            message.success('创建任务成功');
            onSuccess();
            form.resetFields();
            setSelectedFlight(null);
        } catch (error) {
            message.error('创建任务失败');
        } finally {
            setLoading(false);
        }
    };

    const handleCancel = () => {
        form.resetFields();
        setSelectedFlight(null);
        onCancel();
    };

    const handleFlightChange = (flightId: string, flightInfo: autocompleteFlightIdResp) => {
        setSelectedFlight(flightInfo);
        form.setFieldsValue({ flight_id: flightId });
    };

    return (
        <Modal
            title="新建任务"
            open={visible}
            onOk={handleSubmit}
            onCancel={handleCancel}
            confirmLoading={loading}
            width={600}
            destroyOnClose
        >
            <Form
                form={form}
                layout="vertical"
                preserve={false}
            >
                <Form.Item
                    label="航班"
                    name="flight_id"
                    rules={[{ required: true, message: '请选择航班' }]}
                >
                    <FlightSelector
                        onChange={handleFlightChange}
                        placeholder="请输入航班ID或飞机名称搜索"
                    />
                </Form.Item>

                {selectedFlight && (
                    <div style={{
                        marginBottom: 16,
                        padding: 12,
                        backgroundColor: '#f6f6f6',
                        borderRadius: 4
                    }}>
                        <strong>选中航班信息：</strong><br />
                        航班ID: {selectedFlight.flight_id}<br />
                        飞机: {selectedFlight.aircraft_name}
                    </div>
                )}

                <Form.Item
                    label="预计开始时间"
                    name="estimated_start"
                    rules={[{ required: true, message: '请选择预计开始时间' }]}
                >
                    <DatePicker
                        showTime
                        style={{ width: '100%' }}
                        format="YYYY-MM-DD HH:mm:ss"
                        placeholder="请选择预计开始时间"
                    />
                </Form.Item>

                <Form.Item
                    label="预计结束时间"
                    name="estimated_end"
                    rules={[
                        { required: true, message: '请选择预计结束时间' },
                        ({ getFieldValue }) => ({
                            validator(_, value) {
                                const startTime = getFieldValue('estimated_start');
                                if (!value || !startTime || value.isAfter(startTime)) {
                                    return Promise.resolve();
                                }
                                return Promise.reject(new Error('结束时间必须晚于开始时间'));
                            },
                        }),
                    ]}
                >
                    <DatePicker
                        showTime
                        style={{ width: '100%' }}
                        format="YYYY-MM-DD HH:mm:ss"
                        placeholder="请选择预计结束时间"
                    />
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default TaskCreateModal;
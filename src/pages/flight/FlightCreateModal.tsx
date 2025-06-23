import React, {useState} from 'react';
import {Modal, Form, DatePicker, message} from 'antd';
import type {createFlightPayLoad} from '../../api/flightapi';
import {formatLocalDateToISO} from '../../utils/dateUtils';
import {FlightService} from "../../services/FlightService";
import {AircraftSelector, TerminalSelector} from './selectors';

interface FlightCreateModalProps {
    visible: boolean;
    onCancel: () => void;
    onSuccess: () => void;
}

export const FlightCreateModal: React.FC<FlightCreateModalProps> = ({
                                                                        visible,
                                                                        onCancel,
                                                                        onSuccess,
                                                                    }) => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        try {
            const values = await form.validateFields();
            setLoading(true);

            const payload: createFlightPayLoad = {
                aircraft_id: values.aircraft_id,
                terminal_id: values.terminal_id,
                estimated_departure: formatLocalDateToISO(values.estimated_departure),
                estimated_arrival: formatLocalDateToISO(values.estimated_arrival),
            };

            const success = await FlightService.createFlight(payload);
            if (success) {
                message.success('创建航班成功');
                form.resetFields();
                onSuccess();
            }
        } catch (error) {
            message.error('创建航班失败');
        } finally {
            setLoading(false);
        }
    };

    const handleCancel = () => {
        form.resetFields();
        onCancel();
    };

    const handleSearchError = (error: any) => {
        message.error('加载选项数据失败');
    };

    return (
        <Modal
            title="新增航班"
            open={visible}
            onOk={handleSubmit}
            onCancel={handleCancel}
            confirmLoading={loading}
            width={600}
            destroyOnHidden={true}
        >
            <Form
                form={form}
                layout="vertical"
                requiredMark={false}
            >
                <Form.Item
                    label="飞机"
                    name="aircraft_id"
                    rules={[{required: true, message: '请选择飞机'}]}
                >
                    <AircraftSelector
                        placeholder="请输入飞机名称搜索"
                        onSearchError={handleSearchError}
                    />
                </Form.Item>

                <Form.Item
                    label="航站楼"
                    name="terminal_id"
                >
                    <TerminalSelector
                        placeholder="请输入航站楼名称搜索（可选）"
                        allowClear
                        onSearchError={handleSearchError}
                    />
                </Form.Item>

                <Form.Item
                    label="预计起飞时间"
                    name="estimated_departure"
                    rules={[{required: true, message: '请选择预计起飞时间'}]}
                >
                    <DatePicker
                        showTime
                        placeholder="请选择预计起飞时间"
                        style={{width: '100%'}}
                        format="YYYY-MM-DD HH:mm:ss"
                    />
                </Form.Item>

                <Form.Item
                    label="预计到达时间"
                    name="estimated_arrival"
                    rules={[{required: true, message: '请选择预计到达时间'}]}
                >
                    <DatePicker
                        showTime
                        placeholder="请选择预计到达时间"
                        style={{width: '100%'}}
                        format="YYYY-MM-DD HH:mm:ss"
                    />
                </Form.Item>
            </Form>
        </Modal>
    );
};
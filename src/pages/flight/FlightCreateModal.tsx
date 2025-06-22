
import React, { useEffect, useState } from 'react';
import { Modal, Form, Select, DatePicker, message } from 'antd';

import { useAircraftStore } from '../../store/aircraft/aircraftStore';
import { useTerminalStore } from '../../store/terminal/terminalStore';
import type { createFlightPayLoad } from '../../api/flightapi';
import { formatLocalDateToISO } from '../../utils/dateUtils';
import {TerminalService} from "../../services/TerminalService.ts";
import {AircraftListService} from "../../services/AircraftListService.ts";
import {FlightService} from "../../services/FlightService.ts";

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
    const [loadingOptions, setLoadingOptions] = useState(false);

    const { aircrafts } = useAircraftStore();
    const { terminals } = useTerminalStore();

    // 加载飞机和航站楼选项
    useEffect(() => {
        if (visible) {
            loadOptions();
        }
    }, [visible]);

    const loadOptions = async () => {
        setLoadingOptions(true);
        try {
            // 并行加载飞机和航站楼数据
            await Promise.all([
                AircraftListService.getAircraftList({
                    aircraft_name: null,
                    age: null,
                    type_name: null,
                    description: null
                }),
                TerminalService.getTerminalList({
                    terminal_name: null,
                    description: null
                })
            ]);
        } catch (error) {
            console.error('加载选项失败:', error);
            message.error('加载选项数据失败');
        } finally {
            setLoadingOptions(false);
        }
    };

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
                    rules={[{ required: true, message: '请选择飞机' }]}
                >
                    <Select
                        placeholder="请选择飞机"
                        loading={loadingOptions}
                        showSearch
                        filterOption={(input, option) =>
                            (option?.label as string)?.toLowerCase().includes(input.toLowerCase())
                        }
                        options={aircrafts.map(aircraft => ({
                            value: aircraft.aircraft_id,
                            label: `${aircraft.aircraft_name} (${aircraft.type_name})`,
                            key: aircraft.aircraft_id
                        }))}
                    />
                </Form.Item>

                <Form.Item
                    label="航站楼"
                    name="terminal_id"
                >
                    <Select
                        placeholder="请选择航站楼（可选）"
                        allowClear
                        loading={loadingOptions}
                        showSearch
                        filterOption={(input, option) =>
                            (option?.label as string)?.toLowerCase().includes(input.toLowerCase())
                        }
                        options={terminals.map(terminal => ({
                            value: terminal.terminal_id,
                            label: terminal.terminal_name,
                            key: terminal.terminal_id
                        }))}
                    />
                </Form.Item>

                <Form.Item
                    label="预计起飞时间"
                    name="estimated_departure"
                    rules={[{ required: true, message: '请选择预计起飞时间' }]}
                >
                    <DatePicker
                        showTime
                        placeholder="请选择预计起飞时间"
                        style={{ width: '100%' }}
                        format="YYYY-MM-DD HH:mm:ss"
                    />
                </Form.Item>

                <Form.Item
                    label="预计到达时间"
                    name="estimated_arrival"
                    rules={[{ required: true, message: '请选择预计到达时间' }]}
                >
                    <DatePicker
                        showTime
                        placeholder="请选择预计到达时间"
                        style={{ width: '100%' }}
                        format="YYYY-MM-DD HH:mm:ss"
                    />
                </Form.Item>
            </Form>
        </Modal>
    );
};
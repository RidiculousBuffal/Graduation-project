import React, {useEffect, useState} from 'react';
import {Modal, Form, Select, DatePicker, message} from 'antd';
import {FlightService} from '../../services/FlightService';
import {DictionaryService} from '../../services/DictionaryService';
import {APPROVAL_STATUS, FLIGHT_STATUS, HEALTH_STATUS} from '../../consts/dictionary';
import type {flightListType, flightType} from '../../store/flight/types';
import type {dictionaryType} from '../../store/dictionary/type';
import {AircraftSelector, TerminalSelector} from './selectors';
import dayjs from 'dayjs';
import {formatUTCToLocal} from "../../utils/dateUtils";

interface FlightEditModalProps {
    visible: boolean;
    flight: flightListType | null;
    onCancel: () => void;
    onSuccess: () => void;
}

export const FlightEditModal: React.FC<FlightEditModalProps> = ({
                                                                    visible,
                                                                    flight,
                                                                    onCancel,
                                                                    onSuccess,
                                                                }) => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const [loadingOptions, setLoadingOptions] = useState(false);
    const [flightStatusOptions, setFlightStatusOptions] = useState<dictionaryType[]>([]);
    const [healthStatusOptions, setHealthStatusOptions] = useState<dictionaryType[]>([]);
    const [approvalStatusOptions, setApprovalStatusOptions] = useState<dictionaryType[]>([]);

    // 加载字典选项数据
    useEffect(() => {
        if (visible) {
            loadDictionaryOptions();
        }
    }, [visible]);

    // 设置表单初始值
    useEffect(() => {
        if (visible && flight) {
            form.setFieldsValue({
                aircraft_id: flight.aircraft_id,
                terminal_id: flight.terminal_id,
                flight_status: flight.flight_status,
                health_status: flight.health_status,
                approval_status: flight.approval_status,
                estimate_departure: flight.estimated_departure ? dayjs(formatUTCToLocal(flight.estimated_departure)) : null,
                estimate_arrival: flight.estimated_arrival ? dayjs(formatUTCToLocal(flight.estimated_arrival)) : null,
                actual_departure: flight.actual_departure ? dayjs(formatUTCToLocal(flight.actual_departure)) : null,
                actual_arrival: flight.actual_arrival ? dayjs(formatUTCToLocal(flight.actual_arrival)) : null,
            });
        }
    }, [visible, flight, form]);

    const loadDictionaryOptions = async () => {
        setLoadingOptions(true);
        try {
            const [flightStatus, healthStatus, approvalStatus] = await Promise.all([
                DictionaryService.getChildrenByParentId(FLIGHT_STATUS),
                DictionaryService.getChildrenByParentId(HEALTH_STATUS),
                DictionaryService.getChildrenByParentId(APPROVAL_STATUS),
            ]);

            setFlightStatusOptions(flightStatus || []);
            setHealthStatusOptions(healthStatus || []);
            setApprovalStatusOptions(approvalStatus || []);
        } catch (error) {
            console.error('加载字典选项数据失败:', error);
            message.error('加载字典选项数据失败');
        } finally {
            setLoadingOptions(false);
        }
    };

    const handleSubmit = async () => {
        if (!flight) return;

        try {
            const values = await form.validateFields();
            setLoading(true);

            const payload: flightType = {
                flight_id: flight.flight_id,
                aircraft_id: values.aircraft_id,
                flight_status: values.flight_status,
                health_status: values.health_status,
                approval_status: values.approval_status,
                estimated_departure: values.estimate_departure ? values.estimate_departure.toDate() : null,
                estimated_arrival: values.estimate_arrival ? values.estimate_arrival.toDate() : null,
                actual_departure: values.actual_departure ? values.actual_departure.toDate() : null,
                actual_arrival: values.actual_arrival ? values.actual_arrival.toDate() : null,
            };

            const success = await FlightService.updateFlight(payload);
            if (success) {
                message.success('更新航班成功');
                onSuccess();
            }
        } catch (error) {
            message.error('更新航班失败');
        } finally {
            setLoading(false);
        }
    };

    const handleCancel = () => {
        form.resetFields();
        onCancel();
    };

    const handleSearchError = (error: any) => {
        message.error('加载选项数据失败').then(r => r);
    };

    return (
        <Modal
            title="编辑航班"
            open={visible}
            onOk={handleSubmit}
            onCancel={handleCancel}
            confirmLoading={loading}
            width={700}
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
                    label="航班状态"
                    name="flight_status"
                >
                    <Select
                        placeholder="请选择航班状态"
                        allowClear
                        loading={loadingOptions}
                        options={flightStatusOptions.map(option => ({
                            value: option.dict_key,
                            label: option.dict_name,
                            key: option.dict_key
                        }))}
                    />
                </Form.Item>

                <Form.Item
                    label="健康状态"
                    name="health_status"
                >
                    <Select
                        placeholder="请选择健康状态"
                        allowClear
                        loading={loadingOptions}
                        options={healthStatusOptions.map(option => ({
                            value: option.dict_key,
                            label: option.dict_name,
                            key: option.dict_key
                        }))}
                    />
                </Form.Item>

                <Form.Item
                    label="审批状态"
                    name="approval_status"
                >
                    <Select
                        placeholder="请选择审批状态"
                        allowClear
                        loading={loadingOptions}
                        options={approvalStatusOptions.map(option => ({
                            value: option.dict_key,
                            label: option.dict_name,
                            key: option.dict_key
                        }))}
                    />
                </Form.Item>

                <Form.Item
                    label="预计起飞时间"
                    name="estimate_departure"
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
                    name="estimate_arrival"
                >
                    <DatePicker
                        showTime
                        placeholder="请选择预计到达时间"
                        style={{width: '100%'}}
                        format="YYYY-MM-DD HH:mm:ss"
                    />
                </Form.Item>

                <Form.Item
                    label="实际起飞时间"
                    name="actual_departure"
                >
                    <DatePicker
                        showTime
                        placeholder="请选择实际起飞时间"
                        style={{width: '100%'}}
                        format="YYYY-MM-DD HH:mm:ss"
                    />
                </Form.Item>

                <Form.Item
                    label="实际到达时间"
                    name="actual_arrival"
                >
                    <DatePicker
                        showTime
                        placeholder="请选择实际到达时间"
                        style={{width: '100%'}}
                        format="YYYY-MM-DD HH:mm:ss"
                    />
                </Form.Item>
            </Form>
        </Modal>
    );
};
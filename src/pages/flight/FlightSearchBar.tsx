import React, {useEffect, useState} from 'react';
import {Form, Input, Select, DatePicker, Button, Row, Col, Space} from 'antd';
import {SearchOutlined, ReloadOutlined} from '@ant-design/icons';
import type {SearchFlightPayload} from '../../api/flightapi';
import type {dictionaryType} from '../../store/dictionary/type';
import {formatLocalDateToISO} from '../../utils/dateUtils';
import './FlightSearchBar.css';
import {DictionaryService} from "../../services/DictionaryService.ts";
import {APPROVAL_STATUS, FLIGHT_STATUS, HEALTH_STATUS} from "../../consts/dictionary.ts";

const {RangePicker} = DatePicker;

interface FlightSearchBarProps {
    onSearch: (searchParams: SearchFlightPayload) => void;
}

export const FlightSearchBar: React.FC<FlightSearchBarProps> = ({onSearch}) => {
    const [form] = Form.useForm();
    const [flightStatusOptions, setFlightStatusOptions] = useState<dictionaryType[]>([]);
    const [healthStatusOptions, setHealthStatusOptions] = useState<dictionaryType[]>([]);
    const [approvalStatusOptions, setApprovalStatusOptions] = useState<dictionaryType[]>([]);

    // 加载字典数据
    useEffect(() => {
        const loadDictionaries = async () => {
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
                console.error('加载字典数据失败:', error);
            }
        };

        loadDictionaries();
    }, []);

    // 处理搜索
    const handleSearch = () => {
        const values = form.getFieldsValue();
        const searchParams: SearchFlightPayload = {
            flight_status: values.flight_status,
            health_status: values.health_status,
            approval_status: values.approval_status,
            aircraft_name: values.aircraft_name,
            terminal_name: values.terminal_name,
        };

        // 处理预计起飞时间范围
        if (values.estimated_departure_range) {
            searchParams.estimated_departure_start = formatLocalDateToISO(values.estimated_departure_range[0]);
            searchParams.estimated_departure_end = formatLocalDateToISO(values.estimated_departure_range[1]);
        }

        // 处理预计到达时间范围
        if (values.estimated_arrival_range) {
            searchParams.estimated_arrival_start = formatLocalDateToISO(values.estimated_arrival_range[0]);
            searchParams.estimated_arrival_end = formatLocalDateToISO(values.estimated_arrival_range[1]);
        }

        // 处理实际起飞时间范围
        if (values.actual_departure_range) {
            searchParams.actual_departure_start = formatLocalDateToISO(values.actual_departure_range[0]);
            searchParams.actual_departure_end = formatLocalDateToISO(values.actual_departure_range[1]);
        }

        // 处理实际到达时间范围
        if (values.actual_arrival_range) {
            searchParams.actual_arrival_start = formatLocalDateToISO(values.actual_arrival_range[0]);
            searchParams.actual_arrival_end = formatLocalDateToISO(values.actual_arrival_range[1]);
        }

        onSearch(searchParams);
    };

    // 重置搜索
    const handleReset = () => {
        form.resetFields();
        onSearch({});
    };

    return (
        <div className="flight-search-bar">
            <Form form={form} layout="vertical">
                <Row gutter={16}>
                    <Col span={6}>
                        <Form.Item label="飞机名称" name="aircraft_name">
                            <Input placeholder="请输入飞机名称"/>
                        </Form.Item>
                    </Col>
                    <Col span={6}>
                        <Form.Item label="航站楼" name="terminal_name">
                            <Input placeholder="请输入航站楼名称"/>
                        </Form.Item>
                    </Col>
                    <Col span={6}>
                        <Form.Item label="航班状态" name="flight_status">
                            <Select placeholder="请选择航班状态" allowClear>
                                {flightStatusOptions.map(option => (
                                    <Select.Option key={option.dict_key} value={option.dict_key}>
                                        {option.dict_name}
                                    </Select.Option>
                                ))}
                            </Select>
                        </Form.Item>
                    </Col>
                    <Col span={6}>
                        <Form.Item label="健康状态" name="health_status">
                            <Select placeholder="请选择健康状态" allowClear>
                                {healthStatusOptions.map(option => (
                                    <Select.Option key={option.dict_key} value={option.dict_key}>
                                        {option.dict_name}
                                    </Select.Option>
                                ))}
                            </Select>
                        </Form.Item>
                    </Col>
                </Row>

                <Row gutter={16}>
                    <Col span={6}>
                        <Form.Item label="审批状态" name="approval_status">
                            <Select placeholder="请选择审批状态" allowClear>
                                {approvalStatusOptions.map(option => (
                                    <Select.Option key={option.dict_key} value={option.dict_key}>
                                        {option.dict_name}
                                    </Select.Option>
                                ))}
                            </Select>
                        </Form.Item>
                    </Col>
                    <Col span={6}>
                        <Form.Item label="预计起飞时间" name="estimated_departure_range">
                            <RangePicker showTime placeholder={['开始时间', '结束时间']}/>
                        </Form.Item>
                    </Col>
                    <Col span={6}>
                        <Form.Item label="预计到达时间" name="estimated_arrival_range">
                            <RangePicker showTime placeholder={['开始时间', '结束时间']}/>
                        </Form.Item>
                    </Col>
                    <Col span={6}>
                        <Form.Item label="实际起飞时间" name="actual_departure_range">
                            <RangePicker showTime placeholder={['开始时间', '结束时间']}/>
                        </Form.Item>
                    </Col>
                </Row>

                <Row gutter={16}>
                    <Col span={6}>
                        <Form.Item label="实际到达时间" name="actual_arrival_range">
                            <RangePicker showTime placeholder={['开始时间', '结束时间']}/>
                        </Form.Item>
                    </Col>
                    <Col span={18}>
                        <Form.Item label=" ">
                            <Space>
                                <Button type="primary" icon={<SearchOutlined/>} onClick={handleSearch}>
                                    搜索
                                </Button>
                                <Button icon={<ReloadOutlined/>} onClick={handleReset}>
                                    重置
                                </Button>
                            </Space>
                        </Form.Item>
                    </Col>
                </Row>
            </Form>
        </div>
    );
};
import React, { useState } from 'react';
import { Form, Input, Button, Row, Col, Space, Select, InputNumber } from 'antd';
import { SearchOutlined, ReloadOutlined } from '@ant-design/icons';
import { useAircraftStore } from '../../../store/aircraft/aircraftStore';
import { AircraftTypeService } from '../../../services/AircraftTypeService';
import './AircraftSearchBar.css';

const { Option } = Select;

interface SearchParams {
    aircraft_name?: string;
    age?: number;
    type_name?: string;
}

interface AircraftSearchBarProps {
    onSearch: (params: SearchParams) => void;
    onReset: () => void;
    loading?: boolean;
}

const AircraftSearchBar: React.FC<AircraftSearchBarProps> = ({
                                                                 onSearch,
                                                                 onReset,
                                                                 loading = false
                                                             }) => {
    const [form] = Form.useForm();
    const [searchParams, setSearchParams] = useState<SearchParams>({});
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
            console.error('Failed to load aircraft types:', error);
        } finally {
            setLoadingTypes(false);
        }
    };

    const handleSearch = async () => {
        try {
            const values = await form.validateFields();
            const params: SearchParams = {
                aircraft_name: values.aircraft_name?.trim() || undefined,
                age: values.age || undefined,
                type_name: values.type_name || undefined
            };
            setSearchParams(params);
            onSearch(params);
        } catch (error) {
            // 表单验证失败
        }
    };

    const handleReset = () => {
        form.resetFields();
        setSearchParams({});
        onReset();
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    };

    return (
        <div className="aircraft-search-bar">
            <Form
                form={form}
                layout="vertical"
                autoComplete="off"
            >
                <Row gutter={[16, 16]} align="middle">
                    <Col xs={24} sm={12} md={6} lg={5}>
                        <Form.Item
                            label="飞机名称"
                            name="aircraft_name"
                            className="search-form-item"
                        >
                            <Input
                                placeholder="请输入飞机名称"
                                onKeyPress={handleKeyPress}
                                allowClear
                            />
                        </Form.Item>
                    </Col>

                    <Col xs={24} sm={12} md={6} lg={5}>
                        <Form.Item
                            label="机龄"
                            name="age"
                            className="search-form-item"
                        >
                            <InputNumber
                                placeholder="请输入机龄"
                                onKeyPress={handleKeyPress}
                                min={0}
                                style={{ width: '100%' }}
                            />
                        </Form.Item>
                    </Col>

                    <Col xs={24} sm={12} md={6} lg={6}>
                        <Form.Item
                            label="飞机类型"
                            name="type_name"
                            className="search-form-item"
                        >
                            <Select
                                placeholder="请选择飞机类型"
                                allowClear
                                onDropdownVisibleChange={(open) => {
                                    if (open && aircraftTypes.length === 0) {
                                        loadAircraftTypes();
                                    }
                                }}
                                loading={loadingTypes}
                            >
                                {aircraftTypes.map(type => (
                                    <Option key={type.typeid} value={type.type_name}>
                                        {type.type_name}
                                    </Option>
                                ))}
                            </Select>
                        </Form.Item>
                    </Col>

                    <Col xs={24} sm={24} md={6} lg={8}>
                        <div className="search-actions">
                            <Space>
                                <Button
                                    type="primary"
                                    icon={<SearchOutlined />}
                                    onClick={handleSearch}
                                    loading={loading}
                                >
                                    搜索
                                </Button>
                                <Button
                                    icon={<ReloadOutlined />}
                                    onClick={handleReset}
                                    disabled={loading}
                                >
                                    重置
                                </Button>
                            </Space>
                        </div>
                    </Col>
                </Row>
            </Form>
        </div>
    );
};

export default AircraftSearchBar;
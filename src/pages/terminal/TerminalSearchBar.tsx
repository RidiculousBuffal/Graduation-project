import React, { useState } from 'react';
import { Form, Input, Button, Row, Col, Space } from 'antd';
import { SearchOutlined, ReloadOutlined } from '@ant-design/icons';
import './TerminalSearchBar.css';

interface SearchParams {
    terminal_name?: string;
    description?: string;
}

interface TerminalSearchBarProps {
    onSearch: (params: SearchParams) => void;
    onReset: () => void;
    loading?: boolean;
}

const TerminalSearchBar: React.FC<TerminalSearchBarProps> = ({
                                                                 onSearch,
                                                                 onReset,
                                                                 loading = false
                                                             }) => {
    const [form] = Form.useForm();
    const [searchParams, setSearchParams] = useState<SearchParams>({});

    const handleSearch = async () => {
        try {
            const values = await form.validateFields();
            const params: SearchParams = {
                terminal_name: values.terminal_name?.trim() || undefined,
                description: values.description?.trim() || undefined
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
        <div className="terminal-search-bar">
            <Form
                form={form}
                layout="vertical"
                autoComplete="off"
            >
                <Row gutter={[16, 16]} align="middle">
                    <Col xs={24} sm={12} md={8} lg={6}>
                        <Form.Item
                            label="航站楼名称"
                            name="terminal_name"
                            className="search-form-item"
                        >
                            <Input
                                placeholder="请输入航站楼名称"
                                onKeyPress={handleKeyPress}
                                allowClear
                            />
                        </Form.Item>
                    </Col>

                    <Col xs={24} sm={12} md={8} lg={6}>
                        <Form.Item
                            label="描述"
                            name="description"
                            className="search-form-item"
                        >
                            <Input
                                placeholder="请输入描述关键词"
                                onKeyPress={handleKeyPress}
                                allowClear
                            />
                        </Form.Item>
                    </Col>

                    <Col xs={24} sm={24} md={8} lg={12}>
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

export default TerminalSearchBar;
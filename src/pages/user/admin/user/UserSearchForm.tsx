import React from 'react';
import { Form, Input, Button, Row, Col } from 'antd';
import { SearchOutlined, ReloadOutlined } from '@ant-design/icons';

interface UserSearchFormProps {
    onSearch: (values: any) => void;
}

const UserSearchForm: React.FC<UserSearchFormProps> = ({ onSearch }) => {
    const [form] = Form.useForm();

    const handleSubmit = (values: any) => {
        onSearch(values);
    };

    const handleReset = () => {
        form.resetFields();
        onSearch({});
    };

    return (
        <Form
            form={form}
            layout="inline"
            onFinish={handleSubmit}
            className="user-search-form"
        >
            <Row gutter={16} style={{ width: '100%' }}>
                <Col span={6}>
                    <Form.Item name="username" label="用户名">
                        <Input placeholder="请输入用户名" />
                    </Form.Item>
                </Col>
                <Col span={6}>
                    <Form.Item name="name" label="姓名">
                        <Input placeholder="请输入姓名" />
                    </Form.Item>
                </Col>
                <Col span={6}>
                    <Form.Item name="email" label="邮箱">
                        <Input placeholder="请输入邮箱" />
                    </Form.Item>
                </Col>
                <Col span={6}>
                    <Form.Item>
                        <Button type="primary" htmlType="submit" icon={<SearchOutlined />}>
                            搜索
                        </Button>
                        <Button style={{ marginLeft: 8 }} onClick={handleReset} icon={<ReloadOutlined />}>
                            重置
                        </Button>
                    </Form.Item>
                </Col>
            </Row>
        </Form>
    );
};

export default UserSearchForm;
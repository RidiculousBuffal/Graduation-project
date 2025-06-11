import React from 'react';
import { Button, Checkbox, Form, Input } from 'antd';
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import styles from './style.module.css';

interface PasswordLoginProps {
    loading: boolean;
    onSubmit: (values: { username: string; password: string; remember: boolean }) => void;
}

const PasswordLogin: React.FC<PasswordLoginProps> = ({ loading, onSubmit }) => {
    const [form] = Form.useForm();

    return (
        <Form
            form={form}
            name="login"
            initialValues={{ remember: true }}
            onFinish={onSubmit}
            size="large"
            layout="vertical"
        >
            <Form.Item
                name="username"
                initialValue={window.localStorage.getItem("username") ?? ""}
                rules={[
                    { required: true, message: '请输入用户名!' },
                    { min: 5, message: '用户名至少5个字符' }
                ]}
            >
                <Input prefix={<UserOutlined />} placeholder="用户名" />
            </Form.Item>

            <Form.Item
                name="password"
                rules={[{ required: true, message: '请输入密码!' }]}
                initialValue={window.localStorage.getItem("password") ?? ""}
            >
                <Input.Password prefix={<LockOutlined />} placeholder="密码" />
            </Form.Item>

            <Form.Item>
                <Form.Item name="remember" valuePropName="checked" noStyle>
                    <Checkbox>记住我</Checkbox>
                </Form.Item>
            </Form.Item>

            <Form.Item>
                <Button
                    type="primary"
                    htmlType="submit"
                    className={styles.submitButton}
                    loading={loading}
                >
                    登录
                </Button>
            </Form.Item>
        </Form>
    );
};

export default PasswordLogin;
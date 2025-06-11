import React from 'react';
import {Button, Form, Input} from 'antd';
import {LockOutlined, MailOutlined, UserOutlined} from '@ant-design/icons';
import styles from './style.module.css';

interface RegisterProps {
    loading: boolean;
    onSubmit: (values: { username: string; password: string; email: string }) => void;
}

const Register: React.FC<RegisterProps> = ({loading, onSubmit}) => {
    const [form] = Form.useForm();

    return (
        <Form
            form={form}
            name="register"
            onFinish={onSubmit}
            size="large"
            layout="vertical"
        >
            <Form.Item
                name="username"
                rules={[
                    {required: true, message: '请输入用户名!'},
                    {min: 5, max: 20, message: '用户名长度为5-20个字符'}
                ]}
            >
                <Input prefix={<UserOutlined/>} placeholder="用户名"/>
            </Form.Item>

            <Form.Item
                name="email"
                rules={[
                    {type: 'email', message: '请输入有效的邮箱地址!'}
                ]}
            >
                <Input prefix={<MailOutlined/>} placeholder="邮箱"/>
            </Form.Item>

            <Form.Item
                name="password"
                rules={[{required: true, message: '请输入密码!'}]}
            >
                <Input.Password prefix={<LockOutlined/>} placeholder="密码"/>
            </Form.Item>

            <Form.Item
                name="confirm"
                dependencies={['password']}
                rules={[
                    {required: true, message: '请确认密码!'},
                    ({getFieldValue}) => ({
                        validator(_, value) {
                            if (!value || getFieldValue('password') === value) {
                                return Promise.resolve();
                            }
                            return Promise.reject(new Error('两次输入的密码不匹配!'));
                        },
                    }),
                ]}
            >
                <Input.Password prefix={<LockOutlined/>} placeholder="确认密码"/>
            </Form.Item>

            <Form.Item>
                <Button
                    type="primary"
                    htmlType="submit"
                    className={styles.submitButton}
                    loading={loading}
                >
                    注册
                </Button>
            </Form.Item>
        </Form>
    );
};

export default Register;
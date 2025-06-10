import React, {useState} from 'react';
import {Button, Card, Checkbox, Form, Input, Tabs, Typography} from 'antd';
import {LockOutlined, MailOutlined, UserOutlined} from '@ant-design/icons';
import {useNavigate} from 'react-router';
import {AuthService} from '../../services/AuthService';
import styles from './style.module.css';

const {Title} = Typography;
const {TabPane} = Tabs;

const Login: React.FC = () => {
    const [loginForm] = Form.useForm();
    const [registerForm] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (values: { username: string; password: string; remember: boolean }) => {
        try {
            setLoading(true);
            const success = await AuthService.login(values.username, values.password);
            if (success) {
                navigate('/console');
            }
        } finally {
            setLoading(false);
        }
    };

    const handleRegister = async (values: { username: string; password: string; email: string }) => {
        try {
            setLoading(true);
            const success = await AuthService.register(values.username, values.password, values.email);
            if (success) {
                // 切换到登录标签
                registerForm.resetFields();
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.container}>
            <div className={styles.content}>
                <Card className={styles.card}>
                    <Tabs defaultActiveKey="login" centered>
                        <TabPane tab="登录" key="login">
                            <Form
                                form={loginForm}
                                name="login"
                                initialValues={{remember: true}}
                                onFinish={handleLogin}
                                size="large"
                                layout="vertical"
                            >
                                <Form.Item
                                    name="username"
                                    rules={[{required: true, message: '请输入用户名!'}, {
                                        min: 5,
                                        message: '用户名至少5个字符'
                                    }]}
                                >
                                    <Input prefix={<UserOutlined/>} placeholder="用户名"/>
                                </Form.Item>
                                <Form.Item
                                    name="password"
                                    rules={[{required: true, message: '请输入密码!'}]}
                                >
                                    <Input.Password prefix={<LockOutlined/>} placeholder="密码"/>
                                </Form.Item>
                                <Form.Item>
                                    <Form.Item name="remember" valuePropName="checked" noStyle>
                                        <Checkbox>记住我</Checkbox>
                                    </Form.Item>
                                </Form.Item>
                                <Form.Item>
                                    <Button type="primary" htmlType="submit" className={styles.submitButton}
                                            loading={loading}>
                                        登录
                                    </Button>
                                </Form.Item>
                            </Form>
                        </TabPane>
                        <TabPane tab="注册" key="register">
                            <Form
                                form={registerForm}
                                name="register"
                                onFinish={handleRegister}
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
                                    <Button type="primary" htmlType="submit" className={styles.submitButton}
                                            loading={loading}>
                                        注册
                                    </Button>
                                </Form.Item>
                            </Form>
                        </TabPane>
                    </Tabs>
                </Card>
            </div>
        </div>
    );
};

export default Login;

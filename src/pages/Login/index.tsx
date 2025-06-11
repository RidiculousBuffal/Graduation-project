import React, {useState} from 'react';
import {Card, Tabs, Typography} from 'antd';
import {useNavigate} from 'react-router';
import {AuthService} from '../../services/AuthService';
import PasswordLogin from './PasswordLogin';
import Register from './Register';
import FaceLogin from './FaceLogin';
import styles from './style.module.css';

const {Title} = Typography;
const {TabPane} = Tabs;

const Login: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handlePasswordLogin = async (values: { username: string; password: string; remember: boolean }) => {
        try {
            setLoading(true);
            if (values.remember) {
                window.localStorage.setItem("password", values.password);
                window.localStorage.setItem("username", values.username);
            } else {
                window.localStorage.removeItem("password");
                window.localStorage.removeItem("username");
            }
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

            }
        } finally {
            setLoading(false);
        }
    };

    const handleFaceLogin = async (faceData: string) => {
        try {
            setLoading(true);
            const success = await AuthService.loginByFaceInfo(faceData);
            if (success) {
                navigate('/console');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.container}>
            <div className={styles.content}>
                <div className={styles.header}>
                    <Title level={2} className={styles.title}>
                        欢迎登录
                    </Title>
                </div>

                <Card className={styles.card}>
                    <Tabs defaultActiveKey="password" centered>
                        <TabPane tab="密码登录" key="password">
                            <PasswordLogin
                                loading={loading}
                                onSubmit={handlePasswordLogin}
                            />
                        </TabPane>

                        <TabPane tab="人脸识别" key="face">
                            <FaceLogin
                                loading={loading}
                                onSubmit={handleFaceLogin}
                            />
                        </TabPane>

                        <TabPane tab="注册" key="register">
                            <Register
                                loading={loading}
                                onSubmit={handleRegister}
                            />
                        </TabPane>
                    </Tabs>
                </Card>
            </div>
        </div>
    );
};

export default Login;
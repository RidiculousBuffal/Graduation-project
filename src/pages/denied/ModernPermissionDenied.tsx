import React from 'react';
import {Button, Space, Typography} from 'antd';
import {LockOutlined, HomeOutlined, ArrowLeftOutlined} from '@ant-design/icons';
import {useNavigate} from 'react-router';
import './ModernPermissionDenied.css';

const {Title, Text} = Typography;

const ModernPermissionDenied = () => {
    const navigate = useNavigate();

    const handleGoHome = () => {
        navigate('/');
    };

    const handleGoBack = () => {
        navigate(-1);
    };

    return (
        <div className="modern-permission-container">
            <div className="permission-card">
                <div className="lock-icon-wrapper">
                    <LockOutlined className="lock-icon"/>
                </div>

                <div className="content-section">
                    <Title level={1} className="error-code">403</Title>
                    <Title level={3} className="error-title">访问受限</Title>
                    <Text className="error-description">
                        很抱歉，您当前没有权限访问此页面。
                        <br/>
                        请联系管理员获取相应权限或返回其他页面。
                    </Text>
                </div>

                <div className="action-section">
                    <Space size="large">
                        <Button
                            type="primary"
                            size="large"
                            icon={<HomeOutlined/>}
                            onClick={handleGoHome}
                            className="primary-btn"
                        >
                            返回首页
                        </Button>
                        <Button
                            size="large"
                            icon={<ArrowLeftOutlined/>}
                            onClick={handleGoBack}
                            className="secondary-btn"
                        >
                            返回上页
                        </Button>
                    </Space>
                </div>
            </div>
        </div>
    );
};

export default ModernPermissionDenied;
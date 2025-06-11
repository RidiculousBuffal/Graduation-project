import React, {useState} from 'react';
import {Button, Typography, Space} from 'antd';
import {CameraOutlined, UserOutlined} from '@ant-design/icons';

import styles from './style.module.css';
import FaceCapture from "../../components/facelogin/FaceCapture.tsx";

const {Text} = Typography;

interface FaceLoginProps {
    loading: boolean;
    onSubmit: (faceData: string) => void;
}

const FaceLogin: React.FC<FaceLoginProps> = ({loading, onSubmit}) => {
    const [showCapture, setShowCapture] = useState(false);
    const [capturedFace, setCapturedFace] = useState<string>('');

    const handleFaceCapture = (base64: string) => {
        setCapturedFace(base64);
        setShowCapture(false);
    };

    const handleFaceLogin = () => {
        if (capturedFace) {
            onSubmit(capturedFace);
        }
    };

    const handleStartCapture = () => {
        setShowCapture(true);
        setCapturedFace('');
    };

    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            padding: '20px 0',
            minHeight: '400px',
            justifyContent: 'space-between'
        }}>
            <div style={{textAlign: 'center', marginBottom: '24px'}}>
                <UserOutlined style={{fontSize: '48px', color: '#1890ff', marginBottom: '16px'}}/>
                <Text type="secondary" style={{fontSize: '14px'}}>
                    请采集人脸信息进行登录
                </Text>
            </div>

            {showCapture ? (
                <div style={{marginBottom: '24px'}}>
                    <FaceCapture
                        onCapture={handleFaceCapture}
                        width={300}
                        height={225}
                    />
                </div>
            ) : (
                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    marginBottom: '24px'
                }}>
                    {capturedFace ? (
                        <div style={{textAlign: 'center'}}>
                            <img
                                src={capturedFace}
                                alt="Captured face"
                                style={{
                                    width: '120px',
                                    height: '120px',
                                    borderRadius: '50%',
                                    objectFit: 'cover',
                                    border: '3px solid #1890ff',
                                    marginBottom: '16px'
                                }}
                            />
                            <Text type="success" style={{display: 'block', fontSize: '14px'}}>
                                人脸采集成功
                            </Text>
                        </div>
                    ) : (
                        <div style={{
                            width: '120px',
                            height: '120px',
                            borderRadius: '50%',
                            border: '2px dashed #d9d9d9',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            marginBottom: '16px',
                            background: '#fafafa'
                        }}>
                            <CameraOutlined style={{fontSize: '32px', color: '#bfbfbf'}}/>
                        </div>
                    )}
                </div>
            )}

            <Space direction="vertical" size="middle" style={{width: '100%'}}>
                {!showCapture && !capturedFace && (
                    <Button
                        type="primary"
                        size="large"
                        icon={<CameraOutlined/>}
                        onClick={handleStartCapture}
                        className={styles.submitButton}
                        style={{background: 'linear-gradient(135deg, #1890ff, #722ed1)'}}
                    >
                        开始人脸识别
                    </Button>
                )}

                {capturedFace && !showCapture && (
                    <Space style={{width: '100%'}} direction="vertical" size="small">
                        <Button
                            type="primary"
                            size="large"
                            onClick={handleFaceLogin}
                            loading={loading}
                            className={styles.submitButton}
                            style={{background: 'linear-gradient(135deg, #00b894, #00cec9)'}}
                        >
                            人脸登录
                        </Button>
                        <Button
                            type="default"
                            size="large"
                            onClick={handleStartCapture}
                            className={styles.submitButton}
                        >
                            重新采集
                        </Button>
                    </Space>
                )}
            </Space>
        </div>
    );
};

export default FaceLogin;
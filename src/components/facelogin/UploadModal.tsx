
import React, {useState, useEffect, useRef} from 'react';
import {Modal, Button, Typography, Space, message} from 'antd';
import {SaveOutlined, CloseOutlined} from '@ant-design/icons';
import FaceCapture, {type FaceCaptureRef} from './FaceCapture';
import './UploadModal.css';

const {Title, Text} = Typography;

interface UploadModalProps {
    visible: boolean;
    onClose: () => void;
    onSave: (faceData: string) => Promise<void>;
    initialName?: string;
    existingFace?: string;
}

const UploadModal: React.FC<UploadModalProps> = ({
                                                     visible,
                                                     onClose,
                                                     onSave,
                                                     initialName = '',
                                                     existingFace
                                                 }) => {
    const [userName, setUserName] = useState(initialName);
    const [capturedFace, setCapturedFace] = useState<string>('');
    const [isUploading, setIsUploading] = useState(false);
    const faceCaptureRef = useRef<FaceCaptureRef>(null);

    // 设置初始人脸数据和用户名
    useEffect(() => {
        if (visible) {
            if (existingFace) {
                setCapturedFace(existingFace);
            }
            if (initialName) {
                setUserName(initialName);
            }
        }
    }, [existingFace, initialName, visible]);

    const handleFaceCapture = (base64: string) => {
        setCapturedFace(base64);
    };

    const handleUpload = async () => {
        if (!userName.trim()) {
            message.warning('请输入用户姓名');
            return;
        }

        if (!capturedFace) {
            message.warning('请先采集人脸');
            return;
        }

        setIsUploading(true);
        try {
            await onSave(capturedFace);
            handleClose();
        } catch (error) {
            message.error('保存失败，请重试');
        } finally {
            setIsUploading(false);
        }
    };

    const handleClose = () => {
        // 强制停止摄像头
        if (faceCaptureRef.current) {
            faceCaptureRef.current.stopCamera();
        }

        setUserName('');
        setCapturedFace('');
        setIsUploading(false);
        onClose();
    };

    // Modal 关闭时的额外清理
    const handleAfterClose = () => {
        if (faceCaptureRef.current) {
            faceCaptureRef.current.stopCamera();
        }
    };

    return (
        <Modal
            title={null}
            open={visible}
            onCancel={handleClose}
            footer={null}
            width={600}
            className="upload-modal"
            destroyOnHidden={true}
            afterClose={handleAfterClose}
        >
            <div className="modal-content">
                <div className="modal-header">
                    <Title level={3} className="modal-title">
                        {existingFace ? '更新人像信息' : '上传人像信息'}
                    </Title>
                    <Text type="secondary" className="modal-subtitle">
                        请输入姓名并采集人脸信息
                    </Text>
                </div>

                <div className="form-section">
                    <div className="capture-group">
                        <label className="input-label">人脸采集</label>
                        <FaceCapture
                            ref={faceCaptureRef}
                            onCapture={handleFaceCapture}
                            width={350}
                            height={260}
                        />
                    </div>
                </div>

                <div className="modal-actions">
                    <Space size="large">
                        <Button
                            size="large"
                            icon={<CloseOutlined/>}
                            onClick={handleClose}
                            className="cancel-btn"
                        >
                            取消
                        </Button>

                        <Button
                            type="primary"
                            size="large"
                            icon={<SaveOutlined/>}
                            onClick={handleUpload}
                            loading={isUploading}
                            className="upload-btn"
                        >
                            {isUploading ? '保存中...' : (existingFace ? '更新信息' : '保存信息')}
                        </Button>
                    </Space>
                </div>
            </div>
        </Modal>
    );
};

export default UploadModal;
// Security.tsx
import React, {useState} from 'react';
import {
    Form,
    Input,
    Button,
    Space,
    Typography,
    Avatar,
    message,
    Modal,
    Row,
    Col
} from 'antd';
import {
    LockOutlined,
    UserOutlined,
    CameraOutlined,
    EditOutlined,
    DeleteOutlined,
    EyeInvisibleOutlined,
    EyeTwoTone,
    SafetyOutlined
} from '@ant-design/icons';

import './Security.css';
import {useUserStore} from "../../../store/user/userStore.ts";
import UploadModal from "../../../components/facelogin/UploadModal.tsx";
import {UserService} from "../../../services/UserService.ts";
import {AuthService} from "../../../services/AuthService.ts";
import {useNavigate} from "react-router";

const {Title, Text} = Typography;
const {confirm} = Modal;

interface PasswordForm {
    currentPassword: string;
    newPassword: string;
    confirmPassword: string;
}

const Security: React.FC = () => {
    const {user} = useUserStore();
    const [passwordForm] = Form.useForm<PasswordForm>();
    const [isChangingPassword, setIsChangingPassword] = useState(false);
    const [faceModalVisible, setFaceModalVisible] = useState(false);
    const nav = useNavigate()
    // 重置密码
    const handlePasswordReset = async (values: PasswordForm) => {
        if (values.newPassword !== values.confirmPassword) {
            message.error('新密码和确认密码不一致');
            return;
        }
        setIsChangingPassword(true);
        if (await AuthService.updateUserPassword(values.currentPassword, values.newPassword)) {
            message.success("密码修改成功")
            AuthService.logout()
            nav('/login')
        }
        passwordForm.resetFields();
        setIsChangingPassword(false);
    };

    // 保存人脸信息
    const handleFaceSave = async (faceData: string) => {
        if (await AuthService.updateUserFaceInfo(faceData)) {
            message.success('人脸信息保存成功');
        }
        setFaceModalVisible(false);
    };

    // 删除人脸信息
    const handleDeleteFace = () => {
        confirm({
            title: '确认删除',
            content: '确定要删除当前的人脸信息吗？删除后将无法使用人脸登录功能。',
            okText: '确认删除',
            okType: 'danger',
            cancelText: '取消',
            onOk: async () => {
                try {
                    const updatedUser = {
                        ...user,
                        faceInfo: null
                    };
                    if (await UserService.deleteFaceInfo(updatedUser)) {
                        message.success("删除成功")
                    }
                } catch (error) {
                    message.error('删除失败，请重试');
                }
            }
        });
    };

    return (
        <div className="security-container">
            {/* 页面标题 */}
            <div className="security-header">
                <SafetyOutlined className="header-icon"/>
                <div className="header-content">
                    <Title level={2} className="header-title">安全设置</Title>
                    <Text className="header-subtitle">管理您的账户安全信息</Text>
                </div>
            </div>

            {/* 卡片容器 */}
            <div className="security-cards-container">
                <Row gutter={[24, 24]} justify="center" style={{width: "100%"}}>
                    {/* 密码设置卡片 */}
                    <Col xs={24} sm={24} md={12} lg={10} xl={8}>
                        <div className="security-card password-card">
                            <div className="card-header">
                                <LockOutlined className="card-icon"/>
                                <div className="card-title-group">
                                    <Title level={4} className="card-title">密码设置</Title>
                                    <Text className="card-subtitle">修改您的登录密码</Text>
                                </div>
                            </div>

                            <div className="card-content">
                                <Form
                                    form={passwordForm}
                                    layout="vertical"
                                    onFinish={handlePasswordReset}
                                    className="password-form"
                                >
                                    <Form.Item
                                        label="当前密码"
                                        name="currentPassword"
                                        rules={[
                                            {required: true, message: '请输入当前密码'},
                                            {min: 6, message: '密码长度至少6位'}
                                        ]}
                                    >
                                        <Input.Password
                                            placeholder="请输入当前密码"
                                            iconRender={(visible) =>
                                                visible ? <EyeTwoTone/> : <EyeInvisibleOutlined/>
                                            }
                                        />
                                    </Form.Item>

                                    <Form.Item
                                        label="新密码"
                                        name="newPassword"
                                        rules={[
                                            {required: true, message: '请输入新密码'},
                                            {min: 6, message: '密码长度至少6位'},
                                            {
                                                pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{6,}$/,
                                                message: '密码必须包含大小写字母和数字'
                                            }
                                        ]}
                                    >
                                        <Input.Password
                                            placeholder="请输入新密码"
                                            iconRender={(visible) =>
                                                visible ? <EyeTwoTone/> : <EyeInvisibleOutlined/>
                                            }
                                        />
                                    </Form.Item>

                                    <Form.Item
                                        label="确认新密码"
                                        name="confirmPassword"
                                        rules={[
                                            {required: true, message: '请确认新密码'},
                                            ({getFieldValue}) => ({
                                                validator(_, value) {
                                                    if (!value || getFieldValue('newPassword') === value) {
                                                        return Promise.resolve();
                                                    }
                                                    return Promise.reject(new Error('两次输入的密码不一致'));
                                                },
                                            }),
                                        ]}
                                    >
                                        <Input.Password
                                            placeholder="请再次输入新密码"
                                            iconRender={(visible) =>
                                                visible ? <EyeTwoTone/> : <EyeInvisibleOutlined/>
                                            }
                                        />
                                    </Form.Item>

                                    <Button
                                        type="primary"
                                        htmlType="submit"
                                        loading={isChangingPassword}
                                        className="submit-btn password-submit-btn"
                                        block
                                    >
                                        {isChangingPassword ? '修改中...' : '修改密码'}
                                    </Button>
                                </Form>
                            </div>
                        </div>
                    </Col>

                    {/* 人脸识别卡片 */}
                    <Col xs={24} sm={24} md={12} lg={10} xl={8}>
                        <div className="security-card face-card">
                            <div className="card-header">
                                <CameraOutlined className="card-icon"/>
                                <div className="card-title-group">
                                    <Title level={4} className="card-title">人脸识别</Title>
                                    <Text className="card-subtitle">设置人脸登录功能</Text>
                                </div>
                            </div>

                            <div className="card-content">
                                {user.faceInfo ? (
                                    <div className="face-info-display">
                                        <div className="face-avatar-section">
                                            <Avatar
                                                size={150}
                                                src={user.faceInfo}
                                                icon={<UserOutlined/>}
                                                className="face-avatar"
                                            />
                                            <div className="face-status">
                                                <div className="status-indicator active"></div>
                                                <Text className="status-text">已设置</Text>
                                            </div>
                                        </div>

                                        <div className="face-info-text">
                                            <Text style={{fontSize: "18px"}} strong>人脸信息已录入</Text>
                                            <br/>
                                            <Text style={{fontSize: "16px"}} type="secondary" className="face-desc">
                                                您可以使用人脸识别快速登录
                                            </Text>
                                        </div>

                                        <Space direction="vertical" size="small" className="face-actions">
                                            <Button
                                                type="primary"
                                                icon={<EditOutlined/>}
                                                onClick={() => setFaceModalVisible(true)}
                                                className="submit-btn update-btn"
                                                block
                                            >
                                                更新人脸信息
                                            </Button>
                                            <Button
                                                danger
                                                icon={<DeleteOutlined/>}
                                                onClick={handleDeleteFace}
                                                className="delete-btn"
                                                block
                                            >
                                                删除人脸信息
                                            </Button>
                                        </Space>
                                    </div>
                                ) : (
                                    <div className="face-info-empty">
                                        <div className="empty-face-section">
                                            <Avatar
                                                size={80}
                                                icon={<UserOutlined/>}
                                                className="empty-avatar"
                                            />
                                            <div className="face-status">
                                                <div className="status-indicator inactive"></div>
                                                <Text className="status-text">未设置</Text>
                                            </div>
                                        </div>

                                        <div className="empty-info-text">
                                            <Text style={{fontSize: "18px"}} strong>尚未设置人脸信息</Text>
                                            <br/>
                                            <Text style={{fontSize: "18px"}} type="secondary" className="face-desc">
                                                设置后可使用人脸识别快速登录
                                            </Text>
                                        </div>

                                        <Button
                                            type="primary"
                                            icon={<CameraOutlined/>}
                                            onClick={() => setFaceModalVisible(true)}
                                            className="submit-btn add-face-btn"
                                            block
                                        >
                                            添加人脸信息
                                        </Button>
                                    </div>
                                )}
                            </div>
                        </div>
                    </Col>
                </Row>
            </div>

            {/* 人脸信息上传/更新模态框 */}
            <UploadModal
                visible={faceModalVisible}
                onClose={() => setFaceModalVisible(false)}
                onSave={handleFaceSave}
                initialName={user.name || 'hack_user'}
                existingFace={user.faceInfo || undefined}
            />
        </div>
    );
};

export default Security;
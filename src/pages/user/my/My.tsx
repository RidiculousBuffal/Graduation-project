import React, {useState} from 'react';
import {Card, Typography, Row, Col, Form, Input, Button, Divider, message, Select} from 'antd';
import {
    UserOutlined,
    MailOutlined,
    PhoneOutlined,
    TeamOutlined,
    IdcardOutlined,
    CalendarOutlined
} from '@ant-design/icons';
import {useUserStore} from '../../../store/user/userStore';
import type {userType} from '../../../store/user/types';
import './my.css';
import Avatar, {genConfig} from "react-nice-avatar";
import {UserService} from "../../../services/UserService.ts";

const {Title, Text} = Typography;
const {Option} = Select;

function My() {
    const {user, roles, permissions, setUser} = useUserStore();
    const [editing, setEditing] = useState(false);
    const [loading, setLoading] = useState(false)
    const [form] = Form.useForm();

    // 初始化表单数据
    const initialValues = {
        ...user
    };

    // 处理表单提交
    const handleSubmit = async (values: Partial<userType>) => {
        // 保留不可修改的字段
        setLoading(true)
        if (await UserService.updateUserInfo(values)) {
            message.success("用户信息更新成功")
        } else {
            form.resetFields();
        }
        setLoading(false)
        setEditing(false)
    };

    // 取消编辑
    const handleCancel = () => {
        form.resetFields();
        setEditing(false);
    };

    return (
        <div className="my-profile-container">
            <Row gutter={[24, 24]}>
                <Col xs={24} lg={8}>
                    <Card className="profile-card" title="个人信息">
                        <div className="avatar-container">
                            <Avatar style={{width: "5rem", height: "5rem"}} {...genConfig(user.username)}/>
                        </div>
                        <Title level={3} className="user-name">{user.name || '未设置姓名'}</Title>
                        <Text type="secondary" className="username">@{user.username}</Text>
                        <Divider/>
                        <div className="info-item">
                            <IdcardOutlined className="info-icon"/>
                            <div>
                                <Text type="secondary">用户ID</Text>
                                <div>{user.user_id}</div>
                            </div>
                        </div>

                        <div className="info-item">
                            <TeamOutlined className="info-icon"/>
                            <div>
                                <Text type="secondary">角色</Text>
                                <div>
                                    {roles && roles.length > 0
                                        ? roles.map(role => role.role_name).join(', ')
                                        : '暂无角色'}
                                </div>
                            </div>
                        </div>

                        <div className="info-item">
                            <CalendarOutlined className="info-icon"/>
                            <div>
                                <Text type="secondary">注册时间</Text>
                                <div>{user.created_at}</div>
                            </div>
                        </div>

                        <div className="info-item">
                            <CalendarOutlined className="info-icon"/>
                            <div>
                                <Text type="secondary">最后登录</Text>
                                <div>{user.last_login}</div>
                            </div>
                        </div>
                    </Card>
                </Col>

                <Col xs={24} lg={16}>
                    <Card className="profile-card" title="详细资料"
                          extra={!editing ?
                              <Button type="primary" onClick={() => setEditing(true)}>编辑</Button> :
                              null
                          }>
                        {!editing ? (
                            <div className="profile-details">
                                <Row gutter={[24, 24]}>
                                    <Col span={12}>
                                        <div className="detail-item">
                                            <Text type="secondary">姓名</Text>
                                            <div>{user.name || '未设置'}</div>
                                        </div>
                                    </Col>
                                    <Col span={12}>
                                        <div className="detail-item">
                                            <Text type="secondary">用户名</Text>
                                            <div>{user.username}</div>
                                        </div>
                                    </Col>
                                    <Col span={12}>
                                        <div className="detail-item">
                                            <Text type="secondary">邮箱</Text>
                                            <div>{user.email || '未设置'}</div>
                                        </div>
                                    </Col>
                                    <Col span={12}>
                                        <div className="detail-item">
                                            <Text type="secondary">电话</Text>
                                            <div>{user.phone || '未设置'}</div>
                                        </div>
                                    </Col>
                                    <Col span={12}>
                                        <div className="detail-item">
                                            <Text type="secondary">部门</Text>
                                            <div>{user.department || '未设置'}</div>
                                        </div>
                                    </Col>
                                    <Col span={12}>
                                        <div className="detail-item">
                                            <Text type="secondary">性别</Text>
                                            <div>{user.gender || '未设置'}</div>
                                        </div>
                                    </Col>
                                    <Col span={12}>
                                        <div className="detail-item">
                                            <Text type="secondary">工作年限</Text>
                                            <div>{user.work_years !== null ? `${user.work_years}年` : '未设置'}</div>
                                        </div>
                                    </Col>
                                    <Col span={12}>
                                        <div className="detail-item">
                                            <Text type="secondary">账号状态</Text>
                                            <div>{user.status ? '激活' : '禁用'}</div>
                                        </div>
                                    </Col>
                                </Row>

                                <Divider/>

                                <div className="permission-section">
                                    <Title level={5}>我的权限</Title>
                                    <div className="permission-list">
                                        {permissions && permissions.length > 0 ? (
                                            permissions.map((perm, index) => (
                                                <div key={perm.permission_id} className="permission-tag">
                                                    {perm.permission_name}
                                                    <Text type="secondary"> - {perm.description}</Text>
                                                </div>
                                            ))
                                        ) : (
                                            <Text type="secondary">暂无权限</Text>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <Form
                                form={form}
                                layout="vertical"
                                initialValues={initialValues}
                                onFinish={handleSubmit}
                            >
                                <Row gutter={24}>
                                    <Col span={12}>
                                        <Form.Item name="name" label="姓名">
                                            <Input placeholder="请输入姓名"/>
                                        </Form.Item>
                                    </Col>
                                    <Col span={12}>
                                        <Form.Item name="username" label="用户名（不可修改）">
                                            <Input disabled/>
                                        </Form.Item>
                                    </Col>
                                    <Col span={12}>
                                        <Form.Item name="email" label="邮箱" rules={[
                                            {type: 'email', message: '请输入有效的邮箱地址'}
                                        ]}>
                                            <Input prefix={<MailOutlined/>} placeholder="请输入邮箱"/>
                                        </Form.Item>
                                    </Col>
                                    <Col span={12}>
                                        <Form.Item name="phone" label="电话" rules={[
                                            {pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号码'}
                                        ]}>
                                            <Input prefix={<PhoneOutlined/>} placeholder="请输入电话号码"/>
                                        </Form.Item>
                                    </Col>
                                    <Col span={12}>
                                        <Form.Item name="department" label="部门">
                                            <Input placeholder="请输入部门"/>
                                        </Form.Item>
                                    </Col>
                                    <Col span={12}>
                                        <Form.Item name="gender" label="性别">
                                            <Select placeholder="请选择性别">
                                                <Option value="男">男</Option>
                                                <Option value="女">女</Option>
                                                <Option value="其他">其他</Option>
                                            </Select>
                                        </Form.Item>
                                    </Col>
                                    <Col span={12}>
                                        <Form.Item name="work_years" label="工作年限">
                                            <Input type="number" min={0} placeholder="请输入工作年限"/>
                                        </Form.Item>
                                    </Col>
                                    <Col span={12}>
                                        <Form.Item name="user_id" label="用户ID（不可修改）">
                                            <Input disabled/>
                                        </Form.Item>
                                    </Col>
                                </Row>

                                <Form.Item>
                                    <div className="form-buttons">
                                        <Button onClick={handleCancel}>取消</Button>
                                        <Button loading={loading} type="primary" htmlType="submit">保存</Button>
                                    </div>
                                </Form.Item>
                            </Form>
                        )}
                    </Card>
                </Col>
            </Row>
        </div>
    );
}

export default My;

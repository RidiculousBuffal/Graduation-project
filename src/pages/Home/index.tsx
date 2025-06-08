import React from 'react';
import {Avatar, Button, Card, Layout, Menu, Typography} from 'antd';
import {
    DashboardOutlined,
    LogoutOutlined,
    SettingOutlined,
    UserOutlined
} from '@ant-design/icons';

import {useUserStore} from '../../store/user/userStore';
import {AuthService} from '../../services/AuthService';
import styles from './style.module.css';
import {useNavigate} from "react-router";

const {Header, Content, Sider} = Layout;
const {Title, Text} = Typography;
const {Meta} = Card;

const Home: React.FC = () => {
    const navigate = useNavigate();
    const user = useUserStore((state) => state.user);
    const permissions = useUserStore((state) => state.permissions);
    const roles = useUserStore((state) => state.roles);

    const handleLogout = () => {
        AuthService.logout();
        navigate('/');
    };

    return (
        <Layout className={styles.layout}>
            <Header className={styles.header}>
                <div className={styles.logo}>
                    <Title level={4} style={{color: 'white', margin: 0}}>管理系统</Title>
                </div>
                <div className={styles.userInfo}>
                    <Avatar size="large" icon={<UserOutlined/>}/>
                    <Text className={styles.username}>{user.username}</Text>
                    <Button
                        type="text"
                        icon={<LogoutOutlined/>}
                        onClick={handleLogout}
                        className={styles.logoutButton}
                    >
                        退出
                    </Button>
                </div>
            </Header>
            <Layout>
                <Sider width={200} className={styles.sider}>
                    <Menu
                        mode="inline"
                        defaultSelectedKeys={['dashboard']}
                        style={{height: '100%', borderRight: 0}}
                        items={[
                            {
                                key: 'dashboard',
                                icon: <DashboardOutlined/>,
                                label: '仪表盘',
                            },
                            {
                                key: 'settings',
                                icon: <SettingOutlined/>,
                                label: '设置',
                            },
                        ]}
                    />
                </Sider>
                <Layout className={styles.mainContent}>
                    <Content className={styles.content}>
                        <Title level={2}>欢迎回来，{user.name || user.username}</Title>

                        <div className={styles.infoSection}>
                            <Card title="用户信息" className={styles.card}>
                                <Meta
                                    avatar={<Avatar icon={<UserOutlined/>}/>}
                                    title={user.name || user.username}
                                    description={user.email || '未设置邮箱'}
                                />
                                <div className={styles.userDetails}>
                                    <p><strong>用户 ID:</strong> {user.user_id}</p>
                                    <p><strong>部门:</strong> {user.department || '未设置'}</p>
                                    <p><strong>最后登录:</strong> {user.last_login}</p>
                                    <p><strong>账号状态:</strong> {user.status ? '正常' : '禁用'}</p>
                                </div>
                            </Card>

                            <Card title="权限信息" className={styles.card}>
                                <div className={styles.permissionList}>
                                    <Title level={5}>角色</Title>
                                    <div className={styles.tagList}>
                                        {roles.map((role) => (
                                            <div key={role.role_id} className={styles.tag}>
                                                {role.role_name}
                                            </div>
                                        ))}
                                    </div>

                                    <Title level={5}>权限</Title>
                                    <div className={styles.tagList}>
                                        {permissions.map((permission) => (
                                            <div key={permission.permission_id} className={styles.tag}>
                                                {permission.permission_name}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </Card>
                        </div>
                    </Content>
                </Layout>
            </Layout>
        </Layout>
    );
};

export default Home;

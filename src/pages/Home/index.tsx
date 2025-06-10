import React from 'react';
import {Button, Layout, Menu, Typography} from 'antd';
import {
    LogoutOutlined,
} from '@ant-design/icons';
import Avatar, {genConfig} from 'react-nice-avatar'
import {useUserStore} from '../../store/user/userStore';
import {AuthService} from '../../services/AuthService';
import styles from './style.module.css';
import {Outlet, useNavigate} from "react-router";
import {MyMenu} from "../../consts/menu.tsx";
import {Header} from "antd/es/layout/layout";
import Sider from "antd/es/layout/Sider";
import type {SelectInfo} from "rc-menu/lib/interface";

const {Title, Text} = Typography;


const Home: React.FC = () => {
    const navigate = useNavigate();
    const user = useUserStore((state) => state.user);
    const permissions = useUserStore((state) => state.permissions);

    const handleLogout = () => {
        AuthService.logout();
        navigate('/');
    };
    const handleSelect = ({keyPath}: SelectInfo) => {
        navigate(keyPath.reverse().join('/'));
    }

    return (
        <Layout className={styles.layout}>
            <Header className={styles.header}>
                <div className={styles.logo}>
                    <Title level={4} style={{color: 'white', margin: 0}}>管理系统</Title>
                </div>
                <div className={styles.userInfo}>
                    <Avatar  style={{width:"3rem",height:"3rem"}} {...genConfig(user.username)}/>
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
                        onSelect={handleSelect}
                        mode="inline"
                        defaultSelectedKeys={['dashboard']}
                        style={{height: '100%', borderRight: 0}}
                        items={MyMenu.getMenu(permissions)}
                    />
                </Sider>
                <Layout className={styles.mainContent}>
                    <Outlet/>
                </Layout>
            </Layout>
        </Layout>
    );
};

export default Home;

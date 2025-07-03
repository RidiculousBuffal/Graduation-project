import React, {useEffect, useState} from 'react';
import {Layout, Typography, message, Space} from 'antd';
import {FileTextOutlined} from '@ant-design/icons';
import {useLogStore} from '@/store/log/logStore';
import {AuditService} from '@/services/AuditService';
import type {blockChainStatus} from '@/api/auditAPI';
import BlockchainStatusCard from './BlockChainStatusCard.tsx';
import LogTable from './LogTable';
import styles from './style.module.css';

const {Content} = Layout;
const {Title} = Typography;

const LogManagement: React.FC = () => {
    const {logs, logsPagination, setLogsPagination} = useLogStore();
    const [loading, setLoading] = useState(false);
    const [statusLoading, setStatusLoading] = useState(false);
    const [blockchainStatus, setBlockchainStatus] = useState<blockChainStatus | null>(null);

    // 获取区块链状态
    const fetchBlockchainStatus = async () => {
        try {
            setStatusLoading(true);
            const response = await AuditService.getAuditStatus();
            if (response) {
                setBlockchainStatus(response);
            } else {
                message.error('获取区块链状态失败');
            }
        } catch (error) {
            console.error('获取区块链状态失败:', error);
            message.error('获取区块链状态失败');
        } finally {
            setStatusLoading(false);
        }
    };

    // 获取日志数据
    const fetchLogs = async () => {
        try {
            setLoading(true);
            const response = await AuditService.getAuditLog();
            if (!response) {
                message.error('获取日志数据失败');
            }
        } catch (error) {
            console.error('获取日志数据失败:', error);
            message.error('获取日志数据失败');
        } finally {
            setLoading(false);
        }
    };

    // 处理分页变化
    const handleTableChange = (page: number, pageSize: number) => {
        setLogsPagination({
            ...logsPagination,
            current_page: page,
            page_size: pageSize
        });
        fetchLogs();
    };

    // 初始化数据
    useEffect(() => {
        fetchBlockchainStatus();
        fetchLogs();
    }, []);


    return (
        <Layout className={styles.layout}>
            <Content className={styles.mainContent}>
                <div className={styles.content}>
                    <Space direction="vertical" size="large" style={{width: '100%'}}>
                        {/* 页面标题 */}
                        <div>
                            <Title level={2}>
                                <FileTextOutlined style={{marginRight: 8}}/>
                                日志管理
                            </Title>
                        </div>

                        {/* 区块链状态卡片 */}
                        <BlockchainStatusCard
                            data={blockchainStatus}
                            loading={statusLoading}
                        />

                        {/* 日志表格 */}
                        <LogTable
                            data={logs}
                            loading={loading}
                            pagination={{
                                current: logsPagination.current_page,
                                pageSize: logsPagination.page_size,
                                total: logsPagination.total,
                                showSizeChanger: true,
                                showQuickJumper: true,
                                showTotal: (total, range) =>
                                    `第 ${range[0]}-${range[1]} 条，共 ${total} 条数据`,
                            }}
                            onChange={handleTableChange}
                        />
                    </Space>
                </div>
            </Content>
        </Layout>
    );
};

export default LogManagement;
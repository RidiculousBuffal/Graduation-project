import React, { useState } from 'react';
import { Table, Button, Tag, Space, Typography } from 'antd';
import { EyeOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import {type Log } from '@/store/log/types';
import LogActionModal from './LogActionModal';
import dayjs from 'dayjs';

const { Text } = Typography;

interface LogTableProps {
    data: Log[];
    loading?: boolean;
    pagination?: {
        current: number;
        pageSize: number;
        total: number;
        showSizeChanger?: boolean;
        showQuickJumper?: boolean;
        showTotal?: (total: number, range: [number, number]) => string;
    };
    onChange?: (page: number, pageSize: number) => void;
}

const LogTable: React.FC<LogTableProps> = ({
                                               data,
                                               loading = false,
                                               pagination,
                                               onChange
                                           }) => {
    const [modalVisible, setModalVisible] = useState(false);
    const [selectedAction, setSelectedAction] = useState<any>(null);
    const [modalTitle, setModalTitle] = useState('');

    const handleViewAction = (action: any, eventName?: string) => {
        setSelectedAction(action);
        setModalTitle(eventName ? `事件详情 - ${eventName}` : '日志详情');
        setModalVisible(true);
    };

    const columns: ColumnsType<Log> = [
        {
            title: '日志ID',
            dataIndex: 'log_id',
            key: 'log_id',
            width: 100,
            render: (id) => <Text code>{id}</Text>
        },
        {
            title: '用户ID',
            dataIndex: 'user_id',
            key: 'user_id',
            width: 150,
            render: (userId) => <Text code>{userId}</Text>
        },
        {
            title: '事件名称',
            dataIndex: ['action', 'event_name'],
            key: 'event_name',
            width: 200,
            render: (eventName, record) => (
                <Button
                    type="link"
                    onClick={() => handleViewAction(record.action, eventName)}
                    style={{ padding: 0 }}
                >
                    {eventName || '未知事件'}
                </Button>
            )
        },
        {
            title: '时间戳',
            dataIndex: 'timestamp',
            key: 'timestamp',
            width: 180,
            render: (timestamp) => (
                <Text>{dayjs(timestamp).format('YYYY-MM-DD HH:mm:ss')}</Text>
            )
        },
        {
            title: '交易哈希',
            dataIndex: 'blockchain_tx_hash',
            key: 'blockchain_tx_hash',
            width: 200,
            render: (hash) => (
                <Text code style={{ fontSize: '12px' }}>
                    {hash?.slice(0, 20)}...
                </Text>
            )
        },
        {
            title: '区块号',
            dataIndex: 'blockchain_block_number',
            key: 'blockchain_block_number',
            width: 120,
            render: (blockNumber) => (
                <Tag color="blue">{blockNumber}</Tag>
            )
        },
        {
            title: '操作者',
            dataIndex: 'blockchain_operator',
            key: 'blockchain_operator',
            width: 150,
            render: (operator) => <Text code>{operator}</Text>
        },
        {
            title: '操作',
            key: 'action',
            width: 100,
            render: (_, record) => (
                <Space>
                    <Button
                        type="primary"
                        size="small"
                        icon={<EyeOutlined />}
                        onClick={() => handleViewAction(record.action, record.action.event_name)}
                    >
                        查看
                    </Button>
                </Space>
            )
        }
    ];

    return (
        <>
            <Table
                columns={columns}
                dataSource={data}
                loading={loading}
                rowKey="log_id"
                pagination={pagination ? {
                    ...pagination,
                    showSizeChanger: true,
                    showQuickJumper: true,
                    showTotal: (total, range) =>
                        `第 ${range[0]}-${range[1]} 条，共 ${total} 条数据`,
                    onChange: onChange
                } : false}
                scroll={{ x: 1200 }}
                size="middle"
            />

            <LogActionModal
                visible={modalVisible}
                onClose={() => setModalVisible(false)}
                data={selectedAction}
                title={modalTitle}
            />
        </>
    );
};

export default LogTable;
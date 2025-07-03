import React, { useState } from 'react';
import { Card, Button, Tag, Space, Typography } from 'antd';
import { EyeOutlined, LinkOutlined } from '@ant-design/icons';
import type {blockChainStatus} from '@/api/auditAPI';
import BlockchainStatusModal from './BlockchainStatusModal';

const { Text, Title } = Typography;

interface BlockchainStatusCardProps {
    data: blockChainStatus | null;
    loading?: boolean;
}

const BlockchainStatusCard: React.FC<BlockchainStatusCardProps> = ({
                                                                       data,
                                                                       loading = false
                                                                   }) => {
    const [modalVisible, setModalVisible] = useState(false);

    const getStatusColor = (status: string) => {
        switch (status?.toLowerCase()) {
            case 'active':
            case 'running':
                return 'green';
            case 'inactive':
            case 'stopped':
                return 'red';
            case 'pending':
                return 'orange';
            default:
                return 'blue';
        }
    };

    return (
        <>
            <Card
                title={
                    <Space>
                        <LinkOutlined />
                        <Title level={4} style={{ margin: 0 }}>区块链状态</Title>
                    </Space>
                }
                loading={loading}
                extra={
                    data?.abi && (
                        <Button
                            type="primary"
                            icon={<EyeOutlined />}
                            onClick={() => setModalVisible(true)}
                        >
                            查看 ABI
                        </Button>
                    )
                }
            >
                {data && (
                    <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                        <div>
                            <Text strong>状态: </Text>
                            <Tag color={getStatusColor(data.status)}>
                                {data.status || '未知'}
                            </Tag>
                        </div>
                        <div>
                            <Text strong>合约地址: </Text>
                            <Text code>{data.address}</Text>
                        </div>
                        <div>
                            <Text strong>节点URL: </Text>
                            <Text code>{data.url}</Text>
                        </div>
                    </Space>
                )}
            </Card>

            <BlockchainStatusModal
                visible={modalVisible}
                onClose={() => setModalVisible(false)}
                data={data}
            />
        </>
    );
};

export default BlockchainStatusCard;
import React from 'react';
import { Modal } from 'antd';
import JsonView from '@uiw/react-json-view';
import type {blockChainStatus} from '@/api/auditAPI';

interface BlockchainStatusModalProps {
    visible: boolean;
    onClose: () => void;
    data: blockChainStatus | null;
}

const BlockchainStatusModal: React.FC<BlockchainStatusModalProps> = ({
                                                                         visible,
                                                                         onClose,
                                                                         data
                                                                     }) => {
    return (
        <Modal
            title="区块链状态 - ABI详情"
            open={visible}
            onCancel={onClose}
            footer={null}
            width={800}
        >
            {data?.abi && (
                <div style={{ maxHeight: '500px', overflow: 'auto' }}>
                    <JsonView
                        value={data.abi}
                        style={{
                            backgroundColor: '#f5f5f5',
                            padding: '16px',
                            borderRadius: '8px'
                        }}
                    />
                </div>
            )}
        </Modal>
    );
};

export default BlockchainStatusModal;
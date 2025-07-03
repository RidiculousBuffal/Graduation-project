import React from 'react';
import { Modal } from 'antd';
import JsonView from '@uiw/react-json-view';
import type { action } from '@/store/log/types';

interface LogActionModalProps {
    visible: boolean;
    onClose: () => void;
    data: action | null;
    title?: string;
}

const LogActionModal: React.FC<LogActionModalProps> = ({
                                                           visible,
                                                           onClose,
                                                           data,
                                                           title = '日志详情'
                                                       }) => {
    return (
        <Modal
            title={title}
            open={visible}
            onCancel={onClose}
            footer={null}
            width={800}
        >
            {data && (
                <div style={{ maxHeight: '500px', overflow: 'auto' }}>
                    <JsonView
                        value={data}
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

export default LogActionModal;
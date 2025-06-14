import React from 'react';
import {Modal, Descriptions, Typography} from 'antd';
import './TerminalDetailModal.css';
import {Markdown} from "@lobehub/ui";
import type {terminalType} from "../../store/terminal/types.ts";

const {Text} = Typography;

interface TerminalDetailModalProps {
    visible: boolean;
    terminal: terminalType | null;
    onCancel: () => void;
}

const TerminalDetailModal: React.FC<TerminalDetailModalProps> = ({
                                                                     visible,
                                                                     terminal,
                                                                     onCancel
                                                                 }) => {
    if (!terminal) return null;

    return (
        <Modal
            title="航站楼详情"
            open={visible}
            onCancel={onCancel}
            footer={null}
            width={800}
            className="terminal-detail-modal"
        >
            <div className="terminal-detail-content">
                <Descriptions
                    column={1}
                    size="middle"
                    bordered
                >
                    <Descriptions.Item label="航站楼ID">
                        <Text code copyable>
                            {terminal.terminal_id}
                        </Text>
                    </Descriptions.Item>

                    <Descriptions.Item label="航站楼名称">
                        <Text strong style={{fontSize: '16px'}}>
                            {terminal.terminal_name}
                        </Text>
                    </Descriptions.Item>

                    <Descriptions.Item label="描述">
                        <div className="terminal-description">
                            {terminal.description ? (
                                <Markdown children={terminal.description}></Markdown>
                            ) : (
                                <Text type="secondary">暂无描述</Text>
                            )}
                        </div>
                    </Descriptions.Item>
                </Descriptions>
            </div>
        </Modal>
    );
};

export default TerminalDetailModal;
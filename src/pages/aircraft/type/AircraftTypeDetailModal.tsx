import React from 'react';
import {Modal, Descriptions, Typography} from 'antd';
import './AircraftTypeDetailModal.css';
import {Markdown} from "@lobehub/ui";
import type {aircraftTypeType} from "../../../store/aircraft/types.ts";


const {Text} = Typography;

interface AircraftTypeDetailModalProps {
    visible: boolean;
    aircraftType: aircraftTypeType | null;
    onCancel: () => void;
}

const AircraftTypeDetailModal: React.FC<AircraftTypeDetailModalProps> = ({
                                                                             visible,
                                                                             aircraftType,
                                                                             onCancel
                                                                         }) => {
    if (!aircraftType) return null;

    return (
        <Modal
            title="飞机类型详情"
            open={visible}
            onCancel={onCancel}
            footer={null}
            width={800}
            className="aircraft-type-detail-modal"
        >
            <div className="aircraft-type-detail-content">
                <Descriptions
                    column={1}
                    size="middle"
                    bordered
                >
                    <Descriptions.Item label="飞机类型ID">
                        <Text code copyable>
                            {aircraftType.typeid}
                        </Text>
                    </Descriptions.Item>

                    <Descriptions.Item label="飞机类型名称">
                        <Text strong style={{fontSize: '16px'}}>
                            {aircraftType.type_name}
                        </Text>
                    </Descriptions.Item>

                    <Descriptions.Item label="描述">
                        <div className="aircraft-type-description">
                            {aircraftType.description ? (
                                <Markdown children={aircraftType.description}></Markdown>
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

export default AircraftTypeDetailModal;
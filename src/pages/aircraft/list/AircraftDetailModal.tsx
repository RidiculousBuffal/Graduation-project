import React from 'react';
import { Modal, Descriptions, Typography, Tag } from 'antd';
import type { AircraftArrayType } from '../../../store/aircraft/types';
import './AircraftDetailModal.css';

const { Text } = Typography;

interface AircraftDetailModalProps {
    visible: boolean;
    aircraft: AircraftArrayType[0] | null;
    onCancel: () => void;
}

const AircraftDetailModal: React.FC<AircraftDetailModalProps> = ({
                                                                     visible,
                                                                     aircraft,
                                                                     onCancel
                                                                 }) => {
    if (!aircraft) return null;

    return (
        <Modal
            title="飞机详情"
            open={visible}
            onCancel={onCancel}
            footer={null}
            width={800}
            className="aircraft-detail-modal"
        >
            <div className="aircraft-detail-content">
                <Descriptions
                    column={2}
                    size="middle"
                    bordered
                >
                    <Descriptions.Item label="飞机ID" span={2}>
                        <Text code copyable>
                            {aircraft.aircraft_id}
                        </Text>
                    </Descriptions.Item>

                    <Descriptions.Item label="飞机名称">
                        <Text strong style={{ fontSize: '16px' }}>
                            {aircraft.aircraft_name}
                        </Text>
                    </Descriptions.Item>

                    <Descriptions.Item label="机龄">
                        <Tag color="blue">{aircraft.age}年</Tag>
                    </Descriptions.Item>

                    <Descriptions.Item label="飞机类型ID">
                        <Text code copyable>
                            {aircraft.typeid}
                        </Text>
                    </Descriptions.Item>

                    <Descriptions.Item label="飞机类型名称">
                        <Text strong style={{ fontSize: '16px' }}>
                            {aircraft.type_name}
                        </Text>
                    </Descriptions.Item>

                    <Descriptions.Item label="类型描述" span={2}>
                        <div className="aircraft-type-description">
                            {aircraft.description ? (
                                <Text>{aircraft.description}</Text>
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

export default AircraftDetailModal;
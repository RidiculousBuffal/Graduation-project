import React, { useState, useRef } from 'react';
import { Card, Button, message } from 'antd';
import { SelectOutlined } from '@ant-design/icons';
import type { InspectionItem } from '@/store/inspectionItem/types';
import type { Point } from '@/components/imageInnot/types';
import type { AircraftImageType } from "@/store/aircraft/types.ts";

interface InspectionImageViewerProps {
    aircraftImage: AircraftImageType | null;
    inspectionItems: InspectionItem[];
    // 【重构修改】: onPointsSelect现在接收单个Point对象
    onPointsSelect: (point: Point) => void;
}

const InspectionImageViewer: React.FC<InspectionImageViewerProps> = ({
                                                                         aircraftImage,
                                                                         inspectionItems,
                                                                         onPointsSelect
                                                                     }) => {
    const [selectedPoint, setSelectedPoint] = useState<Point | null>(null);
    const [isSelectMode, setIsSelectMode] = useState(false);
    const containerRef = useRef<HTMLDivElement>(null);

    const allPoints = aircraftImage?.image_json.pointInfo || [] as Point[];
    const uploadedPointIds = new Set(
        inspectionItems.map(item => item.item_point.point.id)
    );

    const handlePointClick = (point: Point) => {
        if (!isSelectMode) return;

        if (selectedPoint?.id === point.id) {
            setSelectedPoint(null);
        } else {
            setSelectedPoint(point);
        }
    };

    const handleConfirmSelect = () => {
        if (!selectedPoint) {
            message.warning('请先选择点位');
            return;
        }
        // 【重构修改】: 直接传递单个点位对象
        onPointsSelect(selectedPoint);
        setSelectedPoint(null);
        setIsSelectMode(false);
    };

    const handleCancelSelect = () => {
        setSelectedPoint(null);
        setIsSelectMode(false);
    };

    const getPointStyle = (point: Point): React.CSSProperties => {
        const isUploaded = uploadedPointIds.has(point.id);
        const isSelected = selectedPoint?.id === point.id;

        let backgroundColor = '#1890ff'; // normal
        if (isUploaded) {
            backgroundColor = '#52c41a'; // uploaded
        }
        if (isSelected) {
            backgroundColor = '#722ed1'; // selected
        }

        return {
            position: 'absolute',
            left: `${point.x}%`,
            top: `${point.y}%`,
            transform: 'translate(-50%, -50%)',
            width: '24px',
            height: '24px',
            borderRadius: '50%',
            backgroundColor,
            color: 'white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '12px',
            fontWeight: 'bold',
            cursor: isSelectMode ? 'pointer' : 'default',
            border: '2px solid white',
            boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
            zIndex: 10,
            userSelect: 'none',
            transition: 'all 0.2s ease',
            opacity: isSelectMode ? 1 : 0.8
        };
    };

    const imageUrl = aircraftImage?.image_json.fileInfo.download_url || '';

    return (
        <Card
            title="飞机底图与点位"
            extra={
                <div style={{ display: 'flex', gap: '8px' }}>
                    {isSelectMode ? (
                        <>
                            <Button onClick={handleCancelSelect}>取消</Button>
                            <Button
                                type="primary"
                                onClick={handleConfirmSelect}
                                disabled={!selectedPoint}
                            >
                                {/* 【重构修改】: 文本微调，更明确 */}
                                确认选择 {selectedPoint ? `点位 ${selectedPoint.id}` : ''}
                            </Button>
                        </>
                    ) : (
                        <Button
                            type="primary"
                            icon={<SelectOutlined />}
                            onClick={() => setIsSelectMode(true)}
                        >
                            选择点位
                        </Button>
                    )}
                </div>
            }
        >
            <div style={{
                position: 'relative',

                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                backgroundColor: '#f5f5f5',
                borderRadius: '4px',

            }}>
                {imageUrl ? (
                    <div ref={containerRef} style={{ position: 'relative', display: 'inline-block' }}>
                        <img
                            src={imageUrl}
                            alt="飞机底图"
                            style={{
                                display: 'block',
                                maxWidth: '100%',
                                maxHeight: '100%',
                                objectFit: 'contain'
                            }}
                        />
                        {allPoints.map((point) => (
                            <div
                                key={point.id}
                                style={getPointStyle(point)}
                                onClick={() => handlePointClick(point)}
                                title={`点位 ${point.id}`}
                            >
                                {point.id}
                            </div>
                        ))}
                    </div>
                ) : (
                    <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
                        暂无底图数据
                    </div>
                )}
            </div>

            <div style={{ marginTop: '16px', fontSize: '14px' }}>
                <div style={{ display: 'flex', gap: '16px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <div style={{ width: '12px', height: '12px', backgroundColor: '#1890ff', borderRadius: '50%' }} />
                        <span>未上传点位</span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <div style={{ width: '12px', height: '12px', backgroundColor: '#52c41a', borderRadius: '50%' }} />
                        <span>已上传点位</span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <div style={{ width: '12px', height: '12px', backgroundColor: '#722ed1', borderRadius: '50%' }} />
                        <span>当前选择</span>
                    </div>
                </div>
            </div>
        </Card>
    );
};

export default InspectionImageViewer;
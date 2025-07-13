import React, {useState, useRef} from 'react';
import {Card, Button, message} from 'antd';
import {SelectOutlined} from '@ant-design/icons';
import type {InspectionItem} from '@/store/inspectionItem/types';
import type {Point} from '@/components/imageInnot/types';
import type {AircraftImageType} from "@/store/aircraft/types.ts";

interface InspectionImageViewerProps {
    aircraftImage: AircraftImageType | null;
    inspectionItems: InspectionItem[];
    onPointsSelect: (points: Point[]) => void;
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
        inspectionItems.flatMap(item =>
            item.item_point.point.id
        )
    );

    const handlePointClick = (point: Point) => {
        if (!isSelectMode) return;

        if (uploadedPointIds.has(point.id)) {
            message.warning('该点位已上传，无法重复选择');
            return;
        }

        // 如果点击的是当前已选择的点位，则取消选择
        if (selectedPoint?.id === point.id) {
            setSelectedPoint(null);
        } else {
            // 否则选择新的点位
            setSelectedPoint(point);
        }
    };

    const handleConfirmSelect = () => {
        if (!selectedPoint) {
            message.warning('请先选择点位');
            return;
        }
        onPointsSelect([selectedPoint]);
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

        let backgroundColor = '#1890ff';
        if (isUploaded) {
            backgroundColor = '#52c41a';
        } else if (isSelected) {
            backgroundColor = '#722ed1';
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
            cursor: isSelectMode && !isUploaded ? 'pointer' : 'default',
            border: '2px solid white',
            boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
            zIndex: 10,
            userSelect: 'none',
            transition: 'all 0.2s ease',
            opacity: isSelectMode && !isUploaded ? 1 : 0.8
        };
    };

    const imageUrl = aircraftImage?.image_json.fileInfo.download_url || '';

    return (
        <Card
            title="飞机底图与点位"
            extra={
                <div style={{display: 'flex', gap: '8px'}}>
                    {isSelectMode ? (
                        <>
                            <Button onClick={handleCancelSelect}>取消</Button>
                            <Button
                                type="primary"
                                onClick={handleConfirmSelect}
                                disabled={!selectedPoint}
                            >
                                确认选择 {selectedPoint ? `(id=${selectedPoint.id})` : ''}
                            </Button>
                        </>
                    ) : (
                        <Button
                            type="primary"
                            icon={<SelectOutlined/>}
                            onClick={() => setIsSelectMode(true)}
                        >
                            选择点位
                        </Button>
                    )}
                </div>
            }
        >
            <div style={{position: 'relative', maxHeight: '600px', overflow: 'auto'}}>
                {imageUrl ? (
                    <div ref={containerRef} style={{position: 'relative', display: 'inline-block'}}>
                        <img
                            src={imageUrl}
                            alt="飞机底图"
                            style={{width: '100%', height: 'auto', display: 'block'}}
                        />
                        {allPoints.map((point) => (
                            <div
                                key={point.id}
                                style={getPointStyle(point)}
                                onClick={() => handlePointClick(point)}
                            >
                                {point.id}
                            </div>
                        ))}
                    </div>
                ) : (
                    <div style={{textAlign: 'center', padding: '40px', color: '#999'}}>
                        暂无底图数据
                    </div>
                )}
            </div>

            <div style={{marginTop: '16px', fontSize: '14px'}}>
                <div style={{display: 'flex', gap: '16px'}}>
                    <div style={{display: 'flex', alignItems: 'center', gap: '4px'}}>
                        <div style={{
                            width: '12px',
                            height: '12px',
                            backgroundColor: '#1890ff',
                            borderRadius: '50%'
                        }}/>
                        <span>未上传点位</span>
                    </div>
                    <div style={{display: 'flex', alignItems: 'center', gap: '4px'}}>
                        <div style={{
                            width: '12px',
                            height: '12px',
                            backgroundColor: '#52c41a',
                            borderRadius: '50%'
                        }}/>
                        <span>已上传点位</span>
                    </div>
                    <div style={{display: 'flex', alignItems: 'center', gap: '4px'}}>
                        <div style={{
                            width: '12px',
                            height: '12px',
                            backgroundColor: '#722ed1',
                            borderRadius: '50%'
                        }}/>
                        <span>已选择点位</span>
                    </div>
                </div>
            </div>
        </Card>
    );
};

export default InspectionImageViewer;
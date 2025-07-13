import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Button, message, Spin } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router';
import { useCurrentStore } from '@/store/current/currentStore';
import { AircraftImageService } from '@/services/AircraftImageService';
import { InspectionRecordItemService } from '@/services/InspectionRecordItemService';
import { useInspectionItemStore } from '@/store/inspectionItem/InspectionItemStore';
import InspectionImageViewer from './InspectionImageViewer';
import InspectionItemList from './InspectionItemList';
import InspectionItemUploader from './InspectionItemUploader';
import type { AircraftImageType } from "@/store/aircraft/types.ts";
import type { InspectionItem } from "@/store/inspectionItem/types.ts";
import type { Point } from "@/components/imageInnot/types.ts";
import './InspectionItem.css'

const InspectionSubmitPage: React.FC = () => {
    const navigate = useNavigate();
    const { currentInspectionRecord } = useCurrentStore();
    const { inspectionItems } = useInspectionItemStore();

    const [loading, setLoading] = useState(false);
    const [aircraftImage, setAircraftImage] = useState<AircraftImageType | null>(null);
    const [uploaderVisible, setUploaderVisible] = useState(false);
    // 【重构修改】: 状态从数组变为单个对象或null
    const [selectedPoint, setSelectedPoint] = useState<Point | null>(null);
    const [selectedExistingItem, setSelectedExistingItem] = useState<InspectionItem | null>(null);

    useEffect(() => {
        if (!currentInspectionRecord) {
            message.error('请先选择检测条目');
            navigate('/console/inspection/myInspect');
            return;
        }

        loadData();
    }, [currentInspectionRecord]);

    const loadData = async () => {
        if (!currentInspectionRecord) return;

        setLoading(true);
        try {
            const imageResult = await AircraftImageService.getAircraftImageById(
                currentInspectionRecord.reference_image_id
            );
            if (imageResult) {
                setAircraftImage(imageResult);
            }
            await InspectionRecordItemService.getInspectionRecordItemList();
        } catch (error) {
            message.error('加载数据失败');
        } finally {
            setLoading(false);
        }
    };

    // 【重构修改】: handler现在接收单个point对象
    const handlePointsSelect = (point: Point) => {
        const existingItem = inspectionItems.find(item => item.item_point.point.id === point.id);
        setSelectedExistingItem(existingItem || null);

        setSelectedPoint(point);
        setUploaderVisible(true);
    };

    const handleUploadSuccess = () => {
        setUploaderVisible(false);
        // 【重构修改】: 重置为null
        setSelectedPoint(null);
        setSelectedExistingItem(null);
        loadData();
    };

    const handleBack = () => {
        navigate('/console/inspection/myInspect');
    };

    const handleUploaderCancel = () => {
        setUploaderVisible(false);
        // 【重构修改】: 重置为null
        setSelectedPoint(null);
        setSelectedExistingItem(null);
    };

    if (!currentInspectionRecord) {
        return <div>检测条目信息缺失</div>;
    }

    return (
        <div style={{ padding: '24px' }}>
            <Card
                title={
                    <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                        <Button
                            icon={<ArrowLeftOutlined />}
                            onClick={handleBack}
                        >
                            返回
                        </Button>
                        <span>检测条目提交 - {currentInspectionRecord.inspection_name}</span>
                    </div>
                }
            >
                <Spin spinning={loading}>
                    <Row gutter={24}>
                        <Col span={16}>
                            <InspectionImageViewer
                                aircraftImage={aircraftImage}
                                inspectionItems={inspectionItems}
                                onPointsSelect={handlePointsSelect}
                            />
                        </Col>
                        <Col span={8}>
                            <InspectionItemList
                                inspectionItems={inspectionItems}
                                onRefresh={loadData}
                            />
                        </Col>
                    </Row>
                </Spin>
            </Card>

            <InspectionItemUploader
                visible={uploaderVisible}
                // 【重构修改】: 传递单个point对象
                selectedPoint={selectedPoint}
                aircraftImage={aircraftImage}
                onCancel={handleUploaderCancel}
                onSuccess={handleUploadSuccess}
                existingItem={selectedExistingItem}
            />
        </div>
    );
};

export default InspectionSubmitPage;
import React, { useState, useEffect } from 'react';
import { Card, Row, Col, message } from 'antd';
import type {AircraftImageType} from "../../../store/aircraft/types.ts";
import type {Point} from "../../../components/imageInnot/types.ts";
import AnnotationCanvas from "../../../components/imageInnot/AnnotationCanvas.tsx";
import ControlPanel from "../../../components/imageInnot/ControlPanel.tsx";
import PointsDataViewer from "../../../components/imageInnot/PointsDataViewer.tsx";


interface ImageAnnotationEditorProps {
    imageData: AircraftImageType;
    onSave: (points: Point[]) => void;
    readOnly?: boolean;
}

const ImageAnnotationEditor: React.FC<ImageAnnotationEditorProps> = ({
                                                                         imageData,
                                                                         onSave,
                                                                         readOnly = false
                                                                     }) => {
    const [points, setPoints] = useState<Point[]>([]);
    const [isAddMode, setIsAddMode] = useState(true);
    const [showCurve, setShowCurve] = useState(false);
    const [nextId, setNextId] = useState(1);

    useEffect(() => {
        // 加载现有点位数据
        if (imageData.image_json?.pointInfo) {
            const existingPoints = imageData.image_json.pointInfo;
            setPoints(existingPoints);
            setNextId(Math.max(...existingPoints.map(p => p.id), 0) + 1);
        } else {
            setPoints([]);
            setNextId(1);
        }
    }, [imageData]);

    const handleAddPoint = (point: Omit<Point, 'id'>) => {
        if (readOnly) return;

        const newPoint = { ...point, id: nextId };
        const newPoints = [...points, newPoint];
        setPoints(newPoints);
        setNextId(nextId + 1);
        onSave(newPoints);

    };

    const handleDeletePoint = (id: number) => {
        if (readOnly) return;

        // 1. 删除指定ID的点位
        const filteredPoints = points.filter(point => point.id !== id);

        // 2. 按删除后的顺序重新编号
        const reindexedPoints = filteredPoints.map((point, index) => ({
            ...point,
            id: index + 1
        }));

        // 3. 更新状态
        setPoints(reindexedPoints);
        setNextId(nextId - 1);
        onSave(reindexedPoints);

    };

    const handleModeChange = (addMode: boolean) => {
        if (readOnly) return;
        setIsAddMode(addMode);
    };

    const handleShowCurveChange = (show: boolean) => {
        setShowCurve(show);
    };

    return (
        <div className="image-annotation-editor">
            <Row gutter={16}>
                <Col span={16}>
                    <Card
                        title="图片标注"
                        style={{maxHeight:"100%", overflow:"auto"}}
                        className="annotation-card"
                        extra={
                            !readOnly && (
                                <ControlPanel
                                    isAddMode={isAddMode}
                                    showCurve={showCurve}
                                    onModeChange={handleModeChange}
                                    onShowCurveChange={handleShowCurveChange}
                                />
                            )
                        }
                    >
                        <AnnotationCanvas
                            image={imageData.image_json.fileInfo.download_url}
                            points={points}
                            isAddMode={isAddMode}
                            showCurve={showCurve}
                            onAddPoint={handleAddPoint}
                            onDeletePoint={handleDeletePoint}
                        />
                    </Card>
                </Col>

                <Col span={8}>
                    <PointsDataViewer points={points} />
                </Col>
            </Row>
        </div>
    );
};

export default ImageAnnotationEditor;
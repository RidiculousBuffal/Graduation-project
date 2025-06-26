import React, {useState} from 'react';
import {Card} from 'antd';
import AnnotationCanvas from './AnnotationCanvas';
import type {AircraftImageType} from "@/store/aircraft/types.ts";
import type {FlightImage} from "@/api/flightapi.ts";

interface ImagePreviewViewerProps {
    aircraft_image: Partial<FlightImage>
    aircraft_name: string
    showCurve?: boolean;
    showPointNumbers?: boolean;
    maxHeight?: number;
    title?: string;
}

const ImagePreviewViewer: React.FC<ImagePreviewViewerProps> = ({
                                                                   aircraft_image,
                                                                   showCurve = false,
                                                                   showPointNumbers = true,
                                                                   maxHeight = 600,
                                                                   aircraft_name,
                                                                   title
                                                               }) => {
    const [imageLoaded, setImageLoaded] = useState(false);

    // 只读模式的处理函数（不执行任何操作）
    const handleAddPoint = () => {
        // 预览模式不允许添加点位
    };

    const handleDeletePoint = () => {
        // 预览模式不允许删除点位
    };

    const points = aircraft_image.aircraft_image_json?.pointInfo || [];
    const imageUrl = aircraft_image.aircraft_image_json?.fileInfo?.download_url;

    if (!imageUrl) {
        return (
            <Card title={title || "底图预览"}>
                <div style={{
                    textAlign: 'center',
                    padding: '40px',
                    color: '#999'
                }}>
                    暂无图像数据
                </div>
            </Card>
        );
    }

    return (
        <Card
            title={title || "底图预览"}
            size="small"
            style={{width: '100%'}}
        >
            {/* 图像信息 */}
            <div style={{marginBottom: '12px'}}>
                <div style={{fontSize: '14px', color: '#666'}}>
                    <strong>图像名称:</strong> {aircraft_image.image_name}
                </div>
                {aircraft_name && (
                    <div style={{fontSize: '14px', color: '#666'}}>
                        <strong>飞机:</strong> {aircraft_name}
                    </div>
                )}
                <div style={{fontSize: '14px', color: '#666'}}>
                    <strong>点位数量:</strong> {points.length} 个
                </div>
            </div>

            {/* 图像预览区域 */}
            <div style={{
                display: 'flex',
                justifyContent: 'center',
                backgroundColor: '#fafafa',
                padding: '16px',
                borderRadius: '6px'
            }}>
                <AnnotationCanvas
                    image={imageUrl}
                    points={points}
                    isAddMode={false} // 预览模式不允许添加
                    showCurve={showCurve}
                    onAddPoint={handleAddPoint}
                    onDeletePoint={handleDeletePoint}
                />
            </div>
        </Card>
    );
};

export default ImagePreviewViewer;
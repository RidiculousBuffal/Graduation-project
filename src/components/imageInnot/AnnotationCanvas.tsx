import React, {useRef, useEffect, useState} from 'react';
import type{Point} from './types.ts';
import PointMarker from './PointMarker.tsx';
import CurveOverlay from './CurveOverlay.tsx';

interface AnnotationCanvasProps {
    image: string;
    points: Point[];
    isAddMode: boolean;
    showCurve: boolean;
    onAddPoint: (point: Omit<Point, 'id'>) => void;
    onDeletePoint: (id: number) => void;
}

const AnnotationCanvas: React.FC<AnnotationCanvasProps> = ({
                                                               image,
                                                               points,
                                                               isAddMode,
                                                               showCurve,
                                                               onAddPoint,
                                                               onDeletePoint,
                                                           }) => {
    const containerRef = useRef<HTMLDivElement>(null);
    const imageRef = useRef<HTMLImageElement>(null);
    const [imageLoaded, setImageLoaded] = useState(false);

    useEffect(() => {
        setImageLoaded(false);
    }, [image]);

    const handleImageLoad = () => {
        setImageLoaded(true);
    };

    const handleCanvasClick = (e: React.MouseEvent<HTMLDivElement>) => {
        if (!containerRef.current || !isAddMode || !imageLoaded) return;

        const rect = containerRef.current.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        // 检查点击是否在图片区域内
        if (x >= 0 && x <= rect.width && y >= 0 && y <= rect.height) {
            const newPoint = {
                x: (x / rect.width) * 100, // 转换为百分比
                y: (y / rect.height) * 100, // 转换为百分比
            };

            onAddPoint(newPoint);
        }
    };

    const canvasStyle: React.CSSProperties = {
        position: 'relative',
        display: 'inline-block',
        maxWidth: '100%',
        maxHeight: '600px',
        border: '2px solid #d9d9d9',
        borderRadius: '6px',
        overflow: 'hidden',
        cursor: isAddMode ? 'crosshair' : 'pointer'
    };

    const imageStyle: React.CSSProperties = {
        maxWidth: '100%',
        maxHeight: '600px',
        height: 'auto',
        display: 'block',
        userSelect: 'none'
    };

    return (
        <div
            className={`annotation-canvas ${isAddMode ? 'add-mode' : 'delete-mode'}`}
            ref={containerRef}
            onClick={handleCanvasClick}
            style={canvasStyle}
        >
            <img
                ref={imageRef}
                src={image}
                alt="标注图片"
                className="annotation-image"
                onLoad={handleImageLoad}
                draggable={false}
                style={imageStyle}
            />

            {/* 曲线覆盖层 */}
            {showCurve && points.length >= 2 && imageLoaded && (
                <CurveOverlay points={points}/>
            )}

            {/* 点位标记 */}
            {imageLoaded && points.map((point) => (
                <PointMarker
                    key={point.id}
                    point={point}
                    isAddMode={isAddMode}
                    onDelete={onDeletePoint}
                />
            ))}
        </div>
    );
};

export default AnnotationCanvas;
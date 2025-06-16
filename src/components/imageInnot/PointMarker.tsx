import React from 'react';
import type{ Point } from './types.ts';

interface PointMarkerProps {
    point: Point;
    isAddMode: boolean;
    onDelete: (id: number) => void;
}

const PointMarker: React.FC<PointMarkerProps> = ({ point, isAddMode, onDelete }) => {
    const handleClick = (e: React.MouseEvent) => {
        if (!isAddMode) {
            e.stopPropagation();
            onDelete(point.id);
        }
    };

    const markerStyle: React.CSSProperties = {
        position: 'absolute',
        left: `${point.x}%`,
        top: `${point.y}%`,
        transform: 'translate(-50%, -50%)',
        width: '24px',
        height: '24px',
        borderRadius: '50%',
        backgroundColor: isAddMode ? '#1890ff' : '#ff4d4f',
        color: 'white',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '12px',
        fontWeight: 'bold',
        cursor: isAddMode ? 'default' : 'pointer',
        border: '2px solid white',
        boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
        zIndex: 10,
        userSelect: 'none',
        transition: 'all 0.2s ease'
    };

    const hoverStyle: React.CSSProperties = {
        ...markerStyle,
        transform: 'translate(-50%, -50%) scale(1.1)'
    };

    const [isHovered, setIsHovered] = React.useState(false);

    return (
        <div
            className={`point-marker ${isAddMode ? 'add-mode' : 'delete-mode'}`}
            style={isHovered ? hoverStyle : markerStyle}
            onClick={handleClick}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            title={isAddMode ? `点位 ${point.id}` : `点击删除点位 ${point.id}`}
        >
            {point.id}
        </div>
    );
};

export default PointMarker;
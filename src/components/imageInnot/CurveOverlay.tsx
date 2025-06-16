
import React from 'react';
import type{ Point } from './types.ts';

interface CurveOverlayProps {
    points: Point[];
}

const CurveOverlay: React.FC<CurveOverlayProps> = ({ points }) => {
    // 生成平滑曲线路径
    const generateSmoothCurvePath = () => {
        if (points.length < 2) return '';

        // 按ID排序确保连接顺序正确
        const sortedPoints = [...points].sort((a, b) => a.id - b.id);

        // 从第一个点开始
        let path = `M ${sortedPoints[0].x} ${sortedPoints[0].y}`;

        // 使用三次贝塞尔曲线创建平滑路径
        for (let i = 0; i < sortedPoints.length - 1; i++) {
            const current = sortedPoints[i];
            const next = sortedPoints[i + 1];

            // 计算控制点，简单方法：两点间距离的1/3
            const dx = next.x - current.x;
            const dy = next.y - current.y;

            const ctrl1x = current.x + dx / 3;
            const ctrl1y = current.y + dy / 3;
            const ctrl2x = next.x - dx / 3;
            const ctrl2y = next.y - dy / 3;

            // 添加三次贝塞尔曲线命令
            path += ` C ${ctrl1x} ${ctrl1y}, ${ctrl2x} ${ctrl2y}, ${next.x} ${next.y}`;
        }

        return path;
    };

    const overlayStyle: React.CSSProperties = {
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
        zIndex: 5
    };

    return (
        <svg
            className="curve-overlay"
            style={overlayStyle}
            viewBox="0 0 100 100"
            preserveAspectRatio="none"
        >
            <path
                d={generateSmoothCurvePath()}
                fill="none"
                stroke="#ff3300"
                strokeWidth="0.5"
                strokeLinecap="round"
                strokeLinejoin="round"
                vectorEffect="non-scaling-stroke"
                opacity="0.8"
            />
        </svg>
    );
};

export default CurveOverlay;
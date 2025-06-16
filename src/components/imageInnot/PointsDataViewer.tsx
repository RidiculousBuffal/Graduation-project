import React from 'react';
import { Card } from 'antd';
import type{ Point } from './types.ts';
import {Highlighter} from "@lobehub/ui";

interface PointsDataViewerProps {
    points: Point[];
}

const PointsDataViewer: React.FC<PointsDataViewerProps> = ({ points }) => {
    const cardStyle: React.CSSProperties = {
        maxHeight: '100%',
        overflow: 'auto'
    };

    const preStyle: React.CSSProperties = {
        backgroundColor: '#f5f5f5',
        padding: '12px',
        borderRadius: '4px',
        fontSize: '12px',
        overflow:'auto',
        whiteSpace: 'pre-wrap',
        wordBreak: 'break-all'
    };

    return (
        <Card
            title={`点位数据 (${points.length}个点)`}
            size="small"
            className="points-data-viewer"
            style={cardStyle}
        >
            <pre className="points-json" style={preStyle}>
                <Highlighter language="json" fullFeatured={true}>
                    {JSON.stringify(points, null, 2)}
                </Highlighter>
            </pre>
        </Card>
    );
};

export default PointsDataViewer;
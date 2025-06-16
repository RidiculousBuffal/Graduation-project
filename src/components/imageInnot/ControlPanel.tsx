import React from 'react';
import { Button, Switch, Space } from 'antd';
import { PlusOutlined, DeleteOutlined, LineChartOutlined } from '@ant-design/icons';

interface ControlPanelProps {
    isAddMode: boolean;
    showCurve: boolean;
    onModeChange: (isAddMode: boolean) => void;
    onShowCurveChange: (showCurve: boolean) => void;
}

const ControlPanel: React.FC<ControlPanelProps> = ({
                                                       isAddMode,
                                                       showCurve,
                                                       onModeChange,
                                                       onShowCurveChange,
                                                   }) => {
    return (
        <div className="control-panel">
            <Space wrap>
                <div className="mode-buttons">
                    <Button
                        type={isAddMode ? 'primary' : 'default'}
                        icon={<PlusOutlined />}
                        onClick={() => onModeChange(true)}
                    >
                        添加点位
                    </Button>
                    <Button
                        type={!isAddMode ? 'primary' : 'default'}
                        danger={!isAddMode}
                        icon={<DeleteOutlined />}
                        onClick={() => onModeChange(false)}
                    >
                        删除模式
                    </Button>
                </div>

                <div className="curve-control">
                    <Space>
                        <LineChartOutlined />
                        <span>显示曲线</span>
                        <Switch
                            checked={showCurve}
                            onChange={onShowCurveChange}
                        />
                    </Space>
                </div>
            </Space>
        </div>
    );
};

export default ControlPanel;

import React, { useState } from 'react';
import { Card, List, Tag, Button, Space, Modal, Progress, Image, Descriptions, Badge, Divider, Empty } from 'antd';
import { EyeOutlined, CheckCircleOutlined, CloseCircleOutlined, ClockCircleOutlined, SyncOutlined } from '@ant-design/icons';
import type { InspectionItem, InspectionItemResult } from '@/store/inspectionItem/types';
import dayjs from 'dayjs';

interface InspectionItemListProps {
    inspectionItems: InspectionItem[];
    onRefresh: () => void;
}

const InspectionItemList: React.FC<InspectionItemListProps> = ({
                                                                   inspectionItems,
                                                                   onRefresh
                                                               }) => {
    const [selectedItem, setSelectedItem] = useState<InspectionItem | null>(null);
    const [resultModalVisible, setResultModalVisible] = useState(false);
    const [selectedResultIndex, setSelectedResultIndex] = useState<number>(0);

    // 获取检测状态
    const getItemStatus = (item: InspectionItem) => {
        if (!item.result || item.result.length === 0) {
            return { text: '待检测', color: 'default', icon: <ClockCircleOutlined /> };
        }

        const latestResult = item.result[item.result.length - 1];
        switch (latestResult.progress) {
            case 'pending':
                return { text: '待检测', color: 'default', icon: <ClockCircleOutlined /> };
            case 'detecting':
                return { text: '检测中', color: 'processing', icon: <SyncOutlined spin /> };
            case 'done':
                return {
                    text: latestResult.isPassed ? '检测通过' : '检测未通过',
                    color: latestResult.isPassed ? 'success' : 'error',
                    icon: latestResult.isPassed ? <CheckCircleOutlined /> : <CloseCircleOutlined />
                };
            default:
                return { text: '未知状态', color: 'default', icon: <ClockCircleOutlined /> };
        }
    };

    // 处理查看结果
    const handleViewResult = (item: InspectionItem) => {
        if (!item.result || item.result.length === 0) {
            Modal.info({
                title: '提示',
                content: '该条目还没有检测结果',
            });
            return;
        }
        setSelectedItem(item);
        setSelectedResultIndex(item.result.length - 1); // 默认显示最新结果
        setResultModalVisible(true);
    };

    // 渲染检测结果详情
    const renderResultDetails = (result: InspectionItemResult, index: number) => {
        return (
            <div key={index}>
                <Descriptions column={2} size="small" bordered>
                    <Descriptions.Item label="检测状态">
                        <Badge
                            status={result.progress === 'done' ? 'success' : result.progress === 'detecting' ? 'processing' : 'default'}
                            text={result.progress === 'done' ? '已完成' : result.progress === 'detecting' ? '检测中' : '待检测'}
                        />
                    </Descriptions.Item>
                    <Descriptions.Item label="检测结果">
                        <Tag color={result.isPassed ? 'success' : 'error'}>
                            {result.isPassed ? '通过' : '未通过'}
                        </Tag>
                    </Descriptions.Item>
                    <Descriptions.Item label="版本">v{result.version}</Descriptions.Item>
                    <Descriptions.Item label="检测框数量">
                        {result.resultImage?.boxes?.length || 0} 个
                    </Descriptions.Item>
                </Descriptions>

                {result.progress === 'detecting' && (
                    <div style={{ margin: '16px 0' }}>
                        <Progress percent={65} status="active" />
                        <div style={{ textAlign: 'center', marginTop: '8px', color: '#666' }}>
                            正在进行模型检测...
                        </div>
                    </div>
                )}

                {result.progress === 'done' && (
                    <>
                        <Divider>输入图像</Divider>
                        <div style={{ textAlign: 'center', marginBottom: '16px' }}>
                            <Image
                                src={result.inputImage.download_url}
                                alt="输入图像"
                                style={{ maxWidth: '100%', maxHeight: '300px' }}
                                placeholder={<div>加载中...</div>}
                            />
                            <div style={{ marginTop: '8px', fontSize: '12px', color: '#666' }}>
                                文件名: {result.inputImage.filename} | 大小: {(result.inputImage.size / 1024 / 1024).toFixed(2)}MB
                            </div>
                        </div>

                        <Divider>检测结果图像</Divider>
                        <div style={{ textAlign: 'center', marginBottom: '16px' }}>
                            <Image
                                src={result.resultImage.resultImage.download_url}
                                alt="检测结果图像"
                                style={{ maxWidth: '100%', maxHeight: '300px' }}
                                placeholder={<div>加载中...</div>}
                            />
                            <div style={{ marginTop: '8px', fontSize: '12px', color: '#666' }}>
                                结果图像: {result.resultImage.resultImage.filename}
                            </div>
                        </div>

                        {result.resultImage.boxes && result.resultImage.boxes.length > 0 && (
                            <>
                                <Divider>检测框详情</Divider>
                                <div style={{ maxHeight: '200px', overflowY: 'auto' }}>
                                    {result.resultImage.boxes.map((box, boxIndex) => (
                                        <Card key={boxIndex} size="small" style={{ marginBottom: '8px' }}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                                <div>
                                                    <Tag color="blue">{box.label}</Tag>
                                                    <span style={{ marginLeft: '8px' }}>
                                                        置信度: {(box.confidence * 100).toFixed(1)}%
                                                    </span>
                                                </div>
                                                <div style={{ fontSize: '12px', color: '#666' }}>
                                                    坐标: ({box.points.x1.toFixed(0)}, {box.points.y1.toFixed(0)}) - ({box.points.x2.toFixed(0)}, {box.points.y2.toFixed(0)})
                                                </div>
                                            </div>
                                        </Card>
                                    ))}
                                </div>
                            </>
                        )}

                        {(!result.resultImage.boxes || result.resultImage.boxes.length === 0) && (
                            <Empty
                                description="未检测到任何缺陷"
                                image={Empty.PRESENTED_IMAGE_SIMPLE}
                                style={{ margin: '16px 0' }}
                            />
                        )}
                    </>
                )}
            </div>
        );
    };

    return (
        <>
            <Card
                title={
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span>检测条目列表 ({inspectionItems.length})</span>
                        <Button size="small" onClick={onRefresh}>
                            刷新
                        </Button>
                    </div>
                }
                style={{ height: '600px', overflow: 'auto' }}
            >
                <List
                    dataSource={inspectionItems}
                    renderItem={(item) => {
                        const status = getItemStatus(item);
                        const latestResult = item.result && item.result.length > 0 ? item.result[item.result.length - 1] : null;

                        return (
                            <List.Item style={{ padding: '8px 0' }}>
                                <Card
                                    size="small"
                                    style={{ width: '100%' }}
                                    title={
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                            <span style={{ fontSize: '14px' }}>{item.item_name || '未命名条目'}</span>
                                            <Tag color={status.color} icon={status.icon}>
                                                {status.text}
                                            </Tag>
                                        </div>
                                    }
                                >
                                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '8px' }}>
                                        <div>模型: {item.model_name}</div>
                                        <div>创建时间: {dayjs(item.created_at).format('MM-DD HH:mm')}</div>
                                        <div>点位id:{item.item_point.point.id} x:{item.item_point.point.x} y:{item.item_point.point.y}</div>
                                        {item.description && (
                                            <div>描述: {item.description}</div>
                                        )}
                                        {latestResult && (
                                            <div>
                                                最新检测: v{latestResult.version} |
                                                {latestResult.resultImage?.boxes?.length || 0} 个检测框
                                            </div>
                                        )}
                                    </div>

                                    {latestResult?.progress === 'detecting' && (
                                        <div style={{ marginBottom: '8px' }}>
                                            <Progress percent={65} size="small" status="active" />
                                        </div>
                                    )}

                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                        <Space>
                                            <Button
                                                size="small"
                                                icon={<EyeOutlined />}
                                                onClick={() => handleViewResult(item)}
                                                disabled={!item.result || item.result.length === 0}
                                            >
                                                查看结果
                                            </Button>
                                        </Space>
                                        {item.result && item.result.length > 0 && (
                                            <span style={{ fontSize: '12px', color: '#666' }}>
                                                {item.result.length} 个检测版本
                                            </span>
                                        )}
                                    </div>
                                </Card>
                            </List.Item>
                        );
                    }}
                />
            </Card>

            {/* 检测结果详情模态框 */}
            <Modal
                title={
                    <div>
                        <span>{selectedItem?.item_name || '检测结果'}</span>
                        {selectedItem?.result && selectedItem.result.length > 1 && (
                            <div style={{ marginTop: '8px' }}>
                                <Space>
                                    <span style={{ fontSize: '12px', color: '#666' }}>版本:</span>
                                    {selectedItem.result.map((_, index) => (
                                        <Button
                                            key={index}
                                            size="small"
                                            type={index === selectedResultIndex ? 'primary' : 'default'}
                                            onClick={() => setSelectedResultIndex(index)}
                                        >
                                            v{selectedItem.result[index].version}
                                        </Button>
                                    ))}
                                </Space>
                            </div>
                        )}
                    </div>
                }
                open={resultModalVisible}
                onCancel={() => setResultModalVisible(false)}
                width={800}
                footer={null}
            >
                {selectedItem && selectedItem.result && selectedItem.result[selectedResultIndex] && (
                    renderResultDetails(selectedItem.result[selectedResultIndex], selectedResultIndex)
                )}
            </Modal>
        </>
    );
};

export default InspectionItemList;
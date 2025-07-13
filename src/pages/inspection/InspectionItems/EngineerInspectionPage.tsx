import React, { useState, useEffect } from 'react';
import { Card, Button, Table, message, Space, Tag } from 'antd';
import {  PlayCircleOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router';
import { InspectionRecordService } from '@/services/InspectionRecordService';
import { useInspectionStore } from '@/store/inspection/inspectionStore';
import { useCurrentStore } from '@/store/current/currentStore';
import type { InspectionRecordListType } from '@/store/inspection/types';
import type { ColumnsType } from 'antd/es/table';
import dayjs from 'dayjs';
import './InspectionItem.css'
const EngineerInspectionPage: React.FC = () => {
    const navigate = useNavigate();
    const { inspectionRecords, inspectionRecordsPagination } = useInspectionStore();
    const { setCurrentInspectionRecord } = useCurrentStore();

    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadMyInspectionRecords();
    }, []);

    const loadMyInspectionRecords = async () => {
        setLoading(true);
        try {
            await InspectionRecordService.getMyInspectionRecordList({});
        } catch (error) {
            message.error('获取检测条目失败');
        } finally {
            setLoading(false);
        }
    };

    const handleStartInspection = (record: InspectionRecordListType) => {
        setCurrentInspectionRecord(record);
        navigate('/console/inspection/inspection-submit');
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case '待开始':
                return 'default';
            case '进行中':
                return 'processing';
            case '已完成':
                return 'success';
            default:
                return 'default';
        }
    };

    const columns: ColumnsType<InspectionRecordListType> = [
        {
            title: '检测条目名称',
            dataIndex: 'inspection_name',
            key: 'inspection_name',
        },
        {
            title: '飞机',
            dataIndex: 'aircraft_name',
            key: 'aircraft_name',
        },
        {
            title: '进度',
            dataIndex: 'progress',
            key: 'progress',
            render: (progress: number) => `${progress}%`,
        },
        {
            title: '状态',
            dataIndex: 'status_name',
            key: 'status_name',
            render: (status: string) => (
                <Tag color={getStatusColor(status)}>{status}</Tag>
            ),
        },
        {
            title: '参考底图',
            dataIndex: 'reference_image_name',
            key: 'reference_image_name',
        },
        {
            title: '开始时间',
            dataIndex: 'start_time',
            key: 'start_time',
            render: (time: string) => time ? dayjs(time).format('YYYY-MM-DD HH:mm') : '-',
        },
        {
            title: '结束时间',
            dataIndex: 'end_time',
            key: 'end_time',
            render: (time: string) => time ? dayjs(time).format('YYYY-MM-DD HH:mm') : '-',
        },
        {
            title: '操作',
            key: 'actions',
            render: (_, record) => (
                <Space>
                    <Button
                        type="primary"
                        icon={<PlayCircleOutlined />}
                        onClick={() => handleStartInspection(record)}
                    >
                        去上传
                    </Button>
                </Space>
            ),
        },
    ];

    return (
        <div style={{ padding: '24px' }}>
            <Card title="我的检测条目">
                <Table
                    columns={columns}
                    dataSource={inspectionRecords}
                    loading={loading}
                    rowKey="inspection_id"
                    pagination={{
                        current: inspectionRecordsPagination.current_page,
                        pageSize: inspectionRecordsPagination.page_size,
                        total: inspectionRecordsPagination.total,
                        showSizeChanger: true,
                        showQuickJumper: true,
                        onChange: (page, pageSize) => {
                            useInspectionStore.getState().setInspectionRecordsPagination({
                                ...inspectionRecordsPagination,
                                current_page: page,
                                page_size: pageSize
                            });
                            loadMyInspectionRecords();
                        },
                    }}
                />
            </Card>
        </div>
    );
};

export default EngineerInspectionPage;
import React, { useState, useEffect } from 'react';
import { Card, Button, Table, Space, message, Modal } from 'antd';
import { EditOutlined, DeleteOutlined, EyeOutlined } from '@ant-design/icons';
import { InspectionRecordService } from '@/services/InspectionRecordService';
import { useInspectionStore } from '@/store/inspection/inspectionStore';
import type { InspectionRecordListType } from '@/store/inspection/types';
import type { ColumnsType } from 'antd/es/table';
import InspectionRecordSearchForm from './InspectionRecordSearchForm.tsx';
import InspectionRecordEditModal from './InspectionRecordEditModal';
import InspectionRecordDetailModal from './InspectionRecordDetailModal';
import dayjs from 'dayjs';

const InspectionRecordHall: React.FC = () => {
    const { inspectionRecords, inspectionRecordsPagination } = useInspectionStore();

    const [loading, setLoading] = useState(false);
    const [editModalVisible, setEditModalVisible] = useState(false);
    const [detailModalVisible, setDetailModalVisible] = useState(false);
    const [selectedRecord, setSelectedRecord] = useState<InspectionRecordListType | null>(null);

    // 初始化加载
    useEffect(() => {
        loadInspectionRecords({});
    }, []);

    // 加载检测条目列表
    const loadInspectionRecords = async (searchParams: any) => {
        setLoading(true);
        try {
            await InspectionRecordService.getInspectionRecordList(searchParams);
        } catch (error) {
            message.error('获取检测条目列表失败');
        } finally {
            setLoading(false);
        }
    };

    // 处理搜索
    const handleSearch = (searchParams: any) => {
        // 重置分页
        useInspectionStore.getState().setInspectionRecordsPagination({
            ...inspectionRecordsPagination,
            current_page: 1
        });
        loadInspectionRecords(searchParams);
    };

    // 处理编辑成功
    const handleEditSuccess = () => {
        setEditModalVisible(false);
        setSelectedRecord(null);
        loadInspectionRecords({});
        message.success('检测条目更新成功');
    };

    // 处理删除
    const handleDelete = async (record: InspectionRecordListType) => {
        Modal.confirm({
            title: '确认删除',
            content: `确定要删除检测条目 "${record.inspection_name}" 吗？`,
            okText: '确定',
            cancelText: '取消',
            okType: 'danger',
            onOk: async () => {
                try {
                    await InspectionRecordService.deleteInspectionRecord(record.inspection_id);
                    message.success('删除成功');
                    loadInspectionRecords({});
                } catch (error) {
                    message.error('删除失败');
                }
            }
        });
    };

    // 处理查看详情
    const handleViewDetail = (record: InspectionRecordListType) => {
        setSelectedRecord(record);
        setDetailModalVisible(true);
    };

    // 处理编辑
    const handleEdit = (record: InspectionRecordListType) => {
        setSelectedRecord(record);
        setEditModalVisible(true);
    };

    const columns: ColumnsType<InspectionRecordListType> = [
        {
            title: '检测条目名称',
            dataIndex: 'inspection_name',
            key: 'inspection_name',
        },
        {
            title: '任务ID',
            dataIndex: 'task_id',
            key: 'task_id',
            width: 120,
        },
        {
            title: '飞机',
            dataIndex: 'aircraft_name',
            key: 'aircraft_name',
        },
        {
            title: '执行工程师',
            dataIndex: 'executor_name',
            key: 'executor_name',
            render: (_, record) => {
                if (record.executor_name && record.executor_name.trim() !== '') {
                    return <>{record.executor_name}</>;
                } else if (record.executor_id && record.executor_id.trim() !== '') {
                    return <>{record.executor_id}</>;
                } else {
                    return <>-</>;
                }

            }
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
            fixed: 'right',
            width: 180,
            render: (_, record) => (
                <Space>
                    <Button
                        type="link"
                        size="small"
                        icon={<EyeOutlined />}
                        onClick={() => handleViewDetail(record)}
                    >
                        查看
                    </Button>
                    <Button
                        type="link"
                        size="small"
                        icon={<EditOutlined />}
                        onClick={() => handleEdit(record)}
                    >
                        编辑
                    </Button>
                    <Button
                        type="link"
                        size="small"
                        danger
                        icon={<DeleteOutlined />}
                        onClick={() => handleDelete(record)}
                    >
                        删除
                    </Button>
                </Space>
            ),
        },
    ];

    return (
        <div style={{ padding: '24px' }}>
            <Card>
                <InspectionRecordSearchForm onSearch={handleSearch} />

                <Table
                    columns={columns}
                    dataSource={inspectionRecords}
                    loading={loading}
                    rowKey="inspection_id"
                    scroll={{ x: 1500 }}
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
                            loadInspectionRecords({});
                        },
                    }}
                />
            </Card>

            {/* 编辑检测条目模态框 */}
            <InspectionRecordEditModal
                visible={editModalVisible}
                record={selectedRecord}
                onCancel={() => {
                    setEditModalVisible(false);
                    setSelectedRecord(null);
                }}
                onSuccess={handleEditSuccess}
            />

            {/* 查看详情模态框 */}
            <InspectionRecordDetailModal
                visible={detailModalVisible}
                record={selectedRecord}
                onCancel={() => {
                    setDetailModalVisible(false);
                    setSelectedRecord(null);
                }}
            />
        </div>
    );
};

export default InspectionRecordHall;
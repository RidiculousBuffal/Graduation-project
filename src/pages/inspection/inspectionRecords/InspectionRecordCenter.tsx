import React, {useEffect, useState} from 'react';
import {Button, Card, message, Modal, Space, Table} from 'antd';
import {DeleteOutlined, EditOutlined, EyeOutlined, PlusOutlined} from '@ant-design/icons';
import {useNavigate, useSearchParams} from 'react-router';
import {InspectionRecordService} from '@/services/InspectionRecordService.ts';
import {useInspectionStore} from '@/store/inspection/inspectionStore.ts';
import {useCurrentStore} from '@/store/current/currentStore.ts';
import type {InspectionRecordListType} from '@/store/inspection/types.ts';
import type {ColumnsType} from 'antd/es/table';
import InspectionRecordCreateModal from './InspectionRecordCreateModal';
import InspectionRecordEditModal from './InspectionRecordEditModal';
import InspectionRecordDetailModal from './InspectionRecordDetailModal';
import dayjs from 'dayjs';
import {TaskService} from "@/services/TaskService.ts";

const InspectionRecordCenter: React.FC = () => {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const taskId = useCurrentStore().currentTask?.task_id;

    const {inspectionRecords, inspectionRecordsPagination} = useInspectionStore();
    const {currentTask, setCurrentTask} = useCurrentStore();

    const [loading, setLoading] = useState(false);
    const [createModalVisible, setCreateModalVisible] = useState(false);
    const [editModalVisible, setEditModalVisible] = useState(false);
    const [detailModalVisible, setDetailModalVisible] = useState(false);
    const [selectedRecord, setSelectedRecord] = useState<InspectionRecordListType | null>(null);

    // 初始化加载
    useEffect(() => {
        if (taskId) {
            loadInspectionRecords();
            // 如果当前任务不存在或者不匹配，则获取任务信息
            if (!currentTask || currentTask.task_id !== taskId) {
                loadCurrentTask();
            }
        }
    }, [taskId]);

    // 加载当前任务信息
    const loadCurrentTask = async () => {
        if (!taskId) return;
        try {
            const taskData = await TaskService.getTaskById(taskId);
            if (taskData) {
                setCurrentTask(taskData);
            }
        } catch (error) {
            message.error('获取任务信息失败');
        }
    };

    // 加载检测条目列表
    const loadInspectionRecords = async () => {
        if (!taskId) return;

        setLoading(true);
        try {
            await InspectionRecordService.getInspectionRecordList({
                task_id: taskId
            });
        } catch (error) {
            message.error('获取检测条目列表失败');
        } finally {
            setLoading(false);
        }
    };

    // 处理新建成功
    const handleCreateSuccess = () => {
        setCreateModalVisible(false);
        loadInspectionRecords();
        message.success('检测条目创建成功');
    };

    // 处理编辑成功
    const handleEditSuccess = () => {
        setEditModalVisible(false);
        setSelectedRecord(null);
        loadInspectionRecords();
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
                    loadInspectionRecords();
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
            title: '执行工程师',
            dataIndex: 'executor_name',
            key: 'executor_name',
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
            render: (_, record) => (
                <Space>
                    <Button
                        type="link"
                        icon={<EyeOutlined/>}
                        onClick={() => handleViewDetail(record)}
                    >
                        查看
                    </Button>
                    <Button
                        type="link"
                        icon={<EditOutlined/>}
                        onClick={() => handleEdit(record)}
                    >
                        编辑
                    </Button>
                    <Button
                        type="link"
                        danger
                        icon={<DeleteOutlined/>}
                        onClick={() => handleDelete(record)}
                    >
                        删除
                    </Button>
                </Space>
            ),
        },
    ];

    if (!taskId) {
        return <div>任务ID缺失</div>;
    }

    return (
        <div style={{padding: '24px'}}>
            <Card
                title={
                    <div>
                        <h3>检测条目中心</h3>
                        {currentTask && (
                            <div style={{fontSize: '14px', color: '#666', marginTop: '8px'}}>
                                任务ID: {currentTask.task_id}
                            </div>
                        )}
                    </div>
                }
                extra={
                    <Button
                        type="primary"
                        icon={<PlusOutlined/>}
                        onClick={() => setCreateModalVisible(true)}
                    >
                        新建检测条目
                    </Button>
                }
            >
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
                            loadInspectionRecords();
                        },
                    }}
                />
            </Card>

            {/* 新建检测条目模态框 */}
            <InspectionRecordCreateModal
                visible={createModalVisible}
                taskId={taskId}
                onCancel={() => setCreateModalVisible(false)}
                onSuccess={handleCreateSuccess}
            />

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

export default InspectionRecordCenter;
import React, {useState, useEffect} from 'react';
import {Card, Button, Table, Space, message, Modal} from 'antd';
import {PlusOutlined, EditOutlined, DeleteOutlined, EyeOutlined} from '@ant-design/icons';
import {useNavigate} from 'react-router';
import {TaskService} from '@/services/TaskService.ts';
import {useTaskStore} from '@/store/task/taskStore.ts';
import {useCurrentStore} from '@/store/current/currentStore.ts';
import type {TaskListType} from '@/store/task/types.ts';
import type {ColumnsType} from 'antd/es/table';
import TaskSearchForm from './TaskSearchForm';
import TaskCreateModal from './TaskCreateModal';
import TaskEditModal from './TaskEditModal';
import dayjs from 'dayjs';
import {formatUTCToLocal} from "@/utils/dateUtils.ts";

const TaskCenter: React.FC = () => {
    const navigate = useNavigate();
    const {tasks, tasksPagination, setTasksPagination} = useTaskStore();
    const {setCurrentTask} = useCurrentStore();

    const [loading, setLoading] = useState(false);
    const [createModalVisible, setCreateModalVisible] = useState(false);
    const [editModalVisible, setEditModalVisible] = useState(false);
    const [selectedTask, setSelectedTask] = useState<TaskListType | null>(null);

    useEffect(() => {
        loadTasks();
    }, [tasksPagination.current_page, tasksPagination.page_size]);

    const loadTasks = async (searchParams = {}) => {
        setLoading(true);
        try {
            await TaskService.getTaskList(searchParams);
        } catch (error) {
            message.error('加载任务列表失败');
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = (searchParams: any) => {
        // 重置到第一页
        setTasksPagination({
            ...tasksPagination,
            current_page: 1
        });
        loadTasks(searchParams);
    };

    const handleEdit = (task: TaskListType) => {
        setSelectedTask(task);
        setEditModalVisible(true);
    };

    const handleDelete = (task: TaskListType) => {
        Modal.confirm({
            title: '确认删除',
            content: `确定要删除任务 "${task.task_id}" 吗？`,
            onOk: async () => {
                try {
                    await TaskService.deleteTask(task.task_id);
                    message.success('删除任务成功');
                    loadTasks();
                } catch (error) {
                    message.error('删除任务失败');
                }
            }
        });
    };

    const handleViewInspections = (task: TaskListType) => {
        setCurrentTask(task);
        navigate(`/console/inspection/records/${task.task_id}`);
    };

    const columns: ColumnsType<TaskListType> = [
        {
            title: '任务ID',
            dataIndex: 'task_id',
            key: 'task_id',
            width: 200,
        },
        {
            title: '飞机名称',
            dataIndex: 'aircraft_name',
            key: 'aircraft_name',
        },
        {
            title: '管理员',
            dataIndex: 'admin_name',
            key: 'admin_name',
        },
        {
            title: '任务状态',
            dataIndex: 'task_status',
            key: 'task_status',
        },
        {
            title: '预计开始时间',
            dataIndex: 'estimated_start',
            key: 'estimated_start',
            render: (text) => text ? formatUTCToLocal(text) : '-',
        },
        {
            title: '预计结束时间',
            dataIndex: 'estimated_end',
            key: 'estimated_end',
            render: (text) => text ? formatUTCToLocal(text) : '-',
        },
        {
            title: '实际开始时间',
            dataIndex: 'actual_start',
            key: 'actual_start',
            render: (text) => text ? formatUTCToLocal(text) : '-',
        },
        {
            title: '实际结束时间',
            dataIndex: 'actual_end',
            key: 'actual_end',
            render: (text) => text ? formatUTCToLocal(text) : '-',
        },
        {
            title: '创建时间',
            dataIndex: 'created_at',
            key: 'created_at',
            render: (text) => text ? formatUTCToLocal(text) : '-',
        },
        {
            title: '操作',
            key: 'action',
            width: 200,
            render: (_, record) => (
                <Space size="small">
                    <Button
                        type="primary"
                        size="small"
                        icon={<EyeOutlined/>}
                        onClick={() => handleViewInspections(record)}
                    >
                        检测条目
                    </Button>
                    <Button
                        size="small"
                        icon={<EditOutlined/>}
                        onClick={() => handleEdit(record)}
                    >
                        编辑
                    </Button>
                    <Button
                        size="small"
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

    return (
        <div style={{padding: '24px'}}>
            <Card>
                <div style={{marginBottom: 16}}>
                    <Space>
                        <Button
                            type="primary"
                            icon={<PlusOutlined/>}
                            onClick={() => setCreateModalVisible(true)}
                        >
                            新建任务
                        </Button>
                    </Space>
                </div>

                <TaskSearchForm onSearch={handleSearch}/>

                <Table
                    columns={columns}
                    dataSource={tasks}
                    rowKey="task_id"
                    loading={loading}
                    pagination={{
                        current: tasksPagination.current_page,
                        pageSize: tasksPagination.page_size,
                        total: tasksPagination.total,
                        showSizeChanger: true,
                        showQuickJumper: true,
                        showTotal: (total) => `共 ${total} 条记录`,
                        onChange: (page, pageSize) => {
                            setTasksPagination({
                                ...tasksPagination,
                                current_page: page,
                                page_size: pageSize || 10
                            });
                        }
                    }}
                />
            </Card>

            <TaskCreateModal
                visible={createModalVisible}
                onCancel={() => setCreateModalVisible(false)}
                onSuccess={() => {
                    setCreateModalVisible(false);
                    loadTasks();
                }}
            />

            <TaskEditModal
                visible={editModalVisible}
                task={selectedTask}
                onCancel={() => {
                    setEditModalVisible(false);
                    setSelectedTask(null);
                }}
                onSuccess={() => {
                    setEditModalVisible(false);
                    setSelectedTask(null);
                    loadTasks();
                }}
            />
        </div>
    );
};

export default TaskCenter;
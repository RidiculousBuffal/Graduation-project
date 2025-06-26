import React, {useState, useEffect} from 'react';
import {Modal, Form, DatePicker, Select, message} from 'antd';
import {TaskService} from '@/services/TaskService';
import {DictionaryService} from '@/services/DictionaryService';
import {TASK_STATUS} from '@/consts/dictionary';
import FlightSelector from '../../components/selectors/FlightSelector.tsx';
import type {TaskListType} from '@/store/task/types';

import type {dictionaryType} from '@/store/dictionary/type';
import dayjs from 'dayjs';

interface TaskEditModalProps {
    visible: boolean;
    task: TaskListType | null;
    onCancel: () => void;
    onSuccess: () => void;
}

const TaskEditModal: React.FC<TaskEditModalProps> = ({
                                                         visible,
                                                         task,
                                                         onCancel,
                                                         onSuccess
                                                     }) => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const [taskStatusOptions, setTaskStatusOptions] = useState<dictionaryType[]>([]);

    useEffect(() => {
        loadTaskStatusOptions();
    }, []);

    useEffect(() => {
        if (visible && task) {
            form.setFieldsValue({
                flight_id: task.flight_id,
                estimated_start: task.estimated_start ? dayjs(task.estimated_start) : null,
                estimated_end: task.estimated_end ? dayjs(task.estimated_end) : null,
                actual_start: task.actual_start ? dayjs(task.actual_start) : null,
                actual_end: task.actual_end ? dayjs(task.actual_end) : null,
                task_status: task.task_status,
            });
        }
    }, [visible, task, form]);

    const loadTaskStatusOptions = async () => {
        try {
            const result = await DictionaryService.getChildrenByParentId(TASK_STATUS);
            if (result) {
                setTaskStatusOptions(result);
            }
        } catch (error) {
            console.error('加载任务状态选项失败:', error);
        }
    };

    const handleSubmit = async () => {
        if (!task) return;

        try {
            const values = await form.validateFields();
            setLoading(true);

            const payload = {
                task_id: task.task_id,
                flight_id: values.flight_id,
                estimated_start: values.estimated_start.toISOString(),
                estimated_end: values.estimated_end.toISOString(),
                actual_start: values.actual_start ? values.actual_start.toISOString() : '',
                actual_end: values.actual_end ? values.actual_end.toISOString() : '',
                task_status: values.task_status || '',
            };

            await TaskService.updateTask(payload);
            message.success('更新任务成功');
            onSuccess();
        } catch (error) {
            message.error('更新任务失败');
        } finally {
            setLoading(false);
        }
    };

    const handleCancel = () => {
        form.resetFields();
        onCancel();
    };

    return (
        <Modal
            title="编辑任务"
            open={visible}
            onOk={handleSubmit}
            onCancel={handleCancel}
            confirmLoading={loading}
            width={600}
            destroyOnClose
        >
            <Form
                form={form}
                layout="vertical"
                preserve={false}
            >
                <Form.Item
                    label="航班"
                    name="flight_id"
                    rules={[{required: true, message: '请选择航班'}]}
                >
                    <FlightSelector
                        placeholder="请输入航班ID或飞机名称搜索"
                    />
                </Form.Item>

                <Form.Item
                    label="预计开始时间"
                    name="estimated_start"
                    rules={[{required: true, message: '请选择预计开始时间'}]}
                >
                    <DatePicker
                        showTime
                        style={{width: '100%'}}
                        format="YYYY-MM-DD HH:mm:ss"
                        placeholder="请选择预计开始时间"
                    />
                </Form.Item>

                <Form.Item
                    label="预计结束时间"
                    name="estimated_end"
                    rules={[
                        {required: true, message: '请选择预计结束时间'},
                        ({getFieldValue}) => ({
                            validator(_, value) {
                                const startTime = getFieldValue('estimated_start');
                                if (!value || !startTime || value.isAfter(startTime)) {
                                    return Promise.resolve();
                                }
                                return Promise.reject(new Error('结束时间必须晚于开始时间'));
                            },
                        }),
                    ]}
                >
                    <DatePicker
                        showTime
                        style={{width: '100%'}}
                        format="YYYY-MM-DD HH:mm:ss"
                        placeholder="请选择预计结束时间"
                    />
                </Form.Item>

                <Form.Item
                    label="实际开始时间"
                    name="actual_start"
                >
                    <DatePicker
                        showTime
                        style={{width: '100%'}}
                        format="YYYY-MM-DD HH:mm:ss"
                        placeholder="请选择实际开始时间"
                    />
                </Form.Item>

                <Form.Item
                    label="实际结束时间"
                    name="actual_end"
                    rules={[
                        ({getFieldValue}) => ({
                            validator(_, value) {
                                const actualStartTime = getFieldValue('actual_start');
                                if (!value || !actualStartTime || value.isAfter(actualStartTime)) {
                                    return Promise.resolve();
                                }
                                return Promise.reject(new Error('实际结束时间必须晚于实际开始时间'));
                            },
                        }),
                    ]}
                >
                    <DatePicker
                        showTime
                        style={{width: '100%'}}
                        format="YYYY-MM-DD HH:mm:ss"
                        placeholder="请选择实际结束时间"
                    />
                </Form.Item>

                <Form.Item
                    label="任务状态"
                    name="task_status"
                >
                    <Select placeholder="请选择任务状态" allowClear>
                        {taskStatusOptions.map(option => (
                            <Select.Option key={option.dict_key} value={option.dict_key}>
                                {option.dict_name}
                            </Select.Option>
                        ))}
                    </Select>
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default TaskEditModal;
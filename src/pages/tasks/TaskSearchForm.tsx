import React, {useState, useEffect} from 'react';
import {Form, Input, Select, DatePicker, Button, Space, Row, Col} from 'antd';
import {SearchOutlined, ReloadOutlined} from '@ant-design/icons';
import {DictionaryService} from '@/services/DictionaryService';
import {TASK_STATUS} from '@/consts/dictionary';
import type {dictionaryType} from '@/store/dictionary/type';

const {RangePicker} = DatePicker;

interface TaskSearchFormProps {
    onSearch: (values: any) => void;
}

const TaskSearchForm: React.FC<TaskSearchFormProps> = ({onSearch}) => {
    const [form] = Form.useForm();
    const [taskStatusOptions, setTaskStatusOptions] = useState<dictionaryType[]>([]);

    useEffect(() => {
        loadTaskStatusOptions();
    }, []);

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

    const handleSearch = () => {
        const values = form.getFieldsValue();

        // 处理时间范围
        const searchParams = {
            ...values,
            estimated_start_from: values.estimated_start_range?.[0]?.toISOString(),
            estimated_start_to: values.estimated_start_range?.[1]?.toISOString(),
            estimated_end_from: values.estimated_end_range?.[0]?.toISOString(),
            estimated_end_to: values.estimated_end_range?.[1]?.toISOString(),
            actual_start_from: values.actual_start_range?.[0]?.toISOString(),
            actual_start_to: values.actual_start_range?.[1]?.toISOString(),
            actual_end_from: values.actual_end_range?.[0]?.toISOString(),
            actual_end_to: values.actual_end_range?.[1]?.toISOString(),
        };

        // 移除范围字段
        delete searchParams.estimated_start_range;
        delete searchParams.estimated_end_range;
        delete searchParams.actual_start_range;
        delete searchParams.actual_end_range;

        onSearch(searchParams);
    };

    const handleReset = () => {
        form.resetFields();
        onSearch({});
    };

    return (
        <div style={{marginBottom: 16, padding: 16, backgroundColor: '#fafafa', borderRadius: 6}}>
            <Form form={form} layout="vertical">
                <Row gutter={16}>
                    <Col span={6}>
                        <Form.Item label="航班ID" name="flight_id">
                            <Input placeholder="请输入航班ID" allowClear/>
                        </Form.Item>
                    </Col>
                    <Col span={6}>
                        <Form.Item label="飞机名称" name="aircraft_name">
                            <Input placeholder="请输入飞机名称" allowClear/>
                        </Form.Item>
                    </Col>
                    <Col span={6}>
                        <Form.Item label="管理员姓名" name="admin_name">
                            <Input placeholder="请输入管理员姓名" allowClear/>
                        </Form.Item>
                    </Col>
                    <Col span={6}>
                        <Form.Item label="任务状态" name="task_status">
                            <Select placeholder="请选择任务状态" allowClear>
                                {taskStatusOptions.map(option => (
                                    <Select.Option key={option.dict_key} value={option.dict_key}>
                                        {option.dict_name}
                                    </Select.Option>
                                ))}
                            </Select>
                        </Form.Item>
                    </Col>
                </Row>

                <Row gutter={16}>
                    <Col span={12}>
                        <Form.Item label="预计开始时间" name="estimated_start_range">
                            <RangePicker
                                showTime
                                style={{width: '100%'}}
                                format="YYYY-MM-DD HH:mm:ss"
                            />
                        </Form.Item>
                    </Col>
                    <Col span={12}>
                        <Form.Item label="预计结束时间" name="estimated_end_range">
                            <RangePicker
                                showTime
                                style={{width: '100%'}}
                                format="YYYY-MM-DD HH:mm:ss"
                            />
                        </Form.Item>
                    </Col>
                </Row>

                <Row gutter={16}>
                    <Col span={12}>
                        <Form.Item label="实际开始时间" name="actual_start_range">
                            <RangePicker
                                showTime
                                style={{width: '100%'}}
                                format="YYYY-MM-DD HH:mm:ss"
                            />
                        </Form.Item>
                    </Col>
                    <Col span={12}>
                        <Form.Item label="实际结束时间" name="actual_end_range">
                            <RangePicker
                                showTime
                                style={{width: '100%'}}
                                format="YYYY-MM-DD HH:mm:ss"
                            />
                        </Form.Item>
                    </Col>
                </Row>

                <Row>
                    <Col span={24}>
                        <Space>
                            <Button type="primary" icon={<SearchOutlined/>} onClick={handleSearch}>
                                搜索
                            </Button>
                            <Button icon={<ReloadOutlined/>} onClick={handleReset}>
                                重置
                            </Button>
                        </Space>
                    </Col>
                </Row>
            </Form>
        </div>
    );
};

export default TaskSearchForm;
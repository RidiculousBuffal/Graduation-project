import React, {useState, useEffect} from 'react';
import {Form, Input, Select, DatePicker, Button, Space, Row, Col} from 'antd';
import {SearchOutlined, ReloadOutlined} from '@ant-design/icons';
import {DictionaryService} from '@/services/DictionaryService';
import {INSPECTION_STATUS} from '@/consts/dictionary';
import EngineerSelector from '@/components/selectors/EngineerSelector';
import type {dictionaryType} from '@/store/dictionary/type';

const {RangePicker} = DatePicker;

interface InspectionRecordSearchFormProps {
    onSearch: (values: any) => void;
}

const InspectionRecordSearchForm: React.FC<InspectionRecordSearchFormProps> = ({onSearch}) => {
    const [form] = Form.useForm();
    const [statusOptions, setStatusOptions] = useState<dictionaryType[]>([]);

    useEffect(() => {
        loadStatusOptions();
    }, []);

    const loadStatusOptions = async () => {
        try {
            const result = await DictionaryService.getChildrenByParentId(INSPECTION_STATUS);
            if (result) {
                setStatusOptions(result);
            }
        } catch (error) {
            console.error('加载状态选项失败:', error);
        }
    };

    const handleSearch = () => {
        const values = form.getFieldsValue();

        // 处理时间范围
        const searchParams: any = {...values};

        if (values.start_time_range) {
            searchParams.start_time_from = values.start_time_range[0]?.toISOString();
            searchParams.start_time_to = values.start_time_range[1]?.toISOString();
        }

        if (values.end_time_range) {
            searchParams.end_time_from = values.end_time_range[0]?.toISOString();
            searchParams.end_time_to = values.end_time_range[1]?.toISOString();
        }

        // 删除范围字段
        delete searchParams.start_time_range;
        delete searchParams.end_time_range;

        onSearch(searchParams);
    };

    const handleReset = () => {
        form.resetFields();
        onSearch({});
    };

    return (
        <Form
            form={form}
            layout="vertical"
            style={{marginBottom: '16px'}}
        >
            <Row gutter={16}>
                <Col span={6}>
                    <Form.Item label="任务ID" name="task_id">
                        <Input placeholder="请输入任务ID"/>
                    </Form.Item>
                </Col>
                <Col span={6}>
                    <Form.Item label="检测条目名称" name="inspection_name">
                        <Input placeholder="请输入检测条目名称"/>
                    </Form.Item>
                </Col>
                <Col span={6}>
                    <Form.Item label="执行工程师" name="executor_id">
                        <EngineerSelector placeholder="请选择执行工程师"/>
                    </Form.Item>
                </Col>
                <Col span={6}>
                    <Form.Item label="检测状态" name="inspection_status">
                        <Select placeholder="请选择检测状态" allowClear>
                            {statusOptions.map(option => (
                                <Select.Option key={option.dict_key} value={option.dict_key}>
                                    {option.dict_name}
                                </Select.Option>
                            ))}
                        </Select>
                    </Form.Item>
                </Col>
            </Row>

            <Row gutter={16}>
                <Col span={6}>
                    <Form.Item label="飞机ID" name="aircraft_id">
                        <Input placeholder="请输入飞机ID"/>
                    </Form.Item>
                </Col>
                <Col span={6}>
                    <Form.Item label="航班ID" name="flight_id">
                        <Input placeholder="请输入航班ID"/>
                    </Form.Item>
                </Col>
                <Col span={6}>
                    <Form.Item label="开始时间范围" name="start_time_range">
                        <RangePicker
                            showTime
                            style={{width: '100%'}}
                            placeholder={['开始时间', '结束时间']}
                        />
                    </Form.Item>
                </Col>
                <Col span={6}>
                    <Form.Item label="结束时间范围" name="end_time_range">
                        <RangePicker
                            showTime
                            style={{width: '100%'}}
                            placeholder={['开始时间', '结束时间']}
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
    );
};

export default InspectionRecordSearchForm;
import React, { useState, useEffect } from 'react';
import { Modal, Form, Input, Select, message } from 'antd';
import { InspectionRecordService } from '@/services/InspectionRecordService';
import { DictionaryService } from '@/services/DictionaryService';
import { INSPECTION_STATUS } from '@/consts/dictionary';
import EngineerSelector from '@/components/selectors/EngineerSelector';
import type { InspectionRecordListType } from '@/store/inspection/types';
import type { dictionaryType } from '@/store/dictionary/type';

interface InspectionRecordEditModalProps {
    visible: boolean;
    record: InspectionRecordListType | null;
    onCancel: () => void;
    onSuccess: () => void;
}

const InspectionRecordEditModal: React.FC<InspectionRecordEditModalProps> = ({
                                                                                 visible,
                                                                                 record,
                                                                                 onCancel,
                                                                                 onSuccess
                                                                             }) => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const [statusOptions, setStatusOptions] = useState<dictionaryType[]>([]);

    useEffect(() => {
        if (visible && record) {
            form.setFieldsValue({
                inspection_name: record.inspection_name,
                executor_id: record.executor_id,
                inspection_status: record.inspection_status,
            });
            loadStatusOptions();
        }
    }, [visible, record, form]);

    const loadStatusOptions = async () => {
        try {
            const result = await DictionaryService.getChildrenByParentId(INSPECTION_STATUS);
            if (result) {
                setStatusOptions(result);
            }
        } catch (error) {
            message.error('加载状态选项失败');
        }
    };

    const handleSubmit = async () => {
        if (!record) return;

        try {
            const values = await form.validateFields();
            setLoading(true);

            await InspectionRecordService.updateInspectionRecord({
                inspection_id: record.inspection_id,
                inspection_name: values.inspection_name,
                executor_id: values.executor_id,
                inspection_status: values.inspection_status,
            });

            onSuccess();
        } catch (error) {
            message.error('更新检测条目失败');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Modal
            title="编辑检测条目"
            open={visible}
            onCancel={onCancel}
            onOk={handleSubmit}
            confirmLoading={loading}
            width={600}
            destroyOnHidden={true}
        >
            <Form
                form={form}
                layout="vertical"
                requiredMark={false}
            >
                <Form.Item
                    label="检测条目名称"
                    name="inspection_name"
                    rules={[
                        { required: true, message: '请输入检测条目名称' },
                        { max: 100, message: '名称长度不能超过100个字符' }
                    ]}
                >
                    <Input placeholder="请输入检测条目名称" />
                </Form.Item>

                <Form.Item
                    label="执行工程师"
                    name="executor_id"
                    rules={[{ required: true, message: '请选择执行工程师' }]}
                >
                    <EngineerSelector />
                </Form.Item>

                <Form.Item
                    label="检测状态"
                    name="inspection_status"
                    rules={[{ required: true, message: '请选择检测状态' }]}
                >
                    <Select placeholder="请选择检测状态">
                        {statusOptions.map(option => (
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

export default InspectionRecordEditModal;
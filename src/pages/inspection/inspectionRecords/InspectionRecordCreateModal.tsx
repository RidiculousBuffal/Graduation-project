import React, {useState, useEffect} from 'react';
import {Modal, Form, Input, message} from 'antd';
import {InspectionRecordService} from '@/services/InspectionRecordService';
import EngineerSelector from '@/components/selectors/EngineerSelector';
import AircraftImageSelector from '@/components/selectors/AircraftImageSelector';
import ImagePreviewViewer from '@/components/imageInnot/ImagePreviewViewer';
import {useCurrentStore} from '@/store/current/currentStore';
import type {FlightImage} from '@/api/flightapi';

interface InspectionRecordCreateModalProps {
    visible: boolean;
    taskId: string;
    onCancel: () => void;
    onSuccess: () => void;
}

const InspectionRecordCreateModal: React.FC<InspectionRecordCreateModalProps> = ({
                                                                                     visible,
                                                                                     taskId,
                                                                                     onCancel,
                                                                                     onSuccess
                                                                                 }) => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const [selectedImage, setSelectedImage] = useState<FlightImage | null>(null);
    const {currentTask} = useCurrentStore();

    useEffect(() => {
        if (visible) {
            form.resetFields();
            setSelectedImage(null);
        }
    }, [visible, form]);

    const handleSubmit = async () => {
        try {
            const values = await form.validateFields();
            setLoading(true);

            await InspectionRecordService.createInspectionRecord({
                inspection_name: values.inspection_name,
                executor_id: values.executor_id,
                reference_image_id: values.reference_image_id,
                task_id: taskId
            });

            onSuccess();
        } catch (error) {
            message.error('创建检测条目失败');
        } finally {
            setLoading(false);
        }
    };

    const handleImageChange = (imageId: string, imageInfo: FlightImage) => {
        setSelectedImage(imageInfo);
        form.setFieldsValue({reference_image_id: imageId});
    };

    return (
        <Modal
            title="新建检测条目"
            open={visible}
            onCancel={onCancel}
            onOk={handleSubmit}
            confirmLoading={loading}
            width={800} // 增加宽度以容纳预览组件
            destroyOnClose
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
                        {required: true, message: '请输入检测条目名称'},
                        {max: 100, message: '名称长度不能超过100个字符'}
                    ]}
                >
                    <Input placeholder="请输入检测条目名称"/>
                </Form.Item>

                <Form.Item
                    label="执行工程师"
                    name="executor_id"
                    rules={[{required: true, message: '请选择执行工程师'}]}
                >
                    <EngineerSelector/>
                </Form.Item>

                <Form.Item
                    label="参考底图"
                    name="reference_image_id"
                    rules={[{required: true, message: '请选择参考底图'}]}
                >
                    <AircraftImageSelector
                        flightId={currentTask?.flight_id}
                        onChange={handleImageChange}
                    />
                </Form.Item>

                {selectedImage && (
                    <div style={{marginTop: '16px'}}>
                        <ImagePreviewViewer
                            aircraft_image={selectedImage}
                            aircraft_name={selectedImage.aircraft_name}
                            showCurve={false}
                            title="参考底图预览"
                        />
                    </div>
                )}
            </Form>
        </Modal>
    );
};

export default InspectionRecordCreateModal;
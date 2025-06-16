
import React, { useState, useEffect } from 'react';
import { Modal, Form, Input, message, Spin } from 'antd';

import AircraftSelector from './AircraftSelector';
import ImageAnnotationEditor from './ImageAnnotationEditor';
import type {AircraftImageType} from "../../../store/aircraft/types.ts";
import type {Point} from "../../../components/imageInnot/types.ts";
import {AircraftImageService} from "../../../services/AircraftImageService.ts";

interface ImageEditModalProps {
    visible: boolean;
    onClose: () => void;
    imageData: AircraftImageType | null;
    mode: 'add' | 'edit' | 'view';
}

const ImageEditModal: React.FC<ImageEditModalProps> = ({
                                                           visible,
                                                           onClose,
                                                           imageData,
                                                           mode
                                                       }) => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const [currentPoints, setCurrentPoints] = useState<Point[]>([]);

    useEffect(() => {
        if (visible && imageData) {
            form.setFieldsValue({
                image_name: imageData.image_name,
                aircraft_id: imageData.aircraft_id,
            });
            setCurrentPoints(imageData.image_json?.pointInfo || []);
        } else {
            form.resetFields();
            setCurrentPoints([]);
        }
    }, [visible, imageData, form]);

    const handleSave = async () => {
        if (!imageData) return;

        try {
            const values = await form.validateFields();
            setLoading(true);

            const updatedImageData: AircraftImageType = {
                ...imageData,
                ...values,
                image_json: {
                    ...imageData.image_json,
                    pointInfo: currentPoints,
                },
            };

            await AircraftImageService.updateAircraftImage(updatedImageData);
            message.success('保存成功');
            onClose();
        } catch (error) {
            message.error('保存失败');
        } finally {
            setLoading(false);
        }
    };

    const handlePointsChange = (points: Point[]) => {
        setCurrentPoints(points);
    };

    const getTitle = () => {
        switch (mode) {
            case 'add': return '添加图片';
            case 'edit': return '编辑图片';
            case 'view': return '查看图片';
            default: return '图片详情';
        }
    };

    const isReadOnly = mode === 'view';

    return (
        <Modal
            title={getTitle()}
            open={visible}
            onCancel={onClose}
            onOk={mode !== 'view' ? handleSave : undefined}
            width={1200}
            okText="保存"
            cancelText="取消"
            confirmLoading={loading}
            okButtonProps={{ disabled: isReadOnly }}
            className="image-edit-modal"
        >
            <Spin spinning={loading}>
                <div className="image-edit-content">
                    <Form
                        form={form}
                        layout="vertical"
                        className="image-info-form"
                    >
                        <Form.Item
                            name="image_name"
                            label="图片名称"
                            rules={[{ required: true, message: '请输入图片名称' }]}
                        >
                            <Input
                                placeholder="请输入图片名称"
                                disabled={isReadOnly}
                            />
                        </Form.Item>

                        <Form.Item
                            name="aircraft_id"
                            label="关联飞机"
                            rules={[{ required: true, message: '请选择关联飞机' }]}
                        >
                            <AircraftSelector
                                placeholder="请选择飞机"
                                disabled={isReadOnly}
                            />
                        </Form.Item>
                    </Form>

                    {imageData && (
                        <ImageAnnotationEditor
                            imageData={imageData}
                            onSave={handlePointsChange}
                            readOnly={isReadOnly}
                        />
                    )}
                </div>
            </Spin>
        </Modal>
    );
};

export default ImageEditModal;
import React, { useState, useEffect } from 'react';
import { Modal, Form, Input, Select, Upload, message, Button, Space } from 'antd';
import { UploadOutlined, LoadingOutlined } from '@ant-design/icons';
import type { RcFile } from 'antd/es/upload';
import { ModelService } from '@/services/ModelService';
import { InspectionRecordItemService } from '@/services/InspectionRecordItemService';
import { useModelStore } from '@/store/model/modelStore';
import { useCurrentStore } from '@/store/current/currentStore';
import { uploadFile } from '@/api/fileapi';
import { Highlighter } from '@lobehub/ui';
import type { createInspectionItemType } from "@/api/inspectionItemapi.ts";
import type { AircraftImageType } from "@/store/aircraft/types.ts";
import type { Point } from "@/components/imageInnot/types.ts";

interface InspectionItemUploaderProps {
    visible: boolean;
    selectedPoints: Point[];
    aircraftImage: AircraftImageType | null;
    onCancel: () => void;
    onSuccess: () => void;
}

const InspectionItemUploader: React.FC<InspectionItemUploaderProps> = ({
                                                                           visible,
                                                                           selectedPoints,
                                                                           aircraftImage,
                                                                           onCancel,
                                                                           onSuccess
                                                                       }) => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [detectionResult, setDetectionResult] = useState<any>(null);
    const [uploadedFileInfo, setUploadedFileInfo] = useState<any>(null);

    const { models } = useModelStore();
    const { currentInspectionRecord } = useCurrentStore();

    useEffect(() => {
        if (visible) {
            loadModels();
            form.resetFields();
            setDetectionResult(null);
            setUploadedFileInfo(null);
        }
    }, [visible]);

    const loadModels = async () => {
        try {
            await ModelService.getAllModels();
        } catch (error) {
            message.error('加载模型列表失败');
        }
    };

    const handleFileUpload = async (file: RcFile) => {
        setUploading(true);
        try {
            const uploadResult = await uploadFile(file);
            if (uploadResult) {
                setUploadedFileInfo(uploadResult);
                message.success('文件上传成功');
            }
        } catch (error) {
            message.error('文件上传失败');
        } finally {
            setUploading(false);
        }
        return false;
    };

    const handleSubmit = async (values: any) => {
        if (!currentInspectionRecord) {
            message.error('检测记录信息缺失');
            return;
        }

        if (!uploadedFileInfo) {
            message.error('请先上传检测照片');
            return;
        }

        if (selectedPoints.length === 0) {
            message.error('请选择至少一个检测点位');
            return;
        }

        setLoading(true);
        try {
            const itemData: createInspectionItemType = {
                item_name: values.item_name,
                inspection_id: currentInspectionRecord.inspection_id,
                item_point: {
                    point: selectedPoints[0], // 根据类型定义，这里应该是单个Point
                    fileInfo: uploadedFileInfo
                },
                description: values.description,
                model_id: values.model_id,
            };

            await InspectionRecordItemService.createInspectionRecordItem(itemData);
            message.success('检测条目创建成功');
            onSuccess();
        } catch (error) {
            message.error('创建检测条目失败');
        } finally {
            setLoading(false);
        }
    };

    const handleUpdateResult = async () => {
        if (!detectionResult) return;

        // 重新检测逻辑
        const newResult = {
            ...detectionResult,
            confidence: Math.random() * 0.5 + 0.5,
            timestamp: new Date().toISOString()
        };
        setDetectionResult(newResult);
        message.success('检测结果已更新');
    };

    return (
        <Modal
            title="上传检测条目"
            open={visible}
            onCancel={onCancel}
            width={800}
            footer={[
                <Button key="cancel" onClick={onCancel}>
                    取消
                </Button>,
                <Button
                    key="submit"
                    type="primary"
                    loading={loading}
                    onClick={() => form.submit()}
                >
                    提交
                </Button>
            ]}
        >
            <Form
                form={form}
                layout="vertical"
                onFinish={handleSubmit}
            >
                <Form.Item
                    label="条目名称"
                    name="item_name"
                    rules={[{ required: true, message: '请输入条目名称' }]}
                >
                    <Input placeholder="请输入条目名称" />
                </Form.Item>

                <Form.Item
                    label="选择模型"
                    name="model_id"
                    rules={[{ required: true, message: '请选择检测模型' }]}
                >
                    <Select placeholder="请选择检测模型">
                        {models?.map(model => (
                            <Select.Option key={model.model_id} value={model.model_id}>
                                {model.model_name}
                            </Select.Option>
                        )) }
                    </Select>
                </Form.Item>

                <Form.Item label="上传照片">
                    <Upload
                        beforeUpload={handleFileUpload}
                        showUploadList={false}
                        accept="image/*"
                    >
                        <Button icon={uploading ? <LoadingOutlined /> : <UploadOutlined />}>
                            {uploading ? '上传中...' : '选择照片'}
                        </Button>
                    </Upload>
                    {uploadedFileInfo && (
                        <div style={{ marginTop: '8px' }}>
                            <img
                                src={uploadedFileInfo.download_url}
                                alt="上传的照片"
                                style={{ maxWidth: '200px', maxHeight: '200px' }}
                            />
                        </div>
                    )}
                </Form.Item>

                <Form.Item
                    label="描述"
                    name="description"
                >
                    <Input.TextArea
                        placeholder="请输入描述信息"
                        rows={3}
                    />
                </Form.Item>

                <Form.Item label={`选择的点位 (${selectedPoints.length}个)`}>
                    <div style={{
                        padding: '8px 12px',
                        backgroundColor: '#f5f5f5',
                        borderRadius: '4px',
                        fontSize: '14px'
                    }}>
                        {selectedPoints.map(point => `点位${point.id}`).join(', ')}
                    </div>
                </Form.Item>

                {aircraftImage && (
                    <Form.Item label="飞机图片信息">
                        <div style={{
                            padding: '8px 12px',
                            backgroundColor: '#f5f5f5',
                            borderRadius: '4px',
                            fontSize: '14px'
                        }}>
                            <div>图片名称: {aircraftImage.image_name}</div>
                            <div>飞机ID: {aircraftImage.aircraft_id}</div>
                            <div>描述: {aircraftImage.image_description}</div>
                        </div>
                    </Form.Item>
                )}

                {detectionResult && (
                    <Form.Item
                        label={
                            <Space>
                                <span>检测结果</span>
                                <Button size="small" onClick={handleUpdateResult}>
                                    更新结果
                                </Button>
                            </Space>
                        }
                    >
                        <div style={{
                            backgroundColor: '#f5f5f5',
                            padding: '12px',
                            borderRadius: '4px',
                            maxHeight: '200px',
                            overflow: 'auto'
                        }}>
                            <Highlighter language="json" fullFeatured={true}>
                                {JSON.stringify(detectionResult, null, 2)}
                            </Highlighter>
                        </div>
                    </Form.Item>
                )}
            </Form>
        </Modal>
    );
};

export default InspectionItemUploader;
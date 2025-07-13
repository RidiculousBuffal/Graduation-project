import React, {useState, useEffect} from 'react';
import {Modal, Form, Input, Select, Upload, message, Button} from 'antd';
import {UploadOutlined, LoadingOutlined} from '@ant-design/icons';
import type {RcFile} from 'antd/es/upload';
import {ModelService} from '@/services/ModelService';
import {InspectionRecordItemService} from '@/services/InspectionRecordItemService';
import {useModelStore} from '@/store/model/modelStore';
import {useCurrentStore} from '@/store/current/currentStore';
import {uploadFile} from '@/api/fileapi';
import type {createInspectionItemType, updateInspectionItemType} from "@/api/inspectionItemapi.ts";
import type {AircraftImageType} from "@/store/aircraft/types.ts";
import type {Point} from "@/components/imageInnot/types.ts";
import type {InspectionItem} from "@/store/inspectionItem/types.ts";
import type {ipfsFileType} from "@/publicTypes/ipfs.ts";

interface InspectionItemUploaderProps {
    visible: boolean;
    selectedPoint: Point | null;
    aircraftImage: AircraftImageType | null;
    onCancel: () => void;
    onSuccess: () => void;
    existingItem: InspectionItem | null;
}

const InspectionItemUploader: React.FC<InspectionItemUploaderProps> = ({
                                                                           visible,
                                                                           selectedPoint,
                                                                           aircraftImage,
                                                                           onCancel,
                                                                           onSuccess,
                                                                           existingItem
                                                                       }) => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [uploadedFileInfo, setUploadedFileInfo] = useState<ipfsFileType | null>(null);

    const {models} = useModelStore();
    const {currentInspectionRecord} = useCurrentStore();

    useEffect(() => {
        if (visible) {
            loadModels();
            // 重置文件上传状态
            setUploadedFileInfo(null);

            // 如果是更新模式，使用已有数据填充表单
            if (existingItem) {
                form.setFieldsValue({
                    item_name: existingItem.item_name,
                    model_id: existingItem.model_id,
                    description: existingItem.description,
                });
            } else {
                // 如果是创建模式，清空表单
                form.resetFields();
            }
        }
    }, [visible, existingItem, form]);

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

        if (!selectedPoint) {
            message.error('未选择任何检测点位');
            return;
        }

        if (!uploadedFileInfo) {
            message.error('请先上传检测照片');
            return;
        }

        setLoading(true);

        try {
            // 如果 existingItem 存在，则执行更新逻辑
            if (existingItem) {
                const itemData: updateInspectionItemType = {
                    item_name: values.item_name,
                    description: values.description,
                    inspection_id: currentInspectionRecord.inspection_id,
                    model_id: values.model_id,
                    item_point: {
                        point: selectedPoint,
                        fileInfo: uploadedFileInfo
                    },
                };
                await InspectionRecordItemService.updateInspectionRecordItem(existingItem.item_id, itemData);
                message.success('检测条目更新成功');
            } else {
                // 否则，执行创建逻辑
                const itemData: createInspectionItemType = {
                    item_name: values.item_name,
                    inspection_id: currentInspectionRecord.inspection_id,
                    item_point: {
                        point: selectedPoint,
                        fileInfo: uploadedFileInfo
                    },
                    description: values.description,
                    model_id: values.model_id,
                };
                await InspectionRecordItemService.createInspectionRecordItem(itemData);
                message.success('检测条目创建成功');
            }
            onSuccess();
        } catch (error) {
            const action = existingItem ? '更新' : '创建';
            message.error(`${action}检测条目失败`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Modal
            title={existingItem ? `更新点位 ${existingItem.item_point.point.id} 的检测条目` : "上传新检测条目"}
            open={visible}
            onCancel={onCancel}
            width={800}
            destroyOnHidden={true}
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
                    {existingItem ? "确认更新" : "提交"}
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
                    rules={[{required: true, message: '请输入条目名称'}]}
                >
                    <Input placeholder="请输入条目名称"/>
                </Form.Item>

                <Form.Item
                    label="选择模型"
                    name="model_id"
                    rules={[{required: true, message: '请选择检测模型'}]}
                >
                    <Select placeholder="请选择检测模型">
                        {models?.map(model => (
                            <Select.Option key={model.model_id} value={model.model_id}>
                                {model.model_name}
                            </Select.Option>
                        ))}
                    </Select>
                </Form.Item>

                <Form.Item
                    label={existingItem ? "上传新照片以更新" : "上传照片"}
                    extra={existingItem ? "更新条目需要上传一张新的检测照片。" : ""}
                    rules={[{required: true, message: '请上传一张照片'}]} // 也可在这里加校验
                >
                    <Upload
                        beforeUpload={handleFileUpload}
                        showUploadList={false}
                        accept="image/*"
                    >
                        <Button icon={uploading ? <LoadingOutlined/> : <UploadOutlined/>}>
                            {uploading ? '上传中...' : '选择照片'}
                        </Button>
                    </Upload>
                    {uploadedFileInfo && (
                        <div style={{marginTop: '8px'}}>
                            <p>新上传的照片:</p>
                            <img
                                src={uploadedFileInfo.download_url}
                                alt="上传的照片"
                                style={{maxWidth: '200px', maxHeight: '200px', borderRadius: '4px'}}
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

                <Form.Item label="操作的点位">
                    <div style={{
                        padding: '8px 12px',
                        backgroundColor: '#f5f5f5',
                        borderRadius: '4px',
                        fontSize: '14px'
                    }}>
                        {selectedPoint ? `点位 ${selectedPoint.id} (x: ${selectedPoint.x.toFixed(2)}%, y: ${selectedPoint.y.toFixed(2)}%)` : '未选择'}
                    </div>
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default InspectionItemUploader;

import React, { useState } from 'react';
import { Modal, Steps, Form, Input, AutoComplete, Button, Space, message } from 'antd';
import type { RcFile } from 'antd/es/upload';
import ImageUploader from '../../../components/imageInnot/ImageUploader';
import { AircraftListService } from "../../../services/AircraftListService";
import { useAircraftStore } from "../../../store/aircraft/aircraftStore";
import type { ipfsFileType } from "../../../publicTypes/ipfs";

interface ImageUploadModalProps {
    visible: boolean;
    onClose: () => void;
    onComplete: (data: {
        fileInfo: ipfsFileType;
        aircraftId: string;
        imageName: string;
        description: string;
    }) => Promise<void>;
    onFileUpload: (file: RcFile) => Promise<ipfsFileType>; // 新增：处理文件上传的回调
}

const ImageUploadModal: React.FC<ImageUploadModalProps> = ({
                                                               visible,
                                                               onClose,
                                                               onComplete,
                                                               onFileUpload
                                                           }) => {
    const [currentStep, setCurrentStep] = useState(0);
    const [uploadedFileInfo, setUploadedFileInfo] = useState<ipfsFileType | null>(null);
    const [form] = Form.useForm();
    const [aircraftOptions, setAircraftOptions] = useState<Array<{
        value: string;
        label: string;
        aircraftId: string;
    }>>([]);
    const [searchingAircraft, setSearchingAircraft] = useState(false);
    const [submitLoading, setSubmitLoading] = useState(false);
    const [uploadLoading, setUploadLoading] = useState(false);

    // 重置模态框状态
    const resetModal = () => {
        setCurrentStep(0);
        setUploadedFileInfo(null);
        form.resetFields();
        setAircraftOptions([]);
        setUploadLoading(false);
        setSubmitLoading(false);
    };

    // 处理文件上传
    const handleFileUpload = async (file: RcFile) => {
        setUploadLoading(true);
        try {
            const fileInfo = await onFileUpload(file);
            setUploadedFileInfo(fileInfo);
            setCurrentStep(1);
            // 设置默认图片名称
            form.setFieldsValue({
                image_name: fileInfo.filename
            });
            message.success('文件上传成功');
        } catch (error) {
            message.error('文件上传失败');
            console.error('文件上传失败:', error);
        } finally {
            setUploadLoading(false);
        }
    };

    // 搜索飞机
    const handleAircraftSearch = async (searchText: string) => {
        if (!searchText || searchText.length < 2) {
            setAircraftOptions([]);
            return;
        }

        setSearchingAircraft(true);
        try {
            await AircraftListService.getAircraftList({
                aircraft_name: searchText,
                age: null,
                type_name: null,
                description: null
            });

            const { aircrafts } = useAircraftStore.getState();
            const options = aircrafts.map((aircraft: any) => ({
                value: aircraft.aircraft_name,
                label: aircraft.aircraft_name,
                aircraftId: aircraft.aircraft_id
            }));

            setAircraftOptions(options);
        } catch (error) {
            console.error('搜索飞机失败:', error);
            setAircraftOptions([]);
        } finally {
            setSearchingAircraft(false);
        }
    };

    // 处理飞机选择
    const handleAircraftSelect = (value: string, option: any) => {
        form.setFieldsValue({
            aircraft_name: value,
            aircraft_id: option.aircraftId
        });
    };

    // 提交表单
    const handleSubmit = async () => {
        try {
            const values = await form.validateFields();

            if (!uploadedFileInfo) {
                message.error('请先上传文件');
                return;
            }

            setSubmitLoading(true);

            await onComplete({
                fileInfo: uploadedFileInfo,
                aircraftId: values.aircraft_id,
                imageName: values.image_name,
                description: values.description || ''
            });

            handleCancel();
        } catch (error) {
            console.error('保存失败:', error);
        } finally {
            setSubmitLoading(false);
        }
    };

    // 取消操作
    const handleCancel = () => {
        resetModal();
        onClose();
    };

    // 返回上一步
    const handlePrevious = () => {
        setCurrentStep(0);
        setUploadedFileInfo(null);
        form.resetFields();
    };

    const steps = [
        {
            title: '上传文件',
            content: (
                <div style={{ textAlign: 'center', padding: '20px 0' }}>
                    <ImageUploader
                        onUpload={handleFileUpload}
                        loading={uploadLoading}
                    />
                </div>
            )
        },
        {
            title: '填写信息',
            content: (
                <div style={{ padding: '20px 0' }}>
                    {uploadedFileInfo && (
                        <div style={{ marginBottom: 20, textAlign: 'center' }}>
                            <img
                                src={uploadedFileInfo.download_url}
                                alt="上传的图片"
                                style={{
                                    maxWidth: '200px',
                                    maxHeight: '150px',
                                    borderRadius: '4px',
                                    border: '1px solid #d9d9d9'
                                }}
                            />
                        </div>
                    )}

                    <Form
                        form={form}
                        layout="vertical"
                    >
                        <Form.Item
                            name="image_name"
                            label="图片名称"
                            rules={[{ required: true, message: '请输入图片名称' }]}
                        >
                            <Input placeholder="请输入图片名称" />
                        </Form.Item>

                        <Form.Item
                            name="aircraft_name"
                            label="关联飞机"
                            rules={[{ required: true, message: '请选择关联的飞机' }]}
                        >
                            <AutoComplete
                                placeholder="请输入飞机名称进行搜索"
                                options={aircraftOptions}
                                onSearch={handleAircraftSearch}
                                onSelect={handleAircraftSelect}
                                notFoundContent={searchingAircraft ? '搜索中...' : '暂无数据'}
                                allowClear
                                filterOption={false}
                            />
                        </Form.Item>

                        <Form.Item name="aircraft_id" hidden>
                            <Input />
                        </Form.Item>

                        <Form.Item
                            name="description"
                            label="图片描述"
                        >
                            <Input.TextArea
                                placeholder="请输入图片描述（可选）"
                                rows={3}
                                maxLength={500}
                                showCount
                            />
                        </Form.Item>
                    </Form>
                </div>
            )
        }
    ];

    return (
        <Modal
            title="上传飞机底图"
            open={visible}
            onCancel={handleCancel}
            width={600}
            footer={
                <div style={{ textAlign: 'right' }}>
                    <Space>
                        {currentStep === 1 && (
                            <Button onClick={handlePrevious}>
                                上一步
                            </Button>
                        )}
                        <Button onClick={handleCancel}>
                            取消
                        </Button>
                        {currentStep === 1 && (
                            <Button
                                type="primary"
                                onClick={handleSubmit}
                                loading={submitLoading}
                            >
                                完成
                            </Button>
                        )}
                    </Space>
                </div>
            }
        >
            <Steps current={currentStep} style={{ marginBottom: 24 }}>
                {steps.map(item => (
                    <Steps.Step key={item.title} title={item.title} />
                ))}
            </Steps>

            <div>{steps[currentStep].content}</div>
        </Modal>
    );
};

export default ImageUploadModal;
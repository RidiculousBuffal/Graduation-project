import React from 'react';
import {Upload, message} from 'antd';
import {InboxOutlined} from '@ant-design/icons';
import type {UploadProps} from 'antd';
import type {RcFile} from "antd/es/upload";

const {Dragger} = Upload;

interface ImageUploaderProps {
    onUpload: (file: RcFile) => Promise<void>;
    loading?: boolean;
}

const ImageUploader: React.FC<ImageUploaderProps> = ({onUpload, loading = false}) => {
    const uploadProps: UploadProps = {
        name: 'file',
        multiple: false,
        accept: 'image/*',
        showUploadList: false,
        beforeUpload: async (file) => {
            const isImage = file.type.startsWith('image/');
            if (!isImage) {
                message.error('只能上传图片文件！');
                return false;
            }

            const isLt10M = file.size / 1024 / 1024 < 10;
            if (!isLt10M) {
                message.error('图片大小不能超过10MB！');
                return false;
            }

            await onUpload(file);
            return false; // 阻止默认上传行为
        },
    };

    return (
        <Dragger {...uploadProps} className="image-uploader" disabled={loading}>
            <p className="ant-upload-drag-icon">
                <InboxOutlined/>
            </p>
            <p className="ant-upload-text">
                {loading ? '上传中...' : '点击或拖拽图片到此处上传'}
            </p>
            <p className="ant-upload-hint">
                支持单个图片文件，大小不超过10MB
            </p>
        </Dragger>
    );
};

export default ImageUploader;
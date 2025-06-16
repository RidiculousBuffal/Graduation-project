import React, {useState, useEffect} from 'react';
import {Card, message} from 'antd';
import type {RcFile} from 'antd/es/upload';
import ImageUploadModal from './ImageUploadModal';
import ImageEditModal from './ImageEditModal';
import type {AircraftImageType} from '../../../store/aircraft/types';
import {AircraftImageService} from "../../../services/AircraftImageService";
import {uploadFile} from "../../../api/fileapi";
import type {ipfsFileType} from "../../../publicTypes/ipfs";
import './AircraftImageManager.css';
import ImageList from "./ImageList.tsx";

const AircraftImageManager: React.FC = () => {
    const [uploadModalVisible, setUploadModalVisible] = useState(false);
    const [editModalVisible, setEditModalVisible] = useState(false);
    const [currentImage, setCurrentImage] = useState<AircraftImageType | null>(null);
    const [modalMode, setModalMode] = useState<'add' | 'edit' | 'view'>('add');

    useEffect(() => {
        handleSearch({});
    }, []);

    const handleSearch = async (searchParams: any) => {
        try {
            await AircraftImageService.getAircraftImageList(searchParams);
        } catch (error) {
            message.error('搜索失败');
        }
    };

    // 处理文件上传
    const handleFileUpload = async (file: RcFile): Promise<ipfsFileType> => {
        try {
            const uploadResult = await uploadFile(file);
            if (uploadResult?.success) {
                return uploadResult;
            } else {
                throw new Error('上传失败');
            }
        } catch (error) {
            console.error('文件上传失败:', error);
            throw error;
        }
    };

    // 处理完整的上传流程（包括文件上传和信息填写）
    const handleUploadComplete = async (data: {
        fileInfo: ipfsFileType;
        aircraftId: string;
        imageName: string;
        description: string;
    }) => {
        try {
            // 创建新的图片记录
            const newImage: Partial<AircraftImageType> = {
                image_name: data.imageName,
                aircraft_id: data.aircraftId,
                image_json: {
                    fileInfo: data.fileInfo,
                    pointInfo: [],
                },
                // 如果有描述字段，可以添加到这里
                image_description: data.description
            };

            const createResult = await AircraftImageService.createAircraftImage(newImage);
            if (createResult) {
                message.success('保存成功');
                setUploadModalVisible(false);
                // 刷新列表
                handleSearch({});
            } else {
                message.error('保存失败');
                throw new Error('保存失败');
            }
        } catch (error) {
            message.error('保存失败');
            throw error; // 重新抛出错误，让模态框能够处理
        }
    };

    const handleEdit = (image: AircraftImageType, mode: 'edit' | 'view' = 'edit') => {
        setCurrentImage(image);
        setModalMode(mode);
        setEditModalVisible(true);
    };

    const handleEditModalClose = () => {
        setEditModalVisible(false);
        setCurrentImage(null);
        // 刷新列表
        handleSearch({});
    };

    return (
        <div className="aircraft-image-manager">
            <Card title="飞机底图管理" className="manager-card">
                <ImageList onEdit={handleEdit} onCreate={() => {
                    setUploadModalVisible(true)
                }}></ImageList>
            </Card>

            {/* 上传模态框 */}
            <ImageUploadModal
                visible={uploadModalVisible}
                onClose={() => setUploadModalVisible(false)}
                onComplete={handleUploadComplete}
                onFileUpload={handleFileUpload}
            />

            {/* 编辑模态框 */}
            <ImageEditModal
                visible={editModalVisible}
                onClose={handleEditModalClose}
                imageData={currentImage}
                mode={modalMode}
            />
        </div>
    );
};

export default AircraftImageManager;
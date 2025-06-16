import React, {useState, useEffect} from 'react';
import {

    Table,
    Button,
    Space,
    Image,
    Tag,
    Popconfirm,
    message,
    Pagination
} from 'antd';
import {
    EditOutlined,
    DeleteOutlined,
    EyeOutlined,

} from '@ant-design/icons';
import type {ColumnsType} from 'antd/es/table';

import SearchBar from './SearchBar';
import type {AircraftImageType} from "../../../store/aircraft/types.ts";
import {useAircraftStore} from "../../../store/aircraft/aircraftStore.ts";
import {AircraftImageService} from "../../../services/AircraftImageService.ts";


interface ImageListProps {
    onEdit: (image: AircraftImageType, mode?: 'edit' | 'view') => void;
    onCreate: () => void
}

const ImageList: React.FC<ImageListProps> = ({
                                                 onEdit, onCreate

                                             }) => {
    const {images, aircraftImagePagination} = useAircraftStore();
    const [loading, setLoading] = useState(false);
    const [searchLoading, setSearchLoading] = useState(false);

    useEffect(() => {
        handleSearch({})
    }, []);

    const handleSearch = async (searchParams: any) => {
        setSearchLoading(true);
        try {
            await AircraftImageService.getAircraftImageList(searchParams);
        } catch (error) {
            message.error('搜索失败');
        } finally {
            setSearchLoading(false);
        }
    };

    const handleDelete = async (imageId: string) => {
        setLoading(true);
        try {
            await AircraftImageService.deleteAircraftImage(imageId);
            await AircraftImageService.getAircraftImageList({})
            message.success('删除成功');
        } catch (error) {
            message.error('删除失败');
        } finally {
            setLoading(false);
        }
    };

    const handlePageChange = (page: number, pageSize: number) => {
        const newPagination = {
            ...aircraftImagePagination,
            page,
            page_size: pageSize
        };
        useAircraftStore.getState().setAircraftImagePagination(newPagination);
        handleSearch({});
    };

    const columns: ColumnsType<AircraftImageType> = [
        {
            title: '预览',
            key: 'preview',
            width: 80,
            render: (_, record) => {
                const url = record.image_json?.fileInfo?.download_url;

                return <Image
                    width={50}
                    height={50}
                    src={url}
                    placeholder="加载中..."
                    style={{objectFit: 'cover', borderRadius: 4}}
                />
            },
        },
        {
            title: '图片名称',
            dataIndex: 'image_name',
            key: 'image_name',
            ellipsis: true,
        },
        {
            title: '关联飞机',
            dataIndex: 'aircraft_name',
            key: 'aircraft_name',
            render: (name: string) => name ? <Tag color="blue">{name}</Tag> : <Tag>未关联</Tag>,
        },
        {
            title: '标注点数',
            key: 'points_count',
            render: (_, record) => (
                <Tag color="green">
                    {record.image_json?.pointInfo?.length || 0} 个点
                </Tag>
            ),
        },
        {
            title: '操作',
            key: 'action',

            render: (_, record) => (
                <Space size="small">
                    <Button
                        type="text"
                        size="small"
                        icon={<EyeOutlined/>}
                        onClick={() => onEdit(record, 'view')}
                    >
                        查看
                    </Button>
                    <Button
                        type="text"
                        size="small"
                        icon={<EditOutlined/>}
                        onClick={() => onEdit(record, 'edit')}
                    >
                        编辑
                    </Button>
                    <Popconfirm
                        title="确定要删除这张图片吗？"
                        onConfirm={() => handleDelete(record.image_id)}
                        okText="确定"
                        cancelText="取消"
                    >
                        <Button
                            type="text"
                            size="small"
                            danger
                            icon={<DeleteOutlined/>}
                        >
                            删除
                        </Button>
                    </Popconfirm>
                </Space>
            ),
        },
    ];

    return (
        <div className="image-list-content">
            <div className="list-header">
                <SearchBar
                    onSearch={handleSearch}
                    onReset={() => handleSearch({})}
                    loading={searchLoading}
                    onCreate={onCreate}
                />
            </div>

            <Table
                columns={columns}
                dataSource={images}
                rowKey="image_id"
                loading={loading || searchLoading}
                pagination={false}
                size="middle"
            />

            <div className="list-pagination">
                <Pagination
                    current={aircraftImagePagination.current_page}
                    pageSize={aircraftImagePagination.page_size}
                    total={aircraftImagePagination.total}
                    showSizeChanger
                    showQuickJumper
                    showTotal={(total, range) =>
                        `第 ${range[0]}-${range[1]} 条/共 ${total} 条`
                    }
                    onChange={handlePageChange}
                    onShowSizeChange={handlePageChange}
                />
            </div>
        </div>
    );
};

export default ImageList;
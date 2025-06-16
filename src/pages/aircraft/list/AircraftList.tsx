import React, {useEffect, useState} from 'react';
import {Table, Button, Modal, message, Space, Tag} from 'antd';
import {PlusOutlined, EditOutlined, DeleteOutlined, EyeOutlined} from '@ant-design/icons';
import type {ColumnsType} from 'antd/es/table';
import AircraftCreateModal from './AircraftCreateModal';
import AircraftEditModal from './AircraftEditModal';
import AircraftDetailModal from './AircraftDetailModal';
import AircraftSearchBar from './AircraftSearchBar';
import './Aircraft.css';
import {useAircraftStore} from '../../../store/aircraft/aircraftStore';
import type {AircraftArrayType, aircraftType_} from '../../../store/aircraft/types';
import {AircraftListService} from '../../../services/AircraftListService';

interface SearchParams {
    aircraft_name?: string;
    age?: number;
    type_name?: string;
}

const Aircraft: React.FC = () => {
    const {aircrafts, aircraftPagination, setAircraftPagination} = useAircraftStore();
    const [loading, setLoading] = useState(false);
    const [createModalVisible, setCreateModalVisible] = useState(false);
    const [editModalVisible, setEditModalVisible] = useState(false);
    const [detailModalVisible, setDetailModalVisible] = useState(false);
    const [selectedAircraft, setSelectedAircraft] = useState<AircraftArrayType[0] | null>(null);
    const [searchParams, setSearchParams] = useState<SearchParams>({});

    useEffect(() => {
        loadAircrafts().then(r => r);
    }, [aircraftPagination.current_page, aircraftPagination.page_size]);

    const loadAircrafts = async (searchData?: SearchParams) => {
        setLoading(true);
        try {
            const params = searchData || searchParams;
            await AircraftListService.getAircraftList({
                aircraft_name: params.aircraft_name || null,
                age: params.age || null,
                type_name: params.type_name || null,
                description: null
            });
        } catch (error) {
            message.error('加载飞机列表失败');
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = async (params: SearchParams) => {
        setSearchParams(params);
        // 重置到第一页
        setAircraftPagination({...aircraftPagination, current_page: 1});
        await loadAircrafts(params);
    };

    const handleReset = async () => {
        setSearchParams({});
        setAircraftPagination({...aircraftPagination, current_page: 1});
        await loadAircrafts({});
    };

    const handleView = (aircraft: AircraftArrayType[0]) => {
        setSelectedAircraft(aircraft);
        setDetailModalVisible(true);
    };

    const handleEdit = (aircraft: AircraftArrayType[0]) => {
        setSelectedAircraft(aircraft);
        setEditModalVisible(true);
    };

    const handleDelete = (aircraft: AircraftArrayType[0]) => {
        Modal.confirm({
            title: '确认删除',
            content: `确定要删除飞机 "${aircraft.aircraft_name}" 吗？`,
            okText: '确认',
            cancelText: '取消',
            onOk: async () => {
                try {
                    await AircraftListService.deleteAircraft(aircraft as aircraftType_);
                    message.success('删除成功');
                    await loadAircrafts();
                } catch (error) {
                    message.error('删除失败');
                }
            },
        });
    };

    const handleCreateSuccess = async () => {
        setCreateModalVisible(false);
        message.success('创建成功');
        await loadAircrafts();
    };

    const handleEditSuccess = async () => {
        setEditModalVisible(false);
        setSelectedAircraft(null);
        message.success('更新成功');
        await loadAircrafts();
    };

    const columns: ColumnsType<AircraftArrayType[0]> = [
        {
            title: '飞机名称',
            dataIndex: 'aircraft_name',
            key: 'aircraft_name',
            width: 200,
            fixed: 'left',
            render: (text: string) => (
                <span style={{fontWeight: 600, color: '#1f2937'}}>{text}</span>
            ),
        },
        {
            title: '机龄',
            dataIndex: 'age',
            key: 'age',
            width: 100,
            render: (age: number) => <Tag color="blue">{age}年</Tag>,
            sorter: (a, b) => a.age - b.age,
        },
        {
            title: '飞机类型',
            dataIndex: 'type_name',
            key: 'type_name',
            width: 180,
            render: (text: string) => (
                <span style={{color: '#3b82f6', fontWeight: 500}}>{text}</span>
            ),
        },
        {
            title: '类型描述',
            dataIndex: 'description',
            key: 'description',
            width: 300,
            ellipsis: {showTitle: false},
            render: (text: string) => (
                <span title={text} style={{color: '#6b7280'}}>
                    {text || '暂无描述'}
                </span>
            ),
        },
        {
            title: '飞机ID',
            dataIndex: 'aircraft_id',
            key: 'aircraft_id',
            width: 200,
            render: (text: string) => (
                <span style={{fontFamily: 'monospace', fontSize: '12px', color: '#6b7280'}}>
                    {text}
                </span>
            ),
        },
        {
            title: '操作',
            key: 'action',
            width: 150,
            fixed: 'right',
            render: (_, record) => (
                <Space>
                    <Button
                        type="link"
                        icon={<EyeOutlined/>}
                        onClick={() => handleView(record)}
                        title="查看详情"
                    />
                    <Button
                        type="link"
                        icon={<EditOutlined/>}
                        onClick={() => handleEdit(record)}
                        title="编辑"
                    />
                    <Button
                        type="link"
                        icon={<DeleteOutlined/>}
                        onClick={() => handleDelete(record)}
                        danger
                        title="删除"
                    />
                </Space>
            ),
        },
    ];

    return (
        <div className="aircraft-page">
            <div className="aircraft-header">
                <h2>飞机管理</h2>
                <Button
                    type="primary"
                    icon={<PlusOutlined/>}
                    onClick={() => setCreateModalVisible(true)}
                >
                    新增飞机
                </Button>
            </div>

            <AircraftSearchBar
                onSearch={handleSearch}
                onReset={handleReset}
                loading={loading}
            />

            <div className="aircraft-table-container">
                <Table
                    columns={columns}
                    dataSource={aircrafts}
                    rowKey="aircraft_id"
                    loading={loading}
                    scroll={{x: 1100}}
                    pagination={{
                        current: aircraftPagination.current_page,
                        pageSize: aircraftPagination.page_size,
                        total: aircraftPagination.total,
                        showSizeChanger: true,
                        showQuickJumper: true,
                        showTotal: (total, range) =>
                            `第 ${range[0]}-${range[1]} 条，共 ${total} 条`,
                        pageSizeOptions: ['10', '20', '50', '100'],
                        onChange: (page, pageSize) => {
                            setAircraftPagination({
                                ...aircraftPagination,
                                current_page: page,
                                page_size: pageSize || aircraftPagination.page_size
                            });
                        },
                        onShowSizeChange: (current, size) => {
                            setAircraftPagination({
                                ...aircraftPagination,
                                current_page: current,
                                page_size: size
                            });
                        },
                    }}
                    locale={{
                        emptyText: Object.keys(searchParams).some(key => searchParams[key as keyof SearchParams])
                            ? '没有找到符合条件的飞机'
                            : '暂无飞机数据'
                    }}
                />
            </div>

            <AircraftCreateModal
                visible={createModalVisible}
                onCancel={() => setCreateModalVisible(false)}
                onSuccess={handleCreateSuccess}
            />

            <AircraftEditModal
                visible={editModalVisible}
                aircraft={selectedAircraft as aircraftType_}
                onCancel={() => {
                    setEditModalVisible(false);
                    setSelectedAircraft(null);
                }}
                onSuccess={handleEditSuccess}
            />

            <AircraftDetailModal
                visible={detailModalVisible}
                aircraft={selectedAircraft}
                onCancel={() => {
                    setDetailModalVisible(false);
                    setSelectedAircraft(null);
                }}
            />
        </div>
    );
};

export default Aircraft;
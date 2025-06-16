import React, {useEffect, useState} from 'react';
import {Card, Row, Col, Button, Modal, message, Pagination} from 'antd';
import {PlusOutlined, EditOutlined, DeleteOutlined, EyeOutlined} from '@ant-design/icons';

import AircraftTypeCreateModal from './AircraftTypeCreateModal';
import AircraftTypeEditModal from './AircraftTypeEditModal';
import AircraftTypeDetailModal from './AircraftTypeDetailModal';
import AircraftTypeSearchBar from './AircraftTypeSearchBar.tsx';

import './AircraftType.css';
import {useAircraftStore} from "../../../store/aircraft/aircraftStore.ts";
import type {aircraftTypeType} from "../../../store/aircraft/types.ts";
import {AircraftTypeService} from "../../../services/AircraftTypeService.ts";

interface SearchParams {
    type_name?: string;
    description?: string;
}

const AircraftType: React.FC = () => {
    const {aircraftTypes, pagination, setPagination} = useAircraftStore();
    const [loading, setLoading] = useState(false);
    const [createModalVisible, setCreateModalVisible] = useState(false);
    const [editModalVisible, setEditModalVisible] = useState(false);
    const [detailModalVisible, setDetailModalVisible] = useState(false);
    const [selectedAircraftType, setSelectedAircraftType] = useState<aircraftTypeType | null>(null);
    const [searchParams, setSearchParams] = useState<SearchParams>({});

    useEffect(() => {
        loadAircraftTypes().then(r => r);
    }, [pagination.current_page, pagination.page_size]);

    const loadAircraftTypes = async (searchData?: SearchParams) => {
        setLoading(true);
        try {
            const params = searchData || searchParams;
            await AircraftTypeService.getAircraftTypeList({
                type_name: params.type_name || null,
                description: params.description || null
            });

        } catch (error) {
            message.error('加载飞机类型列表失败');
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = async (params: SearchParams) => {
        setSearchParams(params);
        await loadAircraftTypes(params);
    };

    const handleReset = async () => {
        setSearchParams({});
        await loadAircraftTypes({});
    };

    const handleView = (aircraftType: aircraftTypeType, e?: React.MouseEvent) => {
        e?.stopPropagation();
        setSelectedAircraftType(aircraftType);
        setDetailModalVisible(true);
    };

    const handleEdit = (aircraftType: aircraftTypeType, e?: React.MouseEvent) => {
        e?.stopPropagation();
        setSelectedAircraftType(aircraftType);
        setEditModalVisible(true);
    };

    const handleDelete = (aircraftType: aircraftTypeType, e?: React.MouseEvent) => {
        e?.stopPropagation();
        Modal.confirm({
            title: '确认删除',
            content: `确定要删除飞机类型 "${aircraftType.type_name}" 吗？`,
            okText: '确认',
            cancelText: '取消',
            onOk: async () => {
                try {
                    await AircraftTypeService.deleteAircraftType(aircraftType.typeid);
                    message.success('删除成功');
                    // 删除后重新加载当前页数据
                    await loadAircraftTypes();
                } catch (error) {
                    message.error('删除失败');
                }
            },
        });
    };

    const handleCreateSuccess = async () => {
        setCreateModalVisible(false);
        message.success('创建成功');
        // 创建成功后重新加载数据
        await loadAircraftTypes();
    };

    const handleEditSuccess = async () => {
        setEditModalVisible(false);
        setSelectedAircraftType(null);
        message.success('更新成功');
        // 更新成功后重新加载数据
        await loadAircraftTypes();
    };

    const handlePageChange = (page: number, pageSize?: number) => {
        setPagination({...pagination, current_page: page, page_size: pageSize || pagination.page_size});
    };

    const handlePageSizeChange = (current: number, size: number) => {
        setPagination({...pagination, current_page: current, page_size: size});
    };

    return (
        <div className="aircraft-type-page">
            <div className="aircraft-type-header">
                <h2>飞机类型管理</h2>
                <Button
                    type="primary"
                    icon={<PlusOutlined/>}
                    onClick={() => setCreateModalVisible(true)}
                >
                    新增飞机类型
                </Button>
            </div>

            <AircraftTypeSearchBar
                onSearch={handleSearch}
                onReset={handleReset}
                loading={loading}
            />

            <Row gutter={[16, 16]} className="aircraft-type-grid">
                {aircraftTypes.map((aircraftType) => (
                    <Col xs={24} sm={12} md={8} lg={6} key={aircraftType.typeid}>
                        <Card
                            className="aircraft-type-card"
                            hoverable
                            onClick={() => handleView(aircraftType)}
                            loading={loading}
                            actions={[
                                <EyeOutlined
                                    key="view"
                                    onClick={(e) => handleView(aircraftType, e)}
                                    title="查看详情"
                                />,
                                <EditOutlined
                                    key="edit"
                                    onClick={(e) => handleEdit(aircraftType, e)}
                                    title="编辑"
                                />,
                                <DeleteOutlined
                                    key="delete"
                                    onClick={(e) => handleDelete(aircraftType, e)}
                                    title="删除"
                                />
                            ]}
                        >
                            <Card.Meta
                                title={aircraftType.type_name}
                                description={
                                    <div className="aircraft-type-card-meta">
                                        <p className="aircraft-type-id">ID: {aircraftType.typeid}</p>
                                        <p className="aircraft-type-description">
                                            {aircraftType.description ?
                                                (aircraftType.description.length > 50 ?
                                                        `${aircraftType.description.substring(0, 50)}...` :
                                                        aircraftType.description
                                                ) :
                                                '暂无描述'
                                            }
                                        </p>
                                    </div>
                                }
                            />
                        </Card>
                    </Col>
                ))}
            </Row>

            {aircraftTypes.length === 0 && !loading && (
                <div className="empty-state">
                    <p>
                        {Object.keys(searchParams).some(key => searchParams[key as keyof SearchParams])
                            ? '没有找到符合条件的飞机类型'
                            : '暂无飞机类型数据'
                        }
                    </p>
                    <Button type="primary" onClick={() => setCreateModalVisible(true)}>
                        创建第一个飞机类型
                    </Button>
                </div>
            )}

            {/* 分页组件 */}
            {aircraftTypes.length > 0 && (
                <div className="aircraft-type-pagination">
                    <Pagination
                        current={pagination.current_page}
                        pageSize={pagination.page_size}
                        total={pagination.total}
                        showSizeChanger
                        showQuickJumper
                        showTotal={(total, range) =>
                            `第 ${range[0]}-${range[1]} 条，共 ${total} 条`
                        }
                        pageSizeOptions={['10', '20', '50', '100']}
                        onChange={handlePageChange}
                        onShowSizeChange={handlePageSizeChange}
                        disabled={loading}
                    />
                </div>
            )}

            <AircraftTypeCreateModal
                visible={createModalVisible}
                onCancel={() => setCreateModalVisible(false)}
                onSuccess={handleCreateSuccess}
            />

            <AircraftTypeEditModal
                visible={editModalVisible}
                aircraftType={selectedAircraftType}
                onCancel={() => {
                    setEditModalVisible(false);
                    setSelectedAircraftType(null);
                }}
                onSuccess={handleEditSuccess}
            />

            <AircraftTypeDetailModal
                visible={detailModalVisible}
                aircraftType={selectedAircraftType}
                onCancel={() => {
                    setDetailModalVisible(false);
                    setSelectedAircraftType(null);
                }}
            />
        </div>
    );
};

export default AircraftType;
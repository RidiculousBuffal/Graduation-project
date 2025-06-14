import React, {useEffect, useState} from 'react';
import {Card, Row, Col, Button, Modal, message, Pagination} from 'antd';
import {PlusOutlined, EditOutlined, DeleteOutlined, EyeOutlined} from '@ant-design/icons';
import {useTerminalStore} from '../../store/terminal/terminalStore';
import {TerminalService} from '../../services/TerminalService';
import TerminalCreateModal from './TerminalCreateModal';
import TerminalEditModal from './TerminalEditModal';
import TerminalDetailModal from './TerminalDetailModal';
import TerminalSearchBar from './TerminalSearchBar';
import type {terminalType} from '../../store/terminal/types';
import './Terminal.css';

interface SearchParams {
    terminal_name?: string;
    description?: string;
}

const Terminal: React.FC = () => {
    const {terminals, pagination, setPagination} = useTerminalStore();
    const [loading, setLoading] = useState(false);
    const [createModalVisible, setCreateModalVisible] = useState(false);
    const [editModalVisible, setEditModalVisible] = useState(false);
    const [detailModalVisible, setDetailModalVisible] = useState(false);
    const [selectedTerminal, setSelectedTerminal] = useState<terminalType | null>(null);
    const [searchParams, setSearchParams] = useState<SearchParams>({});

    useEffect(() => {
        loadTerminals().then(r => r);
    }, [pagination.current_page, pagination.page_size]);

    const loadTerminals = async (searchData?: SearchParams) => {
        setLoading(true);
        try {
            const params = searchData || searchParams;
            await TerminalService.getTerminalList({
                terminal_name: params.terminal_name || null,
                description: params.description || null
            });

        } catch (error) {
            message.error('加载航站楼列表失败');
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = async (params: SearchParams) => {
        setSearchParams(params);
        await loadTerminals(params);
    };

    const handleReset = async () => {
        setSearchParams({});
        await loadTerminals({});
    };

    const handleView = (terminal: terminalType, e?: React.MouseEvent) => {
        e?.stopPropagation();
        setSelectedTerminal(terminal);
        setDetailModalVisible(true);
    };

    const handleEdit = (terminal: terminalType, e?: React.MouseEvent) => {
        e?.stopPropagation();
        setSelectedTerminal(terminal);
        setEditModalVisible(true);
    };

    const handleDelete = (terminal: terminalType, e?: React.MouseEvent) => {
        e?.stopPropagation();
        Modal.confirm({
            title: '确认删除',
            content: `确定要删除航站楼 "${terminal.terminal_name}" 吗？`,
            okText: '确认',
            cancelText: '取消',
            onOk: async () => {
                try {
                    await TerminalService.deleteTerminal(terminal.terminal_id);
                    message.success('删除成功');
                    // 删除后重新加载当前页数据
                    await loadTerminals();
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
        await loadTerminals();
    };

    const handleEditSuccess = async () => {
        setEditModalVisible(false);
        setSelectedTerminal(null);
        message.success('更新成功');
        // 更新成功后重新加载数据
        await loadTerminals();
    };

    const handlePageChange = (page: number, pageSize?: number) => {
        setPagination({...pagination, current_page: page, page_size: pageSize || pagination.page_size});
    };

    const handlePageSizeChange = (current: number, size: number) => {
        setPagination({...pagination, current_page: current, page_size: size});
    };

    return (
        <div className="terminal-page">
            <div className="terminal-header">
                <h2>航站楼管理</h2>
                <Button
                    type="primary"
                    icon={<PlusOutlined/>}
                    onClick={() => setCreateModalVisible(true)}
                >
                    新增航站楼
                </Button>
            </div>

            <TerminalSearchBar
                onSearch={handleSearch}
                onReset={handleReset}
                loading={loading}
            />

            <Row gutter={[16, 16]} className="terminal-grid">
                {terminals.map((terminal) => (
                    <Col xs={24} sm={12} md={8} lg={6} key={terminal.terminal_id}>
                        <Card
                            className="terminal-card"
                            hoverable
                            onClick={() => handleView(terminal)}
                            loading={loading}
                            actions={[
                                <EyeOutlined
                                    key="view"
                                    onClick={(e) => handleView(terminal, e)}
                                    title="查看详情"
                                />,
                                <EditOutlined
                                    key="edit"
                                    onClick={(e) => handleEdit(terminal, e)}
                                    title="编辑"
                                />,
                                <DeleteOutlined
                                    key="delete"
                                    onClick={(e) => handleDelete(terminal, e)}
                                    title="删除"
                                />
                            ]}
                        >
                            <Card.Meta
                                title={terminal.terminal_name}
                                description={
                                    <div className="terminal-card-meta">
                                        <p className="terminal-id">ID: {terminal.terminal_id}</p>
                                        <p className="terminal-description">
                                            {terminal.description ?
                                                (terminal.description.length > 50 ?
                                                        `${terminal.description.substring(0, 50)}...` :
                                                        terminal.description
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

            {terminals.length === 0 && !loading && (
                <div className="empty-state">
                    <p>
                        {Object.keys(searchParams).some(key => searchParams[key as keyof SearchParams])
                            ? '没有找到符合条件的航站楼'
                            : '暂无航站楼数据'
                        }
                    </p>
                    <Button type="primary" onClick={() => setCreateModalVisible(true)}>
                        创建第一个航站楼
                    </Button>
                </div>
            )}

            {/* 分页组件 */}
            {terminals.length > 0 && (
                <div className="terminal-pagination">
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

            <TerminalCreateModal
                visible={createModalVisible}
                onCancel={() => setCreateModalVisible(false)}
                onSuccess={handleCreateSuccess}
            />

            <TerminalEditModal
                visible={editModalVisible}
                terminal={selectedTerminal}
                onCancel={() => {
                    setEditModalVisible(false);
                    setSelectedTerminal(null);
                }}
                onSuccess={handleEditSuccess}
            />

            <TerminalDetailModal
                visible={detailModalVisible}
                terminal={selectedTerminal}
                onCancel={() => {
                    setDetailModalVisible(false);
                    setSelectedTerminal(null);
                }}
            />
        </div>
    );
};

export default Terminal;
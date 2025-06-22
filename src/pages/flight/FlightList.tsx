import React, { useEffect, useState } from 'react';
import { Table, Button, Space, message, Popconfirm, Spin } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, EyeOutlined } from '@ant-design/icons';
import { useFlightStore } from '../../store/flight/flightStore';

import { FlightSearchBar } from './FlightSearchBar';
import { FlightCreateModal } from './FlightCreateModal';
import { FlightEditModal } from './FlightEditModal';
import { FlightDetailModal } from './FlightDetailModal';
import type { flightListType } from '../../store/flight/types';
import type { SearchFlightPayload } from '../../api/flightapi';
import {formatGMTDateToLocal, formatUTCToLocal} from '../../utils/dateUtils';
import './Flight.css';
import {FlightService} from "../../services/FlightService.ts";

export const FlightList: React.FC = () => {
  const { flights, flightsPagination, setFlightsPagination } = useFlightStore();
  const [loading, setLoading] = useState(false);
  const [createModalVisible, setCreateModalVisible] = useState(false);
  const [editModalVisible, setEditModalVisible] = useState(false);
  const [detailModalVisible, setDetailModalVisible] = useState(false);
  const [selectedFlight, setSelectedFlight] = useState<flightListType | null>(null);

  // 加载航班列表
  const loadFlights = async (searchParams: SearchFlightPayload = {}) => {
    setLoading(true);
    try {
      await FlightService.getFlightList(searchParams);
    } catch (error) {
      message.error('加载航班列表失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFlights();
  }, []);

  // 处理搜索
  const handleSearch = (searchParams: SearchFlightPayload) => {
    setFlightsPagination({ ...flightsPagination, current_page: 1 });
    loadFlights(searchParams);
  };

  // 处理分页变化
  const handleTableChange = (page: number, pageSize: number) => {
    const newPagination = {
      ...flightsPagination,
      current_page: page,
      page_size: pageSize,
    };
    setFlightsPagination(newPagination);
    loadFlights();
  };

  // 删除航班
  const handleDelete = async (flightId: string) => {
    try {
      const success = await FlightService.deleteFlight(flightId);
      if (success) {
        message.success('删除成功');
      }
    } catch (error) {
      message.error('删除失败');
    }
  };

  // 打开编辑模态框
  const handleEdit = (flight: flightListType) => {
    setSelectedFlight(flight);
    setEditModalVisible(true);
  };

  // 打开详情模态框
  const handleDetail = (flight: flightListType) => {
    setSelectedFlight(flight);
    setDetailModalVisible(true);
  };

  const columns = [
    {
      title: '航班ID',
      dataIndex: 'flight_id',
      key: 'flight_id',
      width: 100,
    },
    {
      title: '飞机名称',
      dataIndex: 'aircraft_name',
      key: 'aircraft_name',
    },
    {
      title: '航站楼',
      dataIndex: 'terminal_name',
      key: 'terminal_name',
    },
    {
      title: '预计起飞',
      dataIndex: 'estimated_departure',
      key: 'estimate_departure',
      render: (date: string) => date ? formatUTCToLocal(date) : '-',
    },
    {
      title: '预计到达',
      dataIndex: 'estimated_arrival',
      key: 'estimate_arrival',
      render: (date: string) => date ? formatUTCToLocal(date) : '-',
    },
    {
      title: '实际起飞',
      dataIndex: 'actual_departure',
      key: 'actual_departure',
      render: (date: string) => date ? formatUTCToLocal(date) : '-',
    },
    {
      title: '实际到达',
      dataIndex: 'actual_arrival',
      key: 'actual_arrival',
      render: (date: string) => date ? formatUTCToLocal(date) : '-',
    },
    {
      title: '航班状态',
      dataIndex: 'flight_status',
      key: 'flight_status',
    },
    {
      title: '健康状态',
      dataIndex: 'health_status',
      key: 'health_status',
    },
    {
      title: '审批状态',
      dataIndex: 'approval_status',
      key: 'approval_status',
    },
    {
      title: '操作',
      key: 'action',
      width: 200,
      render: (_: any, record: flightListType) => (
        <Space size="small">
          <Button
            type="primary"
            icon={<EyeOutlined />}
            size="small"
            onClick={() => handleDetail(record)}
          >
            详情
          </Button>
          <Button
            type="default"
            icon={<EditOutlined />}
            size="small"
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
          <Popconfirm
            title="确认删除"
            description="确定要删除这个航班吗？"
            onConfirm={() => handleDelete(record.flight_id!)}
            okText="确认"
            cancelText="取消"
          >
            <Button
              type="primary"
              danger
              icon={<DeleteOutlined />}
              size="small"
            >
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div className="flight-list-container">
      <div className="flight-list-header">
        <h1>航班管理</h1>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => setCreateModalVisible(true)}
        >
          新增航班
        </Button>
      </div>

      <FlightSearchBar onSearch={handleSearch} />

      <Spin spinning={loading}>
        <Table
          columns={columns}
          dataSource={flights}
          rowKey="flight_id"
          pagination={{
            current: flightsPagination.current_page,
            pageSize: flightsPagination.page_size,
            total: flightsPagination.total,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) =>
              `第 ${range[0]}-${range[1]} 条/共 ${total} 条`,
            onChange: handleTableChange,
            onShowSizeChange: handleTableChange,
          }}
          scroll={{ x: 1200 }}
        />
      </Spin>

      {/* 新增模态框 */}
      <FlightCreateModal
        visible={createModalVisible}
        onCancel={() => setCreateModalVisible(false)}
        onSuccess={() => {
          setCreateModalVisible(false);
          loadFlights();
        }}
      />

      {/* 编辑模态框 */}
      <FlightEditModal
        visible={editModalVisible}
        flight={selectedFlight}
        onCancel={() => {
          setEditModalVisible(false);
          setSelectedFlight(null);
        }}
        onSuccess={() => {
          setEditModalVisible(false);
          setSelectedFlight(null);
          loadFlights();
        }}
      />

      {/* 详情模态框 */}
      <FlightDetailModal
        visible={detailModalVisible}
        flightId={selectedFlight?.flight_id || ''}
        onCancel={() => {
          setDetailModalVisible(false);
          setSelectedFlight(null);
        }}
      />
    </div>
  );
};
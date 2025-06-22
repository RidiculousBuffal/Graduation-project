import React, {useEffect, useState} from 'react';
import {Modal, Descriptions, Spin, message} from 'antd';
import {FlightService} from '../../services/FlightService';
import {DictionaryService} from '../../services/DictionaryService';
import {APPROVAL_STATUS, FLIGHT_STATUS, HEALTH_STATUS} from '../../consts/dictionary.ts';
import type {flightType} from '../../store/flight/types';
import type {dictionaryType} from '../../store/dictionary/type';
import './FlightDetailModal.css';
import {formatUTCToLocal} from "../../utils/dateUtils.ts";

interface FlightDetailModalProps {
    visible: boolean;
    flightId: string;
    onCancel: () => void;
}

export const FlightDetailModal: React.FC<FlightDetailModalProps> = ({
                                                                        visible,
                                                                        flightId,
                                                                        onCancel,
                                                                    }) => {
    const [loading, setLoading] = useState(false);
    const [flightDetail, setFlightDetail] = useState<flightType | null>(null);
    const [statusMaps, setStatusMaps] = useState<{
        flightStatus: Map<string, string>;
        healthStatus: Map<string, string>;
        approvalStatus: Map<string, string>;
    }>({
        flightStatus: new Map(),
        healthStatus: new Map(),
        approvalStatus: new Map(),
    });

    // 加载航班详情和字典数据
    useEffect(() => {
        if (visible && flightId) {
            loadFlightDetail();
            loadDictionaries();
        }
    }, [visible, flightId]);

    const loadFlightDetail = async () => {
        setLoading(true);
        try {
            const response = await FlightService.getFlightDetailById(flightId);
            if (response) {
                setFlightDetail(response);
            }
        } catch (error) {
            message.error('加载航班详情失败');
        } finally {
            setLoading(false);
        }
    };

    const loadDictionaries = async () => {
        try {
            const [flightStatus, healthStatus, approvalStatus] = await Promise.all([
                DictionaryService.getChildrenByParentId(FLIGHT_STATUS),
                DictionaryService.getChildrenByParentId(HEALTH_STATUS),
                DictionaryService.getChildrenByParentId(APPROVAL_STATUS),
            ]);

            const flightStatusMap = new Map<string, string>();
            const healthStatusMap = new Map<string, string>();
            const approvalStatusMap = new Map<string, string>();

            flightStatus?.forEach((item: dictionaryType) => {
                flightStatusMap.set(item.dict_key, item.dict_name);
            });

            healthStatus?.forEach((item: dictionaryType) => {
                healthStatusMap.set(item.dict_key, item.dict_name);
            });

            approvalStatus?.forEach((item: dictionaryType) => {
                approvalStatusMap.set(item.dict_key, item.dict_name);
            });

            setStatusMaps({
                flightStatus: flightStatusMap,
                healthStatus: healthStatusMap,
                approvalStatus: approvalStatusMap,
            });
        } catch (error) {
            console.error('加载字典数据失败:', error);
        }
    };

    const getStatusName = (statusKey: string | null | undefined, statusMap: Map<string, string>) => {
        if (!statusKey) return '-';
        return statusMap.get(statusKey) || statusKey;
    };

    return (
        <Modal
            title="航班详情"
            open={visible}
            onCancel={onCancel}
            footer={null}
            width={800}
            className="flight-detail-modal"
        >
            <Spin spinning={loading}>
                {flightDetail && (
                    <Descriptions column={2} bordered>
                        <Descriptions.Item label="航班ID">
                            {flightDetail.flight_id || '-'}
                        </Descriptions.Item>
                        <Descriptions.Item label="飞机ID">
                            {flightDetail.aircraft_id || '-'}
                        </Descriptions.Item>
                        <Descriptions.Item label="航班状态">
                            {getStatusName(flightDetail.flight_status, statusMaps.flightStatus)}
                        </Descriptions.Item>
                        <Descriptions.Item label="健康状态">
                            {getStatusName(flightDetail.health_status, statusMaps.healthStatus)}
                        </Descriptions.Item>
                        <Descriptions.Item label="审批状态">
                            {getStatusName(flightDetail.approval_status, statusMaps.approvalStatus)}
                        </Descriptions.Item>
                        <Descriptions.Item label="预计起飞时间">
                            {flightDetail.estimated_departure ? formatUTCToLocal(flightDetail.estimated_departure) : '-'}
                        </Descriptions.Item>
                        <Descriptions.Item label="预计到达时间">
                            {flightDetail.estimated_arrival ? formatUTCToLocal(flightDetail.estimated_arrival) : '-'}
                        </Descriptions.Item>
                        <Descriptions.Item label="实际起飞时间">
                            {flightDetail.actual_departure ? formatUTCToLocal(flightDetail.actual_departure) : '-'}
                        </Descriptions.Item>
                        <Descriptions.Item label="实际到达时间">
                            {flightDetail.actual_arrival ? formatUTCToLocal(flightDetail.actual_arrival): '-'}
                        </Descriptions.Item>
                    </Descriptions>
                )}
            </Spin>
        </Modal>
    );
};
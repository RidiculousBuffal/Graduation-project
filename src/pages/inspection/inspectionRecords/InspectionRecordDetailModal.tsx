import React, {useState, useEffect} from 'react';
import {Modal, Descriptions, message, Spin} from 'antd';
import {getAllImageInOneFlight, type FlightImage} from '@/api/flightapi';
import AnnotationCanvas from '@/components/imageInnot/AnnotationCanvas';
import PointsDataViewer from '@/components/imageInnot/PointsDataViewer';
import type {InspectionRecordListType} from '@/store/inspection/types';
import type {Point} from '@/components/imageInnot/types';
import dayjs from 'dayjs';
import {formatUTCToLocal} from "@/utils/dateUtils.ts";

interface InspectionRecordDetailModalProps {
    visible: boolean;
    record: InspectionRecordListType | null;
    onCancel: () => void;
}

const InspectionRecordDetailModal: React.FC<InspectionRecordDetailModalProps> = ({
                                                                                     visible,
                                                                                     record,
                                                                                     onCancel
                                                                                 }) => {
    const [loading, setLoading] = useState(false);
    const [imageData, setImageData] = useState<FlightImage | null>(null);
    const [points, setPoints] = useState<Point[]>([]);

    useEffect(() => {
        if (visible && record) {
            loadImageData();
        }
    }, [visible, record]);

    const loadImageData = async () => {
        if (!record?.flight_id) return;

        setLoading(true);
        try {
            const result = await getAllImageInOneFlight(record.flight_id);
            if (result) {
                const image = result.find(img => img.aircraft_image_id === record.reference_image_id);
                if (image) {
                    setImageData(image);
                    // 从 aircraft_image_json 中提取点位信息
                    if (image.aircraft_image_json?.pointInfo) {
                        setPoints(image.aircraft_image_json.pointInfo);
                    }
                }
            }
        } catch (error) {
            message.error('获取底图信息失败');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Modal
            title="检测条目详情"
            open={visible}
            onCancel={onCancel}
            footer={null}
            width={1200}
            style={{top: 20}}
            destroyOnHidden={true}
        >
            {loading ? (
                <div style={{textAlign: 'center', padding: '50px'}}>
                    <Spin size="large"/>
                </div>
            ) : (
                <div>
                    <Descriptions title="基本信息" bordered column={2}>
                        <Descriptions.Item label="检测条目名称">
                            {record?.inspection_name}
                        </Descriptions.Item>
                        <Descriptions.Item label="执行工程师">
                            {record?.executor_name ? record.executor_name : `${record?.executor_id}(未设置姓名)`}
                        </Descriptions.Item>
                        <Descriptions.Item label="飞机">
                            {record?.aircraft_name}
                        </Descriptions.Item>
                        <Descriptions.Item label="检测状态">
                            {record?.status_name}
                        </Descriptions.Item>
                        <Descriptions.Item label="进度">
                            {record?.progress}%
                        </Descriptions.Item>
                        <Descriptions.Item label="参考底图">
                            {record?.reference_image_name}
                        </Descriptions.Item>
                        <Descriptions.Item label="开始时间">
                            {record?.start_time ? formatUTCToLocal(record.start_time) : '-'}
                        </Descriptions.Item>
                        <Descriptions.Item label="结束时间">
                            {record?.end_time ? dayjs(record.end_time).format('YYYY-MM-DD HH:mm:ss') : '-'}
                        </Descriptions.Item>
                        <Descriptions.Item label="创建时间" span={2}>
                            {record?.created_at ? dayjs(record.created_at).format('YYYY-MM-DD HH:mm:ss') : '-'}
                        </Descriptions.Item>
                    </Descriptions>

                    {imageData && (
                        <div style={{marginTop: '24px'}}>
                            <h3>参考底图与点位信息</h3>
                            <div style={{display: 'flex', gap: '16px'}}>
                                <div style={{flex: 1}}>
                                    <AnnotationCanvas
                                        image={imageData.aircraft_image_json?.fileInfo.download_url || ''}
                                        points={points}
                                        isAddMode={true}
                                        showCurve={true}
                                        onAddPoint={() => {
                                        }} // 详情页面不允许添加点位
                                        onDeletePoint={() => {
                                        }} // 详情页面不允许删除点位
                                    />
                                </div>
                                <div style={{width: '300px'}}>
                                    <PointsDataViewer points={points}/>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            )}
        </Modal>
    );
};

export default InspectionRecordDetailModal;
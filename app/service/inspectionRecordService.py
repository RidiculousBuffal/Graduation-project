from datetime import datetime
from typing import Optional

from app.DTO.inspections import (
    InspectionRecordCreateDTO, InspectionRecordUpdateDTO,
    InspectionRecordDTO, InspectionRecordDetailDTO, InspectionRecordPagedResponseDTO
)
from app.mapper.tasks.inspectionRecordMapper import InspectionRecordMapper


class InspectionRecordService:
    """检查记录服务类"""

    @staticmethod
    def create_inspection_record(inspection_data: InspectionRecordCreateDTO) -> InspectionRecordDTO:
        """
        创建新的检查记录
        :param inspection_data: 检查记录创建数据
        :return: 创建的检查记录信息
        """
        return InspectionRecordMapper.create(inspection_data)
    
    @staticmethod
    def get_inspection_record(inspection_id: str) -> Optional[InspectionRecordDetailDTO]:
        """
        根据ID获取检查记录详情
        :param inspection_id: 检查记录ID
        :return: 检查记录详情或None（如果不存在）
        """
        return InspectionRecordMapper.get_by_id(inspection_id)
    
    @staticmethod
    def update_inspection_record(inspection_id: str, 
                                update_data: InspectionRecordUpdateDTO) -> Optional[InspectionRecordDTO]:
        """
        更新检查记录信息
        :param inspection_id: 检查记录ID
        :param update_data: 更新的数据
        :return: 更新后的检查记录或None（如果记录不存在）
        """
        return InspectionRecordMapper.update(inspection_id, update_data)
    
    @staticmethod
    def delete_inspection_record(inspection_id: str) -> bool:
        """
        删除检查记录
        :param inspection_id: 检查记录ID
        :return: 删除操作是否成功
        """
        return InspectionRecordMapper.delete(inspection_id)
    
    @staticmethod
    def search_inspection_records(
            task_id: Optional[str] = None,
            executor_id: Optional[str] = None,
            inspection_status: Optional[str] = None,
            reference_image_id: Optional[str] = None,
            flight_id: Optional[str] = None,
            aircraft_id: Optional[str] = None,
            executor_name: Optional[str] = None,
            start_time_from: Optional[datetime] = None,
            start_time_to: Optional[datetime] = None,
            end_time_from: Optional[datetime] = None,
            end_time_to: Optional[datetime] = None,
            page_num: int = 1,
            page_size: int = 10
    ) -> InspectionRecordPagedResponseDTO:
        """
        分页搜索检查记录
        :param task_id: 任务ID
        :param executor_id: 执行人ID
        :param inspection_status: 检查状态
        :param reference_image_id: 参考图片ID
        :param flight_id: 航班ID
        :param aircraft_id: 飞机ID
        :param executor_name: 执行人姓名
        :param start_time_from: 开始时间起点
        :param start_time_to: 开始时间终点
        :param end_time_from: 结束时间起点
        :param end_time_to: 结束时间终点
        :param page_num: 页码
        :param page_size: 每页大小
        :return: 分页后的检查记录列表
        """
        return InspectionRecordMapper.search(
            task_id=task_id,
            executor_id=executor_id,
            inspection_status=inspection_status,
            reference_image_id=reference_image_id,
            flight_id=flight_id,
            aircraft_id=aircraft_id,
            executor_name=executor_name,
            start_time_from=start_time_from,
            start_time_to=start_time_to,
            end_time_from=end_time_from,
            end_time_to=end_time_to,
            page_num=page_num,
            page_size=page_size
        )

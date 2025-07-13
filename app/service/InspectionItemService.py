from typing import Optional

from app.DTO.inspectionItems import (
    InspectionItemCreateDTO,
    InspectionItemUpdateDTO,
    InspectionItemDTO, InspectionItemResultDTO, InspectionItemPagedResponseDTO
)
from app.mapper.tasks.inspectionItemMapper import InspectionItemMapper


class InspectionItemService:
    """检查项（InspectionItem）服务类"""

    @staticmethod
    def create_inspection_item(item_data: InspectionItemCreateDTO) -> InspectionItemDTO:
        """
        创建新的检查项
        :param item_data: 检查项创建数据
        :return: 创建的检查项信息
        """
        result = InspectionItemResultDTO(inputImage=item_data.item_point.fileInfo, progress='pending', version=1)
        item_data.result.append(result)
        return InspectionItemMapper.create(item_data)

    @staticmethod
    def get_inspection_item(item_id: str) -> Optional[InspectionItemDTO]:
        """
        根据ID获取单个检查项
        :param item_id: 检查项ID
        :return: 检查项信息或 None（如果不存在）
        """
        return InspectionItemMapper.get_by_id(item_id)

    @staticmethod
    def update_inspection_item(item_id: str, update_data: InspectionItemUpdateDTO) -> Optional[InspectionItemDTO]:
        """
        更新检查项
        :param item_id: 检查项ID
        :param update_data: 更新数据
        :return: 更新后的检查项或 None（如果不存在）
        """
        item = InspectionItemService.get_inspection_item(item_id)
        #  降序排列
        sorted_item = sorted(item.result, key=lambda x: x.version, reverse=True)
        new_version = sorted_item[0].version + 1
        # 结束未完成的任务
        for res in item.result:
            if res.progress == 'pending':
                res.progress = 'canceled'
        result = InspectionItemResultDTO(inputImage=update_data.item_point.fileInfo, progress='pending',
                                         version=new_version)
        item.result.append(result)
        update_data.result = item.result
        return InspectionItemMapper.update(item_id, update_data)

    @staticmethod
    def delete_inspection_item(item_id: str) -> bool:
        """
        删除检查项
        :param item_id: 检查项ID
        :return: 删除是否成功
        """
        return InspectionItemMapper.delete(item_id)

    @staticmethod
    def list_items_by_inspection(
            inspection_id: str,
            page_num: int,
            page_size: int
    ) -> InspectionItemPagedResponseDTO:
        """
        根据 inspection_id 分页列出所有关联的检查项
        """
        return InspectionItemMapper.list_by_inspection_id(
            inspection_id=inspection_id,
            page_num=page_num,
            page_size=page_size
        )

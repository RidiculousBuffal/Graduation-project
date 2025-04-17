from typing import Optional

from sqlalchemy.exc import IntegrityError

from app.DTO.aircrafts import (
    AircraftReferenceImageCreateDTO,
    AircraftReferenceImageUpdateDTO,
    AircraftReferenceImageDTO,
    AircraftReferenceImagePagedResponseDTO
)
from app.consts.Aircrafts import AircraftConsts
from app.mapper.aircraft.aircraftReferenceImageMapper import AircraftReferenceImageMapper
from app.models.response import ResponseModel

class AircraftReferenceImageService:
    @staticmethod
    def create_image(image_data: AircraftReferenceImageCreateDTO) -> ResponseModel:
        """创建飞机参考图片记录"""
        # 参数校验
        if not image_data.image_name or not image_data.aircraft_id:
            return ResponseModel.fail(
                msg=AircraftConsts.INVALID_IMAGE_DATA,
                data={"error": "图片名称和飞机ID不能为空"}
            )

        # 校验是否为图片格式
        mime_type = image_data.image_json.fileInfo.mime_type
        print(mime_type)
        if mime_type is None or not mime_type.startswith('image/'):
            return ResponseModel.fail(
                msg=AircraftConsts.INVALID_IMAGE_DATA,
                data={"error": "文件必须是图片格式（mime 类型需以 'image/' 开头）"}
            )

        try:
            result: AircraftReferenceImageDTO = AircraftReferenceImageMapper.create(image_data)
            return ResponseModel.success(
                msg=AircraftConsts.ADD_IMAGE_SUCCESS,
                data=result.model_dump()
            )
        except IntegrityError as e:
            return ResponseModel.fail(
                msg=AircraftConsts.ADD_IMAGE_ERROR,
                data={"error": str(e)}
            )
        except Exception as e:
            return ResponseModel.fail(
                msg=AircraftConsts.ADD_IMAGE_ERROR,
                data={"error": str(e)}
            )

    @staticmethod
    def get_image_by_id(image_id: str) -> ResponseModel:
        """根据ID获取飞机参考图片记录"""
        if not image_id:
            return ResponseModel.fail(
                msg=AircraftConsts.INVALID_IMAGE_DATA,
                data={"error": "图片ID不能为空"}
            )

        result: Optional[AircraftReferenceImageDTO] = AircraftReferenceImageMapper.get_by_id(image_id)
        if result:
            return ResponseModel.success(
                msg=AircraftConsts.GET_IMAGE_SUCCESS,
                data=result.model_dump()
            )
        return ResponseModel.fail(
            msg=AircraftConsts.GET_IMAGE_NOT_FOUND,
            data={"error": f"未找到ID为{image_id}的飞机参考图片"}
        )

    @staticmethod
    def update_image(image_id: str, update_data: AircraftReferenceImageUpdateDTO) -> ResponseModel:
        """更新飞机参考图片记录"""
        if not image_id:
            return ResponseModel.fail(
                msg=AircraftConsts.INVALID_IMAGE_DATA,
                data={"error": "图片ID不能为空"}
            )

        try:
            result: Optional[AircraftReferenceImageDTO] = AircraftReferenceImageMapper.update(image_id, update_data)
            if result:
                return ResponseModel.success(
                    msg=AircraftConsts.UPDATE_IMAGE_SUCCESS,
                    data=result.model_dump()
                )
            return ResponseModel.fail(
                msg=AircraftConsts.UPDATE_IMAGE_ERROR,
                data={"error": f"未找到ID为{image_id}的飞机参考图片或更新失败"}
            )
        except IntegrityError as e:
            return ResponseModel.fail(
                msg=AircraftConsts.UPDATE_IMAGE_ERROR,
                data={"error": str(e)}
            )
        except Exception as e:
            return ResponseModel.fail(
                msg=AircraftConsts.UPDATE_IMAGE_ERROR,
                data={"error": str(e)}
            )

    @staticmethod
    def delete_image(image_id: str) -> ResponseModel:
        """删除飞机参考图片记录"""
        if not image_id:
            return ResponseModel.fail(
                msg=AircraftConsts.INVALID_IMAGE_DATA,
                data={"error": "图片ID不能为空"}
            )

        success = AircraftReferenceImageMapper.delete(image_id)
        if success:
            return ResponseModel.success(
                msg=AircraftConsts.DELETE_IMAGE_SUCCESS,
                data=None
            )
        return ResponseModel.fail(
            msg=AircraftConsts.DELETE_IMAGE_ERROR,
            data={"error": f"未找到ID为{image_id}的飞机参考图片或删除失败"}
        )

    @staticmethod
    def search_image(
            image_name: Optional[str] = None,
            aircraft_id: Optional[str] = None,
            aircraft_name: Optional[str] = None,
            page_num: int = 1,
            page_size: int = 10
    ) -> ResponseModel:
        """分页查询飞机参考图片记录"""
        if page_num < 1 or page_size < 1:
            return ResponseModel.fail(
                msg=AircraftConsts.INVALID_IMAGE_DATA,
                data={"error": "页码和每页大小必须大于0"}
            )

        result: AircraftReferenceImagePagedResponseDTO = AircraftReferenceImageMapper.search(
            image_name=image_name,
            aircraft_id=aircraft_id,
            aircraft_name=aircraft_name,
            page_num=page_num,
            page_size=page_size
        )
        return ResponseModel.success(
            msg=AircraftConsts.SEARCH_IMAGE_SUCCESS,
            data=result.model_dump()
        )
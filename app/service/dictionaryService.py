# app/service/dictionaryService.py
from typing import Optional, List
from app.DTO.dictionary import DictionaryDetailDTO, DictionaryPagedResponseDTO
from app.consts.Dictionary import DictionaryConsts
from app.mapper.dictionary.dictionaryMapper import DictionaryMapper
from app.models.response import ResponseModel

class DictionaryService:
    @staticmethod
    def get_dictionary_by_key(dict_key: str) -> ResponseModel:
        """根据字典键获取字典记录，包含详细信息"""
        if not dict_key:
            return ResponseModel.fail(
                msg=DictionaryConsts.INVALID_DICTIONARY_DATA,
                data={"error": "字典键不能为空"}
            )

        result: Optional[DictionaryDetailDTO] = DictionaryMapper.get_by_key(dict_key)
        if result:
            return ResponseModel.success(
                msg=DictionaryConsts.GET_DICTIONARY_SUCCESS,
                data=result.model_dump()
            )
        return ResponseModel.fail(
            msg=DictionaryConsts.GET_DICTIONARY_NOT_FOUND,
            data={"error": f"未找到键为{dict_key}的字典"}
        )

    @staticmethod
    def get_children_by_parent_key(parent_key: str) -> ResponseModel:
        """查询某个父字典下的所有子字典"""
        if not parent_key:
            return ResponseModel.fail(
                msg=DictionaryConsts.INVALID_DICTIONARY_DATA,
                data={"error": "父字典键不能为空"}
            )

        result: List[DictionaryDetailDTO] = DictionaryMapper.get_children_by_parent_key(parent_key)
        return ResponseModel.success(
            msg=DictionaryConsts.GET_CHILDREN_SUCCESS,
            data=[item.model_dump() for item in result]
        )

    @staticmethod
    def search_dictionary(
            dict_name: Optional[str] = None,
            parent_key: Optional[str] = None,
            page_num: int = 1,
            page_size: int = 10
    ) -> ResponseModel:
        """分页查询字典记录，支持按名称和父字典键过滤"""
        if page_num < 1 or page_size < 1:
            return ResponseModel.fail(
                msg=DictionaryConsts.INVALID_DICTIONARY_DATA,
                data={"error": "页码和每页大小必须大于0"}
            )

        result: DictionaryPagedResponseDTO = DictionaryMapper.search(
            dict_name=dict_name,
            parent_key=parent_key,
            pageNum=page_num,
            pageSize=page_size
        )
        return ResponseModel.success(
            msg=DictionaryConsts.SEARCH_DICTIONARY_SUCCESS,
            data=result.model_dump()
        )
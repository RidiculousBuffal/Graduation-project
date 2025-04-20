# app/mapper/dictionary/dictionaryMapper.py
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.DTO.dictionary import DictionaryDTO, DictionaryDetailDTO, DictionaryPagedResponseDTO
from app.DTO.pagination import PaginationDTO
from app.ext.extensions import db
from app.models.dictionary import Dictionary

class DictionaryMapper:
    @staticmethod
    def get_by_key(dict_key: str) -> Optional[DictionaryDetailDTO]:
        """根据字典键查询字典记录，包含子字典"""
        dictionary = (db.session.query(Dictionary)
                      .options(joinedload(Dictionary.children))
                      .get(dict_key))
        if dictionary:
            return DictionaryMapper._build_detail_dto(dictionary)
        return None

    @staticmethod
    def get_children_by_parent_key(parent_key: str) -> List[DictionaryDetailDTO]:
        """查询某个父字典下的所有子字典"""
        children = (db.session.query(Dictionary)
                    .options(joinedload(Dictionary.children))
                    .filter(Dictionary.parent_key == parent_key)
                    .order_by(Dictionary.sort_order)
                    .all())
        return [DictionaryMapper._build_detail_dto(child) for child in children]

    @staticmethod
    def search(
            dict_name: Optional[str] = None,
            parent_key: Optional[str] = None,
            pageNum: int = 1,
            pageSize: int = 10
    ) -> DictionaryPagedResponseDTO:
        """分页查询字典记录，支持按名称和父字典键过滤"""
        query = select(Dictionary).options(joinedload(Dictionary.children))

        # 条件过滤
        if dict_name:
            query = query.where(Dictionary.dict_name.ilike(f"%{dict_name}%"))  # 支持模糊查询
        if parent_key:
            query = query.where(Dictionary.parent_key == parent_key)

        query = query.order_by(Dictionary.sort_order)
        pagination = db.paginate(
            select=query,
            page=pageNum,
            per_page=pageSize,
            max_per_page=100,
            error_out=False,
            count=True
        )

        # 手动构建 DictionaryDetailDTO 列表
        dictionaries_data = [DictionaryMapper._build_detail_dto(dictionary) for dictionary in pagination.items]

        pagination_dto = PaginationDTO(
            current_page=pagination.page,
            page_size=pagination.per_page,
            total=pagination.total or 0,
            total_pages=pagination.pages
        )

        response = DictionaryPagedResponseDTO(
            data=dictionaries_data,
            pagination=pagination_dto
        )
        return response

    @staticmethod
    def _build_detail_dto(dictionary: Dictionary) -> DictionaryDetailDTO:
        """构建 DictionaryDetailDTO，包含子字典的嵌套结构"""
        children = [DictionaryMapper._build_detail_dto(child) for child in dictionary.children] if dictionary.children else []
        return DictionaryDetailDTO(
            dict_key=dictionary.dict_key,
            dict_name=dictionary.dict_name,
            description=dictionary.description,
            parent_key=dictionary.parent_key,
            sort_order=dictionary.sort_order,
            created_at=dictionary.created_at,
            updated_at=dictionary.updated_at,
            children=children
        )
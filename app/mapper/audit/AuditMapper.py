from app.DTO.Audit import AuditLogSearchResponsePaginationDTO, AuditLogSearchDTO, ActionDTO
from app.DTO.pagination import PaginationDTO
from app.models.audit import AuditLog
from app.ext.extensions import db
from sqlalchemy import select


class AuditLogMapper:
    """
    用于处理 AuditLog 数据模型的数据库操作
    """

    @staticmethod
    def SearchAuditLogs(
            page_num: int = 1,
            page_size: int = 10,
    ) -> AuditLogSearchResponsePaginationDTO:
        """
        分页查询审计日志。

        Args:
            page_num (int): 当前页码。
            page_size (int): 每页记录数。

        Returns:
            AuditLogSearchResponsePaginationDTO: 包含分页数据和分页信息的DTO。
        """
        # 基础查询
        query = select(AuditLog)
        query = query.order_by(AuditLog.timestamp.desc())
        pagination = db.paginate(
            select=query,
            page=page_num,
            per_page=page_size,
            max_per_page=100,
            error_out=False,
            count=True
        )
        data_dto_list = [
            AuditLogSearchDTO(log_id=x.log_id, action=ActionDTO.model_validate(x.action), timestamp=x.timestamp,
                              blockchain_operator=x.blockchain_operator, user_id=x.user_id,
                              blockchain_tx_hash=x.blockchain_tx_hash,
                              blockchain_block_number=x.blockchain_block_number) for x in pagination.items
        ]
        pagination_info_dto = PaginationDTO(
            current_page=pagination.page,
            page_size=pagination.per_page,
            total=pagination.total or 0,
            total_pages=pagination.pages
        )
        return AuditLogSearchResponsePaginationDTO(
            data=data_dto_list,
            pagination=pagination_info_dto
        )


if __name__ == '__main__':
    from app import create_app

    fake_app = create_app()
    with fake_app.app_context():
        res = AuditLogMapper.SearchAuditLogs()
        print(res)

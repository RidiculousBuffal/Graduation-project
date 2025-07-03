from app.mapper.audit.AuditMapper import AuditLogMapper
from app.models.response import ResponseModel


class AuditlogService:
    @staticmethod
    def searchAuditLog(page_num, page_size):
        res = AuditLogMapper.SearchAuditLogs(page_num=page_num, page_size=page_size)
        return ResponseModel.success(msg="success", data=res.model_dump()).to_dict()

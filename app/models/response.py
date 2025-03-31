from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ResponseModel:
    """统一 API 响应格式"""
    code: int
    msg: str
    data: Optional[Any] = None

    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }

    @staticmethod
    def fail(msg: str, data: Optional[Any] = None):
        return ResponseModel(code=1, msg=msg, data=data)

    @staticmethod
    def success(msg: str, data: Optional[Any] = None):
        return ResponseModel(code=0, msg=msg, data=data)



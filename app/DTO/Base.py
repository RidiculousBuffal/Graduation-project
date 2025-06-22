from datetime import datetime

from pydantic import ConfigDict, BaseModel, model_serializer


class BaseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # 统一覆盖所有字段里出现的 datetime
    @model_serializer
    def ser_model(self):
        # 递归地序列化模块所有datetime为ISO8601字符串
        return {
            k: (v.isoformat() if isinstance(v, datetime) else v)
            for k, v in self.__dict__.items()
        }

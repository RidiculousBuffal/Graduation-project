from functools import wraps

from flask_jwt_extended import get_jwt_identity
from app.DTO.Audit import ActionDTO
from app.web3.Web3Client import myWeb3Client


def logging_to_blockchain(event_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            input_para = {}
            try:
                from flask import request
                input_para = {
                    "args": request.args.to_dict(),
                    "jsons": request.get_json(silent=True),
                    "path": request.path
                }
            except Exception:
                pass
            result = func(*args, **kwargs)
            action = ActionDTO(userId=user_id, event_name=event_name, result=result, input_parameter=input_para)
            myWeb3Client.syncToBlockChain(action)
            return result

        return wrapper

    return decorator

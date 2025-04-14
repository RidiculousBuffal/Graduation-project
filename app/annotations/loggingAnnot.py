from functools import wraps

from flask_jwt_extended import get_jwt_identity

from app.DTO.Audit import ActionDTO
from app.consts.Web3 import Web3Consts
from app.models.response import ResponseModel
from app.web3.Web3Client import myWeb3Client


def logging_to_blockchain(event_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                user_id = get_jwt_identity()
                result = func(*args, **kwargs)
                action = ActionDTO(userId=user_id, event_name=event_name, result=result)
                myWeb3Client.syncToBlockChain(action)
                return result
            except Exception as e:
                return ResponseModel.fail(Web3Consts.SYNC_TO_BLOCKCHAIN_FAILED).to_dict(), 200

        return wrapper

    return decorator

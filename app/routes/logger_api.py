from flask import Blueprint, request

from app.annotations.permissionAnnot import permission_required
from app.consts.Permissions import Permissions
from app.models.response import ResponseModel
from app.service.AuditlogService import AuditlogService
from app.web3.Web3Client import myWeb3Client

logger_bp = Blueprint('logger', __name__)


@logger_bp.get("/blockChainStatus")
def logger():
    abi = myWeb3Client.CONTRACT_ABI
    address = myWeb3Client.CONTRACT_ADDRESS
    url = myWeb3Client.RPC_URL
    status = "connected"
    res = {
        "abi": abi,
        "address": address,
        "url": url,
        "status": status
    }
    return ResponseModel.success(data=res, msg="success").to_dict(), 200


@logger_bp.get("/searchAuditLog")
@permission_required(permissions=Permissions.LOG_READ.get("permission_name"),all_required=True)
def searchAuditLog():
    args = request.args.to_dict()
    page_num = int(args.get("current_page", 1))
    page_size = int(args.get("page_size", 10))
    return AuditlogService.searchAuditLog(page_num, page_size), 200

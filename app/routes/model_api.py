from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.consts.InspectionModel import InspectionModelConsts
from app.models.response import ResponseModel
from app.service.modelService import ModelService

model_bp = Blueprint('model_bp', __name__)


@model_bp.route('/getmodels', methods=['GET'])
@jwt_required()
def get_models():
    return ResponseModel.success(msg=InspectionModelConsts.SEARCH_MODEL_SUCCESS,
                                 data=ModelService.get_all_models()).to_dict(), 200

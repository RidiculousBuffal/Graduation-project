from app.DTO.model import ModelDTO
from app.ext.extensions import db
from app.models import Model


class ModelMapper:
    @staticmethod
    def get_all_models():
        models = db.session.query(Model).all()
        return [ModelDTO.model_validate(m.to_dict()) for m in models]

    @staticmethod
    def get_model_by_id(model_id: str):
        model = db.session.query(Model).filter(Model.model_id == model_id).first()
        return ModelDTO.model_validate(model.to_dict())


if __name__ == '__main__':
    from app import create_app

    fake_app = create_app()
    with fake_app.app_context():
        res = ModelMapper.get_model_by_id('a2b7010b-425b-47a5-a004-2e73f9e6a314')
        print(res)

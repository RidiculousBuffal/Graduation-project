from app.DTO.model import ModelDTO
from app.ext.extensions import db
from app.models import Model


class ModelMapper:
    @staticmethod
    def get_all_models():
        models = db.session.query(Model).all()
        return [ModelDTO.model_validate(m.to_dict()) for m in models]


if __name__ == '__main__':
    from app import create_app

    fake_app = create_app()
    with fake_app.app_context():
        res = ModelMapper.get_all_models()
        print(res)

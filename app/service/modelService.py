from app.mapper.model.modelMapper import ModelMapper


class ModelService:
    @staticmethod
    def get_all_models():
        return [m.model_dump() for m in ModelMapper.get_all_models()]

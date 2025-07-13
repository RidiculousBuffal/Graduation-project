import os

from app import celery
from app.DTO.file import FileDTO
from app.DTO.inspectionItems import YoloResult
from app.lib.yolo.YoloDetect import yolodetect
from app.mapper.model.modelMapper import ModelMapper
from app.mapper.tasks.inspectionItemMapper import InspectionItemMapper
from app.service.ipfsService import IPFSService_

#
@celery.task
def detect_images():
    # 1. 拿到所有pending状态的inspection_item
    items = InspectionItemMapper.get_items_by_progress('pending')
    for item in items:
        for res in item.result:
            if res.progress == 'pending':
                try:
                    input_image = res.inputImage
                    file_path, file_name = IPFSService_.download_file(input_image)
                    if file_name is None:
                        res.progress = 'error'
                    else:
                        model_id = item.model_id
                        model = ModelMapper.get_model_by_id(model_id)
                        api_path = model.model_api_path
                        save_dir, boxes,is_passed = yolodetect.detect(file_path, api_path)
                        base_filename, _ = os.path.splitext(file_name)
                        output_filename = f"{base_filename}.jpg"
                        final_path = os.path.join(save_dir, output_filename)
                        with open(final_path, 'rb') as file_obj:
                            upload_res = IPFSService_.upload_file(file_obj, filename=file_name, add_timestamp=True)
                            final_result = YoloResult(resultImage=FileDTO.model_validate(upload_res), boxes=boxes)
                            res.progress = 'done'
                            res.resultImage = final_result
                            res.isPassed=is_passed
                except Exception as e:
                    res.progress = 'error'
                    print(e)
        InspectionItemMapper.update(item.item_id,item)

if __name__ == '__main__':
    from app import create_app

    fake_app = create_app()
    with fake_app.app_context():
        detect_images()
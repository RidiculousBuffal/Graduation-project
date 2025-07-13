import os
import dotenv

from app.DTO.inspectionItems import YoloResult, YoloBoxDTO, YoloDetect as YoloDetectDTO

dotenv.load_dotenv()
from ultralytics import YOLO


class YoloDetect:
    def __init__(self):
        self.YOLO_SAVE_PATH = os.getenv('YOLO_SAVE_PATH')

    def detect(self, image_path: str, api_path: str):
        model = YOLO(api_path)
        results = model(image_path, project=self.YOLO_SAVE_PATH, save=True, name='result')
        res = results[0]
        save_dir = res.save_dir
        boxes: list[YoloDetectDTO] = []
        is_passed=True
        for xyxy, conf, cls in zip(res.boxes.xyxy, res.boxes.conf, res.boxes.cls):
            x1, y1, x2, y2 = xyxy.cpu().numpy()
            yolo_box = YoloBoxDTO(x1=x1, y1=y1, x2=x2, y2=y2)
            conf_value = float(conf.cpu().numpy())  # 或者 conf.item()
            cls_id = int(cls.cpu().numpy())  # 或者 cls.item()
            label = res.names[cls_id]  # 从名字映射表里取出文字标签
            if conf_value>0.25:
                is_passed=False
            boxes.append(YoloDetectDTO(points=yolo_box, label=label, confidence=conf_value))
        return save_dir, boxes,is_passed

yolodetect = YoloDetect()
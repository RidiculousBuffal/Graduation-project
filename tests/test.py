# 加载模型
from ultralytics import YOLO

model = YOLO(r"./best.pt")

# 检测单张图片
results = model(r"C:\Users\Administrator\Downloads\NEU-DET\NEU-DET\IMAGES\scratches_186.jpg", project=r"E:\codes\large_passenger_aircraft_yolo_train", name="test", save_txt=True ,save_crop=True)  # 推理
[r.save() for r in results]
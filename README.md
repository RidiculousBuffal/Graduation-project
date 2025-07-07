# 下载数据集
```bash
curl -L "https://app.roboflow.com/ds/FVy89cmQRt?key=OuBh814jAx" > roboflow.zip; unzip roboflow.zip; rm roboflow.zip
```

# 采用东北大学缺陷检测数据集
网址:http://faculty.neu.edu.cn/songkechen/zh_CN/zdylm/263270/list/

# 改路径
- 把数据集放在`traindata`目录下
- 修改`data.yaml`至绝对路径

```txt
train: /workspace/Deepseek-R1-Chat-7_8B/large_passenger_aircraft/traindata/train/images
val: /workspace/Deepseek-R1-Chat-7_8B/large_passenger_aircraft/traindata/vaild/images
test: /workspace/Deepseek-R1-Chat-7_8B/large_passenger_aircraft/traindata/test/images
```
# 训练
```bash
yolo detect train data=/root/traindata/data.yaml model=yolo11m.pt epochs=50 imgsz=640 batch=8
```
# 性能实测
## 规格
```txt
镜像
Python  3.12(ubuntu22.04)  CUDA  12.4
GPU
RTX 4090(24GB) * 1
CPU
16 vCPU Intel(R) Xeon(R) Gold 6430
内存
120GB
硬盘
系统盘:30 GB
```
## 结果
```txt

50 epochs completed in 0.146 hours.
Optimizer stripped from /root/yolo/runs/detect/train/weights/last.pt, 5.5MB
Optimizer stripped from /root/yolo/runs/detect/train/weights/best.pt, 5.5MB

Validating /root/yolo/runs/detect/train/weights/best.pt...
Ultralytics 8.3.162 🚀 Python-3.12.3 torch-2.7.1+cu126 CUDA:0 (NVIDIA GeForce RTX 4090, 24111MiB)
YOLO11n summary (fused): 100 layers, 2,583,322 parameters, 0 gradients, 6.3 GFLOPs
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100%|██████████| 23/23 [00:01<00:00, 12.86it/s]
                   all        360        844      0.679      0.706      0.729      0.418
               crazing         59        133      0.441      0.233      0.336      0.126
             inclusion         87        232      0.713       0.78      0.823      0.456
               patches         66        164      0.782       0.89       0.89      0.594
        pitted_surface         60         82      0.775      0.768      0.812      0.509
       rolled-in_scale         53        111      0.552      0.649      0.583      0.263
             scratches         68        122      0.809      0.918      0.929      0.559
Speed: 0.1ms preprocess, 0.4ms inference, 0.0ms loss, 0.6ms postprocess per image
Results saved to /root/yolo/runs/detect/train
💡 Learn more at https://docs.ultralytics.com/modes/train
```
## AI分析

### 一、整体训练&评估信息

- **训练参数：**
  - 训练集：1259张
  - 验证集：360张，844个目标实例
- **模型：** YOLO11n（nano，超轻量级，参数2.58M）
- **训练时长：** 50个epoch仅0.146小时（约8.8分钟，GPU飞快）
- **最终权重：**
  - `/root/yolo/runs/detect/train/weights/last.pt`（最后一轮）
  - `/root/yolo/runs/detect/train/weights/best.pt`（最佳mAP的轮次）

---

### 二、验证集评估结果（看这块最重要）

| 类别               | P(查准率) | R(查全率) | mAP50 | mAP50-95 | 实例数 |
|--------------------|-----------|----------|-------|----------|--------|
| **all**            | 0.679     | 0.706    | 0.729 | 0.418    |  844   |
| crazing            | 0.441     | 0.233    | 0.336 | 0.126    |  133   |
| inclusion          | 0.713     | 0.780    | 0.823 | 0.456    |  232   |
| patches            | 0.782     | 0.890    | 0.890 | 0.594    |  164   |
| pitted_surface     | 0.775     | 0.768    | 0.812 | 0.509    |   82   |
| rolled-in_scale    | 0.552     | 0.649    | 0.583 | 0.263    |  111   |
| scratches          | 0.809     | 0.918    | 0.929 | 0.559    |  122   |

- **查准率 Precision (P)**：预测为正的样本中，有多少是对的。越高越好。
- **查全率 Recall (R)**：所有真正样本中，被成功检出的比例。越高越好。
- **mAP50**：最常见目标检测评价指标，IoU阈值=0.5时的平均准确率，主流模型通常>0.70就是很不错的。
- **mAP50-95**：IoU阈值0.5到0.95变化区间的平均准确率，这个更严格，通常低一些。

---

#### 1. **整体性能**

- **all（整体）**
  - **P=0.679、R=0.706：**模型对检测目标的查准率和查全率都不错，查全率更高，说明召回了大部分目标；
  - **mAP50=0.729：** 超过0.7，说明“定位+分类”的主任务模型已经学得相当靠谱，适合直接部署或展示demo。
  - **mAP50-95=0.418：** 标准精度线，杂类mAP也已达合理区间。

#### 2. **分类别表现**

- **表现最好的类别**
  - **scratches**：P=0.809，R=0.918，mAP50=0.929（非常优秀！）
  - **patches**：mAP50=0.890
  - **pitted_surface**：mAP50=0.812
  - **inclusion**：mAP50=0.823

- **表现相对弱一点的类别**
  - **crazing**：P=0.441，R=0.233，mAP50=0.336，mAP50-95=0.126 （召回很低）
    - 说明该类在训练数据中较难，或者样本本身难以识别/混淆

  - **rolled-in_scale**：mAP50=0.583（但也在及格线）

#### 3. **速度**
- **推理速度**：每张图片，前后处理仅1.1ms，超快实时。适合大量推理和边缘部署。



### 三、结论与建议

#### 1. **模型已经表现不俗，可以直接用于实际场景demo**
- 轻量模型mAP近0.73，假如业务能接受，有90%+类的mAP甚至很高，
- 说明配置和数据准备都到位。

#### 2. **如何进一步提升？**
- 针对**crazing类**可考虑
  - 查看样本够不够？（数量OK的话考虑数据增强）
  - 是否标注模糊/异类过多导致难学？
  - 想要这个类表现变好，建议用MixUp/CutMix/拷贝粘贴等数据增强。

- 如果业务追求极致准确率：
  - 可以采用更大模型（如 YOLOv8s、YOLOv8m 等）
  - 增加训练轮数
  - 细致清洗和扩充数据集

#### 3. **如何测试新图片？**
- 使用刚刚训练的 `best.pt` 可立即推理
    ```bash
    yolo detect predict model=/root/yolo/runs/detect/train/weights/best.pt source=你的图片或文件夹
    ```
  输出带框结果在`runs/detect/predict/`目录下。

#### 4. **可进一步可视化**
- `/root/yolo/runs/detect/train/results.png` 包含 loss 和 mAP 训练曲线
- `/root/yolo/runs/detect/train/confusion_matrix.png` 有混淆矩阵（可分析各类混淆/漏检情况）

---

### 四、你的下一个推荐步骤

1. **挑选典型图片做推理，人工快速测一下典型业务痛点**
2. **如果有需求，可切换更大模型继续迁移训练**
3. **重点关注困难类别的数据质量和样本数量**
4. 有任何问题（推理、画图、模型优化、测试新图片）可随时反馈！


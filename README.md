# 下载数据集
```bash
curl -L "https://app.roboflow.com/ds/FVy89cmQRt?key=OuBh814jAx" > roboflow.zip; unzip roboflow.zip; rm roboflow.zip
```

# 采用东北大学缺陷检测数据集
网址:http://faculty.neu.edu.cn/songkechen/zh_CN/zdylm/263270/list/

# 该路径
- 把数据集放在`traindata`目录下
- 修改`data.yaml`至绝对路径

```txt
train: /workspace/Deepseek-R1-Chat-7_8B/large_passenger_aircraft/traindata/train/images
val: /workspace/Deepseek-R1-Chat-7_8B/large_passenger_aircraft/traindata/vaild/images
test: /workspace/Deepseek-R1-Chat-7_8B/large_passenger_aircraft/traindata/test/images
```
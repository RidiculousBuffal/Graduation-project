# 飞机底图+点位上传

## 前端示例:

点位示例可参考:[**https://zlcimageannot.zeabur.app/**](https://zlcimageannot.zeabur.app/)

![](http://www.kdocs.cn/api/v3/office/copy/SnFjTzZaZENqbFVxRUcyR1U1YU10RE1XYXIwSTNGQ2dpbEFsNzJzaGNZaEoxSzRaUmtSWGNQQUU0anBlRXNKczVLdmlMQ1h2dVhnbCtmdnFpZGxQZlhhQThkOWtqaW83bVZSNUQyNWR4L0VnK05OblJmUlpZOFZXdW5SNVJTNm1HbkZiVnhWMHY5RTBNZkVzQS90d0t3MENtSWhTTDE5a3hNZWdITjBIaDgrcUdoQVN5Q2l0eGxCYmU0ek5kSFZ5M2NHa0xha2gxR2pDd2lqbU4wTk5sTndaVEVhQ1gwWEhYTzVucGwxSGFZMGpLOWFoU3NmMmtkUFVQS3gzYU1KRVdBTy9RUDRIcExZPQ==/attach/object/AGT7PCA7ADQF4?)

## 接口地址

```bash
/aircraft/createAircraftImage
```

## 传入参数

要求鉴权:是

请求方式:`POST`

传入方式:`json`

要求权限:`AIRCRAFT.IMAGE.ADD`

|参数名|描述|是否必须|类型|
|-|-|-|-|
|`image_name`|图片名|是|`string`|
|`image_description`|图片描述|否|`string`|
|`image_json`|图片json点位[见下方]|是|`obect`|
|`image_json.fileInfo`|图片文件信息|是|上传文件到IPFS的返回值的data字段|
|`image_json.pointInfo`|图片点位信息|是|`array`|
|`image_json.pointInfo.id`|图片点位id|是|`int`|
|`image_json.pointInfo.x`|图片点位横坐标|是|`float`|
|`image_json.pointInfo.y`|图片点位纵坐标|是|`float`|


参考:

```json
{
    "image_name":"飞机底图1",
    "image_description":"地图描述",
    "aircraft_id":"AC008",
    "image_json":{
        "fileInfo":
            {
                "download_url": "http://localhost:8080/ipfs/QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg?filename=lingxi-export.png",
                "filename": "lingxi-export.png",
                "ipfs_cid": "QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg",
                "ipfs_path": "/ipfs/QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg",
                "mfs_path": "/uploads/2025-04-17/lingxi-export_1744898162.png",
                "mime_type": "image/png",
                "size": 816287,
                "stored_filename": "lingxi-export_1744898162.png",
                "success": true,
                "uploaded_at": "2025-04-17T21:56:23.249354"
            },
  "pointInfo":[
        {"id":1,"x":10.5,"y":20.5},
        {"id":2,"x":10.5,"y":30.5}
        
    ]
        
    }
}
```

## 返回值——成功

`aircraft_name`始终为`null`是正常的,只有在`search`接口的时候不为`null`

```json
{
    "code": 0,
    "data": {
        "aircraft_id": "AC008",
        "aircraft_name": null,
        "image_description": "地图描述",
        "image_id": "57d13dc8-61d4-4a12-b0fe-096ceb04d8fe",
        "image_json": {
            "fileInfo": {
                "download_url": "http://localhost:8080/ipfs/QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg?filename=lingxi-export.png",
                "filename": "lingxi-export.png",
                "ipfs_cid": "QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg",
                "ipfs_path": "/ipfs/QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg",
                "mfs_path": "/uploads/2025-04-17/lingxi-export_1744898162.png",
                "mime_type": "image/png",
                "size": 816287,
                "stored_filename": "lingxi-export_1744898162.png",
                "success": true,
                "uploaded_at": "2025-04-17T21:56:23.249354"
            },
            "pointInfo": [
                {
                    "id": 1,
                    "x": 10.5,
                    "y": 20.5
                },
                {
                    "id": 2,
                    "x": 10.5,
                    "y": 30.5
                }
            ]
        },
        "image_name": "飞机底图1"
    },
    "msg": "添加飞机参考图片成功"
}
```

## 返回值——文件类型不是图片

```json
{
    "code": 1,
    "data": {
        "error": "文件必须是图片格式（mime 类型需以 'image/' 开头）"
    },
    "msg": "飞机参考图片数据无效"
}
```

## 请求示例

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDg5NzEwOCwianRpIjoiMTU4NmNjYjUtMGY4NC00NjBkLWJjZTctMjAwMWNiZDRjMzUyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NDg5NzEwOCwiY3NyZiI6Ijg1YzFhMDZiLTIzYjItNDQ1Ny1hNzVmLTNhN2EyNWQ4ODk1NSIsImV4cCI6MTc0NDk4MzUwOH0.hOe-8NfPgOPHHFBYmyrAhhufEBz0klT7JwFKuaIPfb0");
myHeaders.append("User-Agent", "Apifox/1.0.0 (https://apifox.com)");
myHeaders.append("Content-Type", "application/json");
myHeaders.append("Accept", "*/*");
myHeaders.append("Host", "localhost:5000");
myHeaders.append("Connection", "keep-alive");
var raw = JSON.stringify({
   "image_name": "飞机底图5",
   "image_description": "地图描述",
   "aircraft_id": "AC008",
   "image_json": {
      "fileInfo": {
         "download_url": "http://localhost:8080/ipfs/QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg?filename=lingxi-export.png",
         "filename": "lingxi-export.png",
         "ipfs_cid": "QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg",
         "ipfs_path": "/ipfs/QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg",
         "mfs_path": "/uploads/2025-04-17/lingxi-export_1744898162.png",
         "mime_type": "image/png",
         "size": 816287,
         "stored_filename": "lingxi-export_1744898162.png",
         "success": true,
         "uploaded_at": "2025-04-17T21:56:23.249354"
      },
      "pointInfo": [
         {
            "id": 1,
            "x": 10.5,
            "y": 20.5
         },
         {
            "id": 2,
            "x": 10.5,
            "y": 30.5
         }
      ]
   }
});
var requestOptions = {
   method: 'POST',
   headers: myHeaders,
   body: raw,
   redirect: 'follow'
};
fetch("http://localhost:5000/api/aircraft/createAircraftImage", requestOptions)
   .then(response => response.text())
   .then(result => console.log(result))
   .catch(error => console.log('error', error));
```

# 飞机底图更新

## 接口地址

```bash
/aircraft/updateAircraftImage/<string:image_id>
```

## 传入参数

要求鉴权:是

请求方式:`POST`

传入方式:`地址参数+JSON`

要求权限:`AIRCRAFT.IMAGE.UPDATE`

|||||
|-|-|-|-|
|参数名|描述|是否必须|类型|
|`image_name`|图片名|是|`string`|
|`image_description`|图片描述|否|`string`|
|`image_json`|图片json点位[见下方]|是|`obect`|
|`image_json.fileInfo`|图片文件信息|是|上传文件到IPFS的返回值的data字段|
|`image_json.pointInfo`|图片点位信息|是|`array`|
|`image_json.pointInfo.id`|图片点位id|是|`int`|
|`image_json.pointInfo.x`|图片点位横坐标|是|`float`|
|`image_json.pointInfo.y`|图片点位纵坐标|是|`float`|


## 返回值——成功

```json
{
    "code": 0,
    "data": {
        "aircraft_id": "AC008",
        "aircraft_name": null,
        "image_description": "地图描述",
        "image_id": "c67c4ae5-ce64-4199-a5e7-0b68ae83406f",
        "image_json": {
            "fileInfo": {
                "download_url": "http://localhost:8080/ipfs/QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg?filename=lingxi-export.png",
                "filename": "lingxi-export.png",
                "ipfs_cid": "QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg",
                "ipfs_path": "/ipfs/QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg",
                "mfs_path": "/uploads/2025-04-17/lingxi-export_1744898162.png",
                "mime_type": "image/png",
                "size": 816287,
                "stored_filename": "lingxi-export_1744898162.png",
                "success": true,
                "uploaded_at": "2025-04-17T21:56:23.249354"
            },
            "pointInfo": [
                {
                    "id": 1,
                    "x": 10.5,
                    "y": 20.5
                },
                {
                    "id": 2,
                    "x": 10.5,
                    "y": 30.5
                }
            ]
        },
        "image_name": "飞机底图更新"
    },
    "msg": "更新飞机参考图片成功"
}
```

## 请求示例

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDg5NzEwOCwianRpIjoiMTU4NmNjYjUtMGY4NC00NjBkLWJjZTctMjAwMWNiZDRjMzUyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NDg5NzEwOCwiY3NyZiI6Ijg1YzFhMDZiLTIzYjItNDQ1Ny1hNzVmLTNhN2EyNWQ4ODk1NSIsImV4cCI6MTc0NDk4MzUwOH0.hOe-8NfPgOPHHFBYmyrAhhufEBz0klT7JwFKuaIPfb0");
myHeaders.append("User-Agent", "Apifox/1.0.0 (https://apifox.com)");
myHeaders.append("Content-Type", "application/json");
myHeaders.append("Accept", "*/*");
myHeaders.append("Host", "localhost:5000");
myHeaders.append("Connection", "keep-alive");
var raw = JSON.stringify({
   "image_name": "飞机底图更新",
   "image_description": "地图描述",
   "aircraft_id": "AC008",
   "image_json": {
      "fileInfo": {
         "download_url": "http://localhost:8080/ipfs/QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg?filename=lingxi-export.png",
         "filename": "lingxi-export.png",
         "ipfs_cid": "QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg",
         "ipfs_path": "/ipfs/QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg",
         "mfs_path": "/uploads/2025-04-17/lingxi-export_1744898162.png",
         "mime_type": "image/png",
         "size": 816287,
         "stored_filename": "lingxi-export_1744898162.png",
         "success": true,
         "uploaded_at": "2025-04-17T21:56:23.249354"
      },
      "pointInfo": [
         {
            "id": 1,
            "x": 10.5,
            "y": 20.5
         },
         {
            "id": 2,
            "x": 10.5,
            "y": 30.5
         }
      ]
   }
});
var requestOptions = {
   method: 'POST',
   headers: myHeaders,
   body: raw,
   redirect: 'follow'
};
fetch("http://localhost:5000/api/aircraft/updateAircraftImage/c67c4ae5-ce64-4199-a5e7-0b68ae83406f", requestOptions)
   .then(response => response.text())
   .then(result => console.log(result))
   .catch(error => console.log('error', error));
```

# 飞机底图删除

## 接口地址

```bash
/aircraft/deleteAircraftImage/<string:image_id>
```

## 传入参数

要求鉴权:是

请求方式:`DELETE`

传入方式:`地址参数+JSON`

要求权限:`AIRCRAFT.IMAGE.UPDATE`

## 返回值——删除成功

```json
{
  "code": 0,
  "data": null,
  "msg": "删除飞机参考图片成功"
}
```

## 返回值——id不存在

```json
{
  "code": 1,
  "data": {
    "error": "未找到ID为e7e7846e-01f9-4f43-9e16-3eaf145dfd74的飞机参考图片或删除失败"
  },
  "msg": "删除飞机参考图片失败"
}
```

## 请求示例

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDg5NzEwOCwianRpIjoiMTU4NmNjYjUtMGY4NC00NjBkLWJjZTctMjAwMWNiZDRjMzUyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NDg5NzEwOCwiY3NyZiI6Ijg1YzFhMDZiLTIzYjItNDQ1Ny1hNzVmLTNhN2EyNWQ4ODk1NSIsImV4cCI6MTc0NDk4MzUwOH0.hOe-8NfPgOPHHFBYmyrAhhufEBz0klT7JwFKuaIPfb0");
myHeaders.append("User-Agent", "Apifox/1.0.0 (https://apifox.com)");
myHeaders.append("Accept", "*/*");
myHeaders.append("Host", "localhost:5000");
myHeaders.append("Connection", "keep-alive");
var requestOptions = {
   method: 'DELETE',
   headers: myHeaders,
   redirect: 'follow'
};
fetch("http://localhost:5000/api/aircraft/deleteAircraftImage/e7e7846e-01f9-4f43-9e16-3eaf145dfd74", requestOptions)
   .then(response => response.text())
   .then(result => console.log(result))
   .catch(error => console.log('error', error));
```

# 根据底图id获得详细信息

## 接口地址

```bash
/aircraft/getAircraftImage/c67c4ae5-ce64-4199-a5e7-0b68ae83406f
```

## 传入参数

要求鉴权:是

请求方式:`GET`

传入方式:`地址参数`

要求权限:`AIRCRAFT.IMAGE.READ`

## 返回值——成功

```bash
{
    "code": 0,
    "data": {
        "aircraft_id": "AC008",
        "aircraft_name": null,
        "image_description": "地图描述",
        "image_id": "c67c4ae5-ce64-4199-a5e7-0b68ae83406f",
        "image_json": {
            "fileInfo": {
                "download_url": "http://localhost:8080/ipfs/QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg?filename=lingxi-export.png",
                "filename": "lingxi-export.png",
                "ipfs_cid": "QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg",
                "ipfs_path": "/ipfs/QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg",
                "mfs_path": "/uploads/2025-04-17/lingxi-export_1744898162.png",
                "mime_type": "image/png",
                "size": 816287,
                "stored_filename": "lingxi-export_1744898162.png",
                "success": true,
                "uploaded_at": "2025-04-17T21:56:23.249354"
            },
            "pointInfo": [
                {
                    "id": 1,
                    "x": 10.5,
                    "y": 20.5
                },
                {
                    "id": 2,
                    "x": 10.5,
                    "y": 30.5
                }
            ]
        },
        "image_name": "飞机底图4"
    },
    "msg": "获取飞机参考图片信息成功"
}
```

## 请求示例

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDg5NzEwOCwianRpIjoiMTU4NmNjYjUtMGY4NC00NjBkLWJjZTctMjAwMWNiZDRjMzUyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NDg5NzEwOCwiY3NyZiI6Ijg1YzFhMDZiLTIzYjItNDQ1Ny1hNzVmLTNhN2EyNWQ4ODk1NSIsImV4cCI6MTc0NDk4MzUwOH0.hOe-8NfPgOPHHFBYmyrAhhufEBz0klT7JwFKuaIPfb0");
myHeaders.append("User-Agent", "Apifox/1.0.0 (https://apifox.com)");
myHeaders.append("Accept", "*/*");
myHeaders.append("Host", "localhost:5000");
myHeaders.append("Connection", "keep-alive");
var requestOptions = {
   method: 'GET',
   headers: myHeaders,
   redirect: 'follow'
};
fetch("http://localhost:5000/api/aircraft/getAircraftImage/c67c4ae5-ce64-4199-a5e7-0b68ae83406f", requestOptions)
   .then(response => response.text())
   .then(result => console.log(result))
   .catch(error => console.log('error', error));
```

# 分页查询飞机底图

## 接口地址

```bash
/aircraft/searchAircraftImage
```

## 传入参数

要求鉴权:是

请求方式:`GET`

传入方式:`Query`

要求权限:`AIRCRAFT.IMAGE.READ`

||||
|-|-|-|
|参数名|描述|是否必须|
|`**image_name**`|飞机类型名|否|
|`**aircraft_id**`|飞机id|否|
|`**aircraft_name**`|飞机名|否|
|**current_page**|当前页数|否|
|`**page_size**`|每页展示条数|否|


## 返回值——成功

```json
{
  "code": 0,
  "data": {
    "data": [
      {
        "aircraft_id": "AC008",
        "aircraft_name": "Storm Theta",
        "image_description": "地图描述",
        "image_id": "57d13dc8-61d4-4a12-b0fe-096ceb04d8fe",
        "image_json": {
          "fileInfo": {
            "download_url": "http://localhost:8080/ipfs/QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg?filename=lingxi-export.png",
            "filename": "lingxi-export.png",
            "ipfs_cid": "QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg",
            "ipfs_path": "/ipfs/QmQwSQkVkHrcGUKcSnGR4i4K9PswH6jTkhqxaRBtFaRQgg",
            "mfs_path": "/uploads/2025-04-17/lingxi-export_1744898162.png",
            "mime_type": "image/png",
            "size": 816287,
            "stored_filename": "lingxi-export_1744898162.png",
            "success": true,
            "uploaded_at": "2025-04-17T21:56:23.249354"
          },
          "pointInfo": [
            {
              "id": 1,
              "x": 10.5,
              "y": 20.5
            },
            {
              "id": 2,
              "x": 10.5,
              "y": 30.5
            }
          ]
        },
        "image_name": "飞机底图1"
      }
    ],
    "pagination": {
      "current_page": 1,
      "page_size": 1,
      "total": 3,
      "total_pages": 3
    }
  },
  "msg": "查询飞机参考图片列表成功"
}
```

## 请求示例

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDg5NzEwOCwianRpIjoiMTU4NmNjYjUtMGY4NC00NjBkLWJjZTctMjAwMWNiZDRjMzUyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NDg5NzEwOCwiY3NyZiI6Ijg1YzFhMDZiLTIzYjItNDQ1Ny1hNzVmLTNhN2EyNWQ4ODk1NSIsImV4cCI6MTc0NDk4MzUwOH0.hOe-8NfPgOPHHFBYmyrAhhufEBz0klT7JwFKuaIPfb0");
myHeaders.append("User-Agent", "Apifox/1.0.0 (https://apifox.com)");
myHeaders.append("Accept", "*/*");
myHeaders.append("Host", "localhost:5000");
myHeaders.append("Connection", "keep-alive");
var requestOptions = {
   method: 'GET',
   headers: myHeaders,
   redirect: 'follow'
};
fetch("http://localhost:5000/api/aircraft/searchAircraftImage?image_name=&aircraft_id=&aircraft_name=Storm%20Theta&current_page=1&page_size=1", requestOptions)
   .then(response => response.text())
   .then(result => console.log(result))
   .catch(error => console.log('error', error));
```
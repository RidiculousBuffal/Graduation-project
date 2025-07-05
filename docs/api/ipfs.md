# 上传文件到IPFS——单文件上传

:::tip
需要安装配置IPFS`docker` 参考[docker/middleware/ipfs · github](https://github.com/RidiculousBuffal/Graduation-project/tree/dev_backend/docker/middleware/ipfs)
:::

## 接口地址

```bash
/ipfs/upload
```

## 传入参数

要求鉴权:是

请求方式:`POST`

传入方式:`Multipart-Formdata`

要求权限:`IPFS.FILE.UPLOAD`

|参数名|描述|是否必须|类型|
|-|-|-|-|
|`**file**`|单个文件|是|`file`二进制|
|`**directory**`|上传到的文件夹,不填默认`/upload`|否|`string`|
|`**add_timestamp**`|是否添加时间戳保证文件名不重复|否|`bool`|


## 返回值——成功

可以通过`download_url`来直接在前端展示,最好保留一下这个`json`的`data`部分,别的接口可能要传的。需要把前端的地址加入到`ipfs`的跨域请求中,参考

```Bash
ipfs config --json API.HTTPHeaders.Access-Control-Allow-Origin '["*"]'
```

```JSON
{
  "code": 0,
  "data": {
    "download_url": "http://localhost:8080/ipfs/QmRsb4LKbxKLzivwUkAukcuHrZxveNcL8ufWToSLDmsFsR?filename=%E5%90%B4%E5%9B%BD%E6%96%87.pdf",
    "filename": "吴国文.pdf",
    "ipfs_cid": "QmRsb4LKbxKLzivwUkAukcuHrZxveNcL8ufWToSLDmsFsR",
    "ipfs_path": "/ipfs/QmRsb4LKbxKLzivwUkAukcuHrZxveNcL8ufWToSLDmsFsR",
    "mfs_path": "/uploads/2025-04-13/吴国文_1744542851.pdf",
    "mime_type": "application/pdf",
    "size": 3561781,
    "stored_filename": "吴国文_1744542851.pdf",
    "success": true,
    "uploaded_at": "2025-04-13T19:14:11.371003"
  },
  "msg": "文件上传成功"
}
```

## 返回值——文件不存在(表单中未找到文件)

```JSON
{
  "code": 1,
  "data": null,
  "msg": "文件不存在"
}
```

## 请求示例

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDU0MjcxMSwianRpIjoiM2I5ZWUyMzItY2FlYS00MzU2LWI2NWItNzdhYTI0ZTJjNjk5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NDU0MjcxMSwiY3NyZiI6IjEzN2RlMTc0LTQ5OTAtNGI0Mi05NzkwLTJlNmYxNzVhZGUwOCIsImV4cCI6MTc0NDYyOTExMX0.IcUkEMJXqCGqgs1E9nlYK2NC_nfibmXqoFj7-pt880A");
myHeaders.append("User-Agent", "Apifox/1.0.0 (https://apifox.com)");
myHeaders.append("Accept", "*/*");
myHeaders.append("Host", "localhost:5000");
myHeaders.append("Connection", "keep-alive");
myHeaders.append("Content-Type", "multipart/form-data; boundary=--------------------------029882605920241107287595");
var formdata = new FormData();
formdata.append("file", fileInput.files[0], "C:\Users\Administrator\Downloads\吴国文.pdf");
var requestOptions = {
   method: 'POST',
   headers: myHeaders,
   body: formdata,
   redirect: 'follow'
};
fetch("http://localhost:5000/api/ipfs/upload", requestOptions)
   .then(response => response.text())
   .then(result => console.log(result))
   .catch(error => console.log('error', error));
```

# 上传文件到IPFS——并行批量上传

## 接口地址

```Markdown
/ipfs/upload/multiple
```

## 传入参数

要求鉴权:是

请求方式:`POST`

传入方式:`Multipart-Formdata`

要求权限:`IPFS.FILE.UPLOAD`

|参数名|描述|是否必须|类型|
|-|-|-|-|
|`**files**`|单个文件|是|`file`二进制|
|`**directory**`|上传到的文件夹,不填默认`/upload`|否|`string`|
|`**add_timestamp**`|是否添加时间戳保证文件名不重复,默认为是|否|`bool`|
|`**parallel**`|是否采用并行上传，默认为是|否|`bool`|


## 返回值——上传成功

```JSON
{
  "code": 0,
  "data": {
    "failed": 1,
    "invalid_files": [
      "案例分析.pptx.md"
    ],
    "results": [
      {
        "download_url": "http://localhost:8080/ipfs/QmRx2qaFUVPFonQZ7GnHkMNtR7z2k3UiXkrTDUwL64ybof?filename=585210030103011311.pdf",
        "filename": "585210030103011311.pdf",
        "ipfs_cid": "QmRx2qaFUVPFonQZ7GnHkMNtR7z2k3UiXkrTDUwL64ybof",
        "ipfs_path": "/ipfs/QmRx2qaFUVPFonQZ7GnHkMNtR7z2k3UiXkrTDUwL64ybof",
        "mfs_path": "/uploads/2025-04-13/585210030103011311_1744543368.pdf",
        "mime_type": "application/pdf",
        "size": 740739,
        "stored_filename": "585210030103011311_1744543368.pdf",
        "success": true,
        "uploaded_at": "2025-04-13T19:22:48.785643"
      }
    ],
    "success": true,
    "successful": 1,
    "total": 2
  },
  "msg": "文件上传成功"
}
```

## 请求示例

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDU0MjcxMSwianRpIjoiM2I5ZWUyMzItY2FlYS00MzU2LWI2NWItNzdhYTI0ZTJjNjk5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NDU0MjcxMSwiY3NyZiI6IjEzN2RlMTc0LTQ5OTAtNGI0Mi05NzkwLTJlNmYxNzVhZGUwOCIsImV4cCI6MTc0NDYyOTExMX0.IcUkEMJXqCGqgs1E9nlYK2NC_nfibmXqoFj7-pt880A");
myHeaders.append("User-Agent", "Apifox/1.0.0 (https://apifox.com)");
myHeaders.append("Accept", "*/*");
myHeaders.append("Host", "localhost:5000");
myHeaders.append("Connection", "keep-alive");
myHeaders.append("Content-Type", "multipart/form-data; boundary=--------------------------490421456580803628580455");
var formdata = new FormData();
formdata.append("parallel", "True");
formdata.append("files", fileInput.files[0], "C:\Users\Administrator\Downloads\案例分析.pptx.md");
formdata.append("files", fileInput.files[0], "C:\Users\Administrator\Downloads\585210030103011311.pdf");
var requestOptions = {
   method: 'POST',
   headers: myHeaders,
   body: formdata,
   redirect: 'follow'
};
fetch("http://localhost:5000/api/ipfs/upload/multiple", requestOptions)
   .then(response => response.text())
   .then(result => console.log(result))
   .catch(error => console.log('error', error));

```

![](http://www.kdocs.cn/api/v3/office/copy/SnFjTzZaZENqbFVxRUcyR1U1YU10RE1XYXIwSTNGQ2dpbEFsNzJzaGNZaEoxSzRaUmtSWGNQQUU0anBlRXNKczVLdmlMQ1h2dVhnbCtmdnFpZGxQZlhhQThkOWtqaW83bVZSNUQyNWR4L0VnK05OblJmUlpZOFZXdW5SNVJTNm1HbkZiVnhWMHY5RTBNZkVzQS90d0t3MENtSWhTTDE5a3hNZWdITjBIaDgrcUdoQVN5Q2l0eGxCYmU0ek5kSFZ5M2NHa0xha2gxR2pDd2lqbU4wTk5sTndaVEVhQ1gwWEhYTzVucGwxSGFZMGpLOWFoU3NmMmtkUFVQS3gzYU1KRVdBTy9RUDRIcExZPQ==/attach/object/ODELO4Y7ACQE6?)

![](http://www.kdocs.cn/api/v3/office/copy/SnFjTzZaZENqbFVxRUcyR1U1YU10RE1XYXIwSTNGQ2dpbEFsNzJzaGNZaEoxSzRaUmtSWGNQQUU0anBlRXNKczVLdmlMQ1h2dVhnbCtmdnFpZGxQZlhhQThkOWtqaW83bVZSNUQyNWR4L0VnK05OblJmUlpZOFZXdW5SNVJTNm1HbkZiVnhWMHY5RTBNZkVzQS90d0t3MENtSWhTTDE5a3hNZWdITjBIaDgrcUdoQVN5Q2l0eGxCYmU0ek5kSFZ5M2NHa0xha2gxR2pDd2lqbU4wTk5sTndaVEVhQ1gwWEhYTzVucGwxSGFZMGpLOWFoU3NmMmtkUFVQS3gzYU1KRVdBTy9RUDRIcExZPQ==/attach/object/BQCLQ4Y7AAAFU?)
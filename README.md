# 启动项目

## 安装uv

```bash
pip install uv 
```

## 安装依赖

```bash
uv sync 
```

## 配置环境变量

1. 配置数据库链接信息

```bash
cp .env.example .env
```

2. 自行创建数据库

- 只要创建数据库即可,不需要`create table`
- 创建完数据库自行填写`.env`文件夹的相关信息

## 执行数据库迁移
### pull
- **建议每次pull代码的时候执行一下(不执行默认第一次启动应用的时候自动执行)**  

```bash
flask db upgrade 
```
### push
- **建议每次push代码的时候执行一下（如果涉及到数据库更改）**

```bash
flask db migrate -m "迁移信息" 
```

## 启动区块链服务
根据[README.md](web3%2FREADME.md)自行启动区块链服务 \
随便找一个`private Key`填入`.env`文件的`PRIVATE_KEY`处:
![img.png](readmeimg%2Fimg.png) 
把合约地址填入到`.env`文件的`CONTRACT_ADDRESS`处
![img1.png](readmeimg%2Fimg1.png)
## 启动ipfs分布式文件存储
根据[install_windows_docker.md](docker%2Fmiddleware%2Fipfs%2Finstall_windows_docker.md)自行启动分布式文件存储服务

## 自动测试

- 在[tests](tests)中书写,查看单元测试
```bash
pytest 
```

## 启动项目
```bash
flask run
```
## 调试项目
在`pycharm`做如下配置,打断点调试即可:
![img_1.png](readmeimg%2Fimg_1.png)
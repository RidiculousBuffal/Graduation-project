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

## 执行数据库迁移

- **建议每次push的时候执行一下**

```bash
flask db upgrade 
```

## 部署webase

- 已经把docker镜像打包好了,直接拉镜像启动

```bash
docker run -d \
  -p 30300:30300 -p 30301:30301 -p 30302:30302 -p 30303:30303 \
  -p 20200:20200 -p 20201:20201 -p 20202:20202 -p 20203:20203 \
  -p 8545:8545 -p 8546:8546 -p 8547:8547 -p 8548:8548 \
  -p 5002:5002 \
  --name fisco-all-in-one \
  ridiculousbuffalo/fisco-webase-all-in-one:1.0.0
```

要自行构建镜像去[webase-fisco](docker%2Fmiddleware%2Fwebase-fisco)中自行`docker build`即可

## 自动测试

- 在[tests](tests)中书写,查看单元测试
```bash
pytest 
```
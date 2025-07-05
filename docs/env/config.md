
# 启动开发环境

## 方式一——直接使用云端环境作为api进行本地开发

我们的云端环境BaseUrl为:

```bash
https://largeaircraft.ridiculousbuffal.com/api
```

## 方式二——使用docker镜像+云端中间件开发

> 云端已经配置好各种中间件,只需要拉取镜像绑定环境变量即可在本地开发

在本地新建.env 一些隐私变量已经隐藏,见微信群中发的`.env`

```env
DB_USERNAME=root
DB_NAME=dhu_aircraft
CONTRACT_ADDRESS=xxxxxxxxxxxx
DB_PORT=31001
DB_HOST=43.167.245.135
IPFS_MAX_UPLOAD_WORKERS=4
IPFS_TIMESTAMP_FORMAT=timestamp
IPFS_HOST=http://43.167.245.135
RPC_URL=http://43.167.245.135:32055
DB_PASSWORD=xxxxxxxxxxxxxx
IPFS_USE_MFS=True
IPFS_GATEWAY_PORT=443
IPFS_GATEWAY=https://ipfs.ridiculousbuffal.com
PASSWORD=xxxxxxxxxxxxxxx
IPFS_MFS_BASE_DIR=/uploads
PRIVATE_KEY=xxxxxxxxxxxxxxxx
IPFS_PORT=30882
SECRET_KEY=8fd963757e9665ab4e7e48de885aa56c688fde4191da56bf54da9d10dfbb4b72
FLASK_ENV=production
WEAVIATE_HOST=43.167.245.135
WEAVIATE_API_KEY=xxxxxxxx
WEAVIATE_GRPC_PORT=31055
WEAVIATE_TCP_PORT=31441
OPENAI_BASE_URL=https://aihubmix.com/v1
OPENAI_API_KEY=sk-TWxxxxxxxxxxxxxxxxxxxxx5E4
CELERY_BROKER_URL=redis://localhost:6379/3
CELERY_RESULT_BACKEND=redis://localhost:6379/4
MODE=api/worker 
```

::: info
这里要准备2份`.env` 一份中`MODE=api` 另一份中`MODE=worker`
:::

::: warning
在`docker`容器中使用本地或者其他`docker`容器中的服务: `HOST`要从`ip`更改为`host.docker.internal`
:::

启动命令:

```bash
docker run --env-file .env -p 5050:5050 ridiculousbuffalo/large-aircraft-backend:latest
```

如果觉得某个中间件云端响应慢,可以在下面的链接中找到对应的中间件docker自行开发:
<GitCard
title="Docker 中间件"
description="Docker 中间件"
link="https://github.com/RidiculousBuffal/Graduation-project/tree/dev_backend/docker/middleware"
darkSrc="/github-mark-white.svg"
lightSrc="/github-mark.svg"
/>

`Hardhat` 区块链网络的现成镜像:
```bash
docker push ridiculousbuffalo/large-aircraft-hardhat:latest 
docker run -p 8545:8545 ridiculousbuffalo/large-aircraft-hardhat:latest 
```
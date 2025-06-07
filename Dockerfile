# 使用小体积的Python Alpine镜像作为基础
FROM python:3.12-alpine

# 设置工作目录
WORKDIR /app

# 安装uv包管理工具
RUN pip install --no-cache-dir uv

# 安装系统依赖项（如MySQL客户端所需的库）
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    mariadb-dev

# 复制项目文件
COPY pyproject.toml uv.lock ./
COPY app ./app
COPY migrations ./migrations
COPY scripts ./scripts
COPY run.py ./

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

# 使用uv sync安装依赖项
RUN uv sync

# 清理构建依赖，减小镜像体积
RUN apk del gcc musl-dev libffi-dev && \
    rm -rf /var/cache/apk/*

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "run.py"]

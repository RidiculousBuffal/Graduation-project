ARG APT_MIRROR_SOURCE=standard
FROM python:3.12-slim-bookworm AS builder

# 设置工作目录
WORKDIR /app
ARG PIP_INDEX_URL=https://pypi.org/simple
RUN pip config set global.index-url ${PIP_INDEX_URL}
# 使用 ARG，在需要时替换 apt 源
ARG APT_MIRROR_SOURCE
RUN if [ "$APT_MIRROR_SOURCE" = "aliyun" ]; then \
      sed -i 's@deb.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list.d/debian.sources && \
      sed -i 's@security.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list.d/debian.sources ; \
    elif [ "$APT_MIRROR_SOURCE" = "tsinghua" ]; then \
      sed -i 's@deb.debian.org@mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list.d/debian.sources && \
      sed -i 's@security.debian.org@mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list.d/debian.sources ; \
    fi

# 推荐版本锁定，生产更稳
RUN pip install --no-cache-dir uv==0.7.11

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libc-dev libffi-dev libmariadb-dev pkg-config

# 创建虚拟环境
RUN python -m venv /app/.venv

COPY pyproject.toml uv.lock ./
RUN /app/.venv/bin/python -m pip install --upgrade pip && \
    /app/.venv/bin/pip install uv && \
    /app/.venv/bin/uv sync --python /app/.venv/bin/python

# 生产镜像
FROM python:3.12-slim-bookworm AS production
ARG APT_MIRROR_SOURCE
RUN if [ "$APT_MIRROR_SOURCE" = "aliyun" ]; then \
      sed -i 's@deb.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list.d/debian.sources && \
      sed -i 's@security.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list.d/debian.sources ; \
    elif [ "$APT_MIRROR_SOURCE" = "tsinghua" ]; then \
      sed -i 's@deb.debian.org@mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list.d/debian.sources && \
      sed -i 's@security.debian.org@mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list.d/debian.sources ; \
    fi
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libc-dev libffi-dev libmariadb-dev pkg-config
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=builder /app/.venv /app/.venv
COPY app ./app
COPY migrations ./migrations
COPY scripts ./scripts
COPY run.py ./
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 5000
ENV FLASK_ENV=production
ENV FLASK_APP=run.py
ENV MODE=api
ENTRYPOINT ["/entrypoint.sh"]
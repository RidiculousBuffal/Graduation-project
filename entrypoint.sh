#!/bin/bash
set -euo pipefail
# 自动迁移
flask db upgrade
MODE="${MODE:-api}"

if [ "$MODE" = "api" ]; then
    # 启动 Flask API(web/gunicorn)
    exec gunicorn -k gevent -w 4 -b 0.0.0.0:5000 run:app
elif [ "$MODE" = "worker" ]; then
    # 启动 celery worker
    exec celery -A app.celery worker --beat --loglevel=info
else
    echo "MODE 参数必须为 'api'、'worker' 之一！当前值: ${MODE}"
    exit 1
fi
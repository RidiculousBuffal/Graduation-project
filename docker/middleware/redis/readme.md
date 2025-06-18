# Redis
```bash
docker run --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --env=GOSU_VERSION=1.17 --env=REDIS_VERSION=7.4.2 --env=REDIS_DOWNLOAD_URL=http://download.redis.io/releases/redis-7.4.2.tar.gz --env=REDIS_DOWNLOAD_SHA=4ddebbf09061cbb589011786febdb34f29767dd7f89dbe712d2b68e808af6a1f --volume=F:\\redis\\redisdata:/data --volume=F:\\redis\\redis.conf:/etc/redis/redis.conf --volume=/data --network=bridge --privileged --workdir=/data -p 6379:6379 --restart=no --runtime=runc -d redis
```
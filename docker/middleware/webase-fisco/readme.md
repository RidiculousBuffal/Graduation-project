# 说明
一键集成 FISCO BCOS 节点、控制台和 WeBASE-Front,安装官方文档部署 
参考的文档:
[webase](https://webasedoc.readthedocs.io/zh-cn/latest/docs/WeBASE-Install/developer.html)


# 如何使用

```bash
docker run -d \
  -p 30300:30300 -p 30301:30301 -p 30302:30302 -p 30303:30303 \
  -p 20200:20200 -p 20201:20201 -p 20202:20202 -p 20203:20203 \
  -p 8545:8545 -p 8546:8546 -p 8547:8547 -p 8548:8548 \
  -p 5002:5002 \
  --name fisco-all-in-one \
  ridiculousbuffalo/fisco-webase-all-in-one:1.0.0
```

# 查看前端

```bash
loaclhost:5002/WeBASE-Front
```
# 测试镜像是否生效:
部署完成后，可以分步验证：

- FISCO BCOS 节点是否正常运行:
```bash
docker exec -it fisco-all-in-one bash
ps -ef | grep fisco-bcos
netstat -an | grep -E "30300|20200|8545"
```
WeBASE-Front 服务是否启动:

```bash
docker exec -it fisco-all-in-one bash
curl http://127.0.0.1:5002/WeBASE-Front
```

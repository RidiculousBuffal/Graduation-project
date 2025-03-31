# 使用官方 Ubuntu 镜像
FROM ubuntu:latest

# 设置非交互环境变量，避免阻塞
ENV DEBIAN_FRONTEND=noninteractive

# 1. 安装基础依赖和 OpenJDK，同时安装一些必要工具
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl wget openssl default-jdk lsb-release git unzip && \
    rm -rf /var/lib/apt/lists/*

# 2. 安装 chsrc 工具并换源为最快镜像
RUN curl -fsSL https://chsrc.run/posix | bash && \
    /usr/local/bin/chsrc set ubuntu # 自动优化 Ubuntu 源

# 3. 动态设置 JAVA_HOME 环境变量
# 获取 Java 动态路径并更新 `/etc/profile`，同时设置容器环境变量
RUN JAVA_PATH=$(update-alternatives --query java | grep 'Value: ' | awk '{print $2}') && \
    JAVA_HOME=$(dirname $(dirname ${JAVA_PATH})) && \
    echo "export JAVA_HOME=${JAVA_HOME}" >> /etc/profile && \
    echo "export PATH=\$JAVA_HOME/bin:\$PATH" >> /etc/profile && \
    export JAVA_HOME=${JAVA_HOME} && \
    export PATH=$JAVA_HOME/bin:$PATH

# 声明环境变量以便在容器中生效
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# 4. 下载和搭建 FISCO BCOS
WORKDIR /root/fisco
RUN curl -#LO https://github.com/FISCO-BCOS/FISCO-BCOS/releases/download/v2.11.0/build_chain.sh && \
    chmod u+x build_chain.sh && \
    bash build_chain.sh -l 127.0.0.1:4 -p 30300,20200,8545

# 5. 下载和配置 FISCO 控制台
RUN curl -LO https://github.com/FISCO-BCOS/console/releases/download/v2.9.2/download_console.sh && \
    bash download_console.sh && \
    cp -n console/conf/config-example.toml console/conf/config.toml && \
    cp -r nodes/127.0.0.1/sdk/* console/conf/

# 6. 下载和部署 WeBASE-Front
RUN wget https://github.com/WeBankBlockchain/WeBASELargeFiles/releases/download/v1.5.5/webase-front.zip && \
    unzip webase-front.zip && \
    rm webase-front.zip && \
    cp -r nodes/127.0.0.1/sdk/* webase-front/conf/

# 7. 准备自动化启动脚本
COPY ./start_services.sh /root/
RUN chmod +x /root/start_services.sh

# 暴露容器的必要端口
EXPOSE 30300-30303 20200-20203 8545-8548 5002

# 容器启动时进入自动化脚本
CMD ["/root/start_services.sh"]
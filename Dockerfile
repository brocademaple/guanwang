# 使用Python 3.8作为基础镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /work

# 复制项目文件
COPY . /work/

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 升级pip并配置国内镜像源
RUN pip install --upgrade pip && \
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip config set global.trusted-host mirrors.aliyun.com

# 安装Python依赖
RUN pip install -r requirements.txt

# 安装simpleui
RUN pip install django-simpleui -U

# 创建静态文件目录和媒体文件目录
RUN mkdir -p /work/static && mkdir -p /work/media

# 收集静态文件（可选，生产环境推荐）
RUN python manage.py collectstatic --noinput --clear || true

# 暴露端口
EXPOSE 8080

# 设置环境变量（可被docker-compose覆盖）
ENV DB_HOST=db
ENV DB_PORT=3306
ENV DB_NAME=pipedb
ENV DB_USER=root
ENV DB_PASSWORD=root

# 设置启动命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]



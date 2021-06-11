# 基础镜像
FROM python:3.9.5-slim
# 作者
MAINTAINER WANG
# 不缓存输出
ENV PYTHONUNBUFFERED 1
# 关闭字节码输出
ENV PYTHONDONTWRITEBYTECODE 1
# Django密钥
ENV DJANGO_SECRET_KEY "django-insecure-3+3_+!d12=qn38e&#jv-$m&!tia59mk7(7qu_ns%ec!r_8obqe"
# 配置文件环境切换
ENV BLOGSITE_PROFILE "product"
# 修改apt源加快下载库速度，安装系统库
RUN sed -i "s/deb.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y gcc && \
    apt-get install -y default-libmysqlclient-dev
# 更新pip版本
RUN /usr/local/bin/python -m pip install --upgrade pip
# 工作目录
WORKDIR /var/www/html/blogsite
# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.douban.com/simple
# 移除windows回车符
RUN sed -i 's/\r//' start.sh && \
    chmod +x start.sh && \
    sed -i 's/\r//' check_mysql.py
# 入口命令
ENTRYPOINT ./start.sh

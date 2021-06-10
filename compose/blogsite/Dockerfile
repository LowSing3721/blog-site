FROM python:3.9.5-slim
# 环境变量
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SECRET_KEY "django-insecure-3+3_+!d12=qn38e&#jv-$m&!tia59mk7(7qu_ns%ec!r_8obqe"
ENV MYSQL_PASSWORD "root"
ENV REDIS_PASSWORD "redis"
ENV BLOGSITE_PROFILE "product"
# 指定工作空间
WORKDIR /blogsite
# 修改apt源加快下载库速度
RUN sed -i "s/deb.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y gcc && \
    apt-get install -y default-libmysqlclient-dev
# 安装依赖
COPY /requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt -i https://pypi.douban.com/simple
# 启动脚本和检查MySQL脚本, 去windows空白
COPY /compose/blogsite/check_mysql.py /check_mysql.py
COPY /compose/blogsite/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh && \
    chmod +x /start.sh && \
    sed -i 's/\r//' /check_mysql.py

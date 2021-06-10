#!/bin/bash

#sleep 10  # 等待mysql容器完全启动
# 此处可以使用netcat命令替代
function check_mysql(){
    python /check_mysql.py
}
until check_mysql; do
    echo "MySQL is not running yet"
    sleep 1
done

python manage.py makemigrations
python manage.py migrate
gunicorn blogproject.wsgi:application -w 4 -k gthread -b 0.0.0.0:8000 --chdir=/blogsite
#!/bin/bash

# 等待mysql容器完全启动
function check_mysql(){
    python /check_mysql.py
}
until check_mysql; do
    echo "Waiting for the MySQL Server......"
    sleep 3
done
# 启动Django
python manage.py collectstatic --noinput &&
python manage.py makemigrations &&
python manage.py migrate &&
gunicorn blogsite.wsgi:application -w 4 -k gthread -b 0.0.0.0:8000 &&
# 使容器保持开启状态
tail -f /dev/null

exec "$@"
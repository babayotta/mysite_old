#!/bin/bash
trap 'exit' ERR

python manage.py migrate
python manage.py collectstatic --noinput

#python manage.py runserver 0.0.0.0:8000
#uwsgi --http :8000 --wsgi-file mysite/wsgi.py
#uwsgi --ini uwsgi.ini
exec uwsgi \
    --socket=django:9000 \
    --chdir=/src/ \
    --uid=www-data \
    --gid=www-data \
    --wsgi-file=/src/mysite/wsgi.py \
    --module=mysite \
    --auto-procname \
    --processes=3 \
    --master \
    --die-on-term \
    --vacuum


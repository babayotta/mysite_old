#!/bin/bash

python manage.py migrate

#python manage.py runserver 0.0.0.0:8000
uwsgi --ini uwsgi.ini
#uwsgi --http :8000 --wsgi-file mysite/wsgi.py


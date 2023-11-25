#!/bin/sh

python manage.py migrate

celery -A eatpoint beat --loglevel=info
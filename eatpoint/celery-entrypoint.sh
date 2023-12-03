#!/bin/sh

python3 manage.py migrate

celery -A eatpoint flower --port=5555 &
celery -A eatpoint worker --loglevel=info &
celery -A eatpoint beat --loglevel=info

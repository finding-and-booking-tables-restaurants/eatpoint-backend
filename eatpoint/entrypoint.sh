#! /bin/bash

python3 manage.py migrate --no-input
python3 ./manage.py spectacular --color --file schema.yml
python3 manage.py collectstatic --no-input
gunicorn eatpoint.wsgi:application --bind 0.0.0.0:8000
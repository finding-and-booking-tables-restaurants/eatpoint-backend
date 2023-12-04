#!/bin/sh

until cd .
do
    echo "Waiting for server volume..."
done


until python manage.py makemigrations
do
    echo "Waiting for migrations to be ready..."
    sleep 2
done

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

#until python manage.py loaddata data/fixtures2.json
#do
#    echo "Waiting for fixtures to be ready..."
#    sleep 2
#done

until python manage.py collectstatic --no-input
do
    echo "Waiting for static files to be ready..."
    sleep 2
done

python manage.py createsuperuser \
    --noinput \
    --email $DJANGO_SUPERUSER_EMAIL

gunicorn eatpoint.wsgi --bind 0.0.0.0:8000
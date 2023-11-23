#! /bin/sh


until cd /app/eatpoint
do
    echo "Waiting for server volume..."
done


until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

python3 manage.py loaddata data/fixtures.json

python3 manage.py collectstatic --no-input

gunicorn eatpoint.wsgi --bind 0.0.0.0:8000

# for debug
#python manage.py runserver 0.0.0.0:8000
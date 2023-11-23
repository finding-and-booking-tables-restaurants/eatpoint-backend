#!/bin/sh

until cd /app/eatpoint
do
    echo "Waiting for server volume..."
done


celery -A eatpoint worker --loglevel=info

#!/bin/sh

celery -A eatpoint worker --loglevel=info &
celery -A eatpoint beat --loglevel=info

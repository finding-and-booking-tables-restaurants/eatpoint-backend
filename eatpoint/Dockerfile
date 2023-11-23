FROM python:3.11-alpine

RUN apk update && apk add python3-dev gcc libc-dev

RUN pip install --upgrade pip
RUN pip install gunicorn

WORKDIR /app

ADD ./eatpoint /app/eatpoint
RUN pip install -r ./eatpoint/requirements.txt

ADD ../infra/backend-entrypoint.sh /app/infra/
ADD ../infra/flower/flower-entrypoint.sh /app/infra/
ADD ../infra/celery /app/infra/celery/

RUN chmod +x /app/infra/backend-entrypoint.sh

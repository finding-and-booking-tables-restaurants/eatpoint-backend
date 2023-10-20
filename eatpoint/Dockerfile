FROM python:3.11-slim

WORKDIR /app
COPY /eatpoint/requirements.txt /app/
RUN pip install -r requirements.txt
COPY /eatpoint/ /app/
COPY /eatpoint/entrypoint.sh /app/
CMD ["gunicorn", "eatpoint.wsgi:application", "--bind", "0:8000"]

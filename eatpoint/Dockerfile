FROM python:3.11-slim
WORKDIR /app
COPY /eatpoint/requirements.txt /app/
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
COPY /eatpoint/ /app/
COPY /eatpoint/entrypoint.sh /app/
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

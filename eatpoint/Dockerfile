FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

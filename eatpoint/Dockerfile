FROM python:3.11-slim
WORKDIR /app
COPY /eatpoint/requirements.txt /app/
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
COPY /eatpoint/ /app/
COPY /eatpoint/entrypoint.sh /app/
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

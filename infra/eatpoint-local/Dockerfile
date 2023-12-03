FROM python:3.11-slim

WORKDIR /app
COPY ./eatpoint/requirements.txt /app/
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt install -y --no-install-recommends locales; rm -rf /var/lib/apt/lists/*; sed -i '/^#.* ru_RU.UTF-8 /s/^#//' /etc/locale.gen; locale-gen
RUN locale -a
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
ADD ./eatpoint /app/


RUN chmod +x /app/flower-entrypoint.sh
RUN chmod +x /app/worker-entrypoint.sh
RUN chmod +x /app/beat-entrypoint.sh
RUN chmod +x /app/backend-entrypoint.sh

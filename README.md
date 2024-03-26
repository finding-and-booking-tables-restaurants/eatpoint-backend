# eatpoint-backend
![eatpoint_workflow](https://github.com/finding-and-booking-tables-restaurants/eatpoint-backend/actions/workflows/eatpoint_workflows.yml/badge.svg)

## Описание проекта

Проект создан в рамках акселерации Яндекс.Практикум.

Веб-приложения для поиска и бронирования столиков в ресторанах 
в режиме реального времени, чтобы любой человек мог выбрать ресторан или кафе 
на основании отзывов и рейтинга, а также для ресторанов, 
которые могли бы улучшать процесс, вести аналитику и тп.

Проект разворачивается в Docker контейнерах: 
- backend-приложение API, 
- db-база данных, 
- nginx-сервер,
- celery-менеджер периодических задач. 

Реализовано CI и CD проекта. 
При пуше изменений в главную ветку проект автоматически тестируется на соответствие требованиям PEP8.

После успешного прохождения тестов, на git-платформе собирается образ backend-контейнера Docker 
и автоматически размешается в облачном хранилище DockerHub.

Размещенный образ автоматически разворачивается на боевом сервере вместе 
с контейнером веб-сервера nginx и базой данных PostgreSQL.

## Системные требования
- Python 3.11
- Docker
- Works on Linux, Windows, macOS, BSD

## Стек технологий
- Python 3.11
- Django 4.2.5
- Rest API
- PostgreSQL
- Nginx
- gunicorn
- Docker
- DockerHub
- GitHub Actions (CI/CD)
- Celery

## Установка проекта из репозитория
### Клонировать репозиторий и перейти в него в командной строке:

```git clone https://github.com/finding-and-booking-tables-restaurants/eatpoint-backend.git```

### Перейти в директорию инфраструктуры проекта:
``` cd eatpoint/infra ```

### Создать и открыть файл .env с переменными окружения:

```touch .env```
### Заполнить .env файл с переменными окружения по примеру:
```
echo DB_ENGINE=django.db.backends.postgresql >> .env
echo DB_NAME=postgres >> .env
echo POSTGRES_PASSWORD=postgres >> .env
echo POSTGRES_USER=postgres >> .env
echo DB_HOST=db >> .env
echo DB_PORT=5432 >> .env

echo EMAIL_USE_SSL=True >> .env          # или EMAIL_USE_TLS=True
echo EMAIL_HOST='smtp.example.ru' >> .env
echo EMAIL_PORT=port >> .env
echo EMAIL_HOST_USER='your_mail@example.ru' >> .env
echo EMAIL_HOST_PASSWORD='your_password' >> .env
echo DEFAULT_FROM_EMAIL='your_mail@example.ru' >> .env

```

### Установка и запуск приложения в контейнерах (контейнер backend загружается из DockerHub):
```docker-compose up -d```

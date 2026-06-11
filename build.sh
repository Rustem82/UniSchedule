#!/bin/bash

# Сбор статических файлов
python manage.py collectstatic --noinput

# Выполнение миграций
python manage.py migrate --noinput
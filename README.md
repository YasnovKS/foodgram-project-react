# FoodGram

[![CI](https://github.com/YasnovKS/foodgram-project-react/actions/workflows/workflow.yml/badge.svg)](https://github.com/YasnovKS/foodgram-project-react/actions/workflows/workflow.yml)

Foodgram - это сервис, позволяющий людям делиться своими рецептами, сохранять рецепты других людей, подписываться на авторов рецептов и легко формировать список покупок, необходимых для приготовления выбранных блюд.

## Технологии:
- Python
- Django REST Framework
- PostgreSQL
- Docker
- React
- NGINX

## Как это работает?
Склонируйте себе репозиторий проекта, создайте и активируйте виртуальное окружение и установите зависимости с помощью команды "pip install -r requirements.txt".
В разделах репозитория Frontend и Backend находятся файлы создания образов контейнеров (Dockerfile), с помощью которых создаются контейнеры для бекенда и фронтенда.
В разделе Infra находится файл docker-compose, в котором прописана последовательность действий для успешного развертывания контейнеров на сервере.
Для успешного запуска проекта на удаленном сервере скопируйте файлы docker-compose.yml и nginx.conf из папки Infra в домашнюю директорию удаленного сервера.
Основные этапы развертывания проекта указаны в файле workflow.yml. В случае использования github actions, нужно добавить в github secrets необходимые значения переменных, которые используются в workflow.

##### После развертывания контейнеров на удаленном сервере необходимо выполнить миграции и импорт данных в БД.
- зайдите на удаленный сервер через ssh-соединение
- выполните поочередно миграции, используя поочередно команды:
> sudo docker-compose exec backend python manage.py makemigrations users
> sudo docker-compose exec backend python manage.py makemigrations food_app
> sudo docker-compose exec backend python manage.py migrate
- выполните импорт данных с помощью команды:
> sudo docker-compose exec backend python manage.py import_data
- создайте супер юзера командой:
> sudo docker-compose exec backend python manage.py createsuperuser
- выполните сбор статики:
> sudo docker-compose exec backend python manage.py collectstatic --no-input

## Лицензия

#### The MIT License (MIT)

Copyright © «2022» «copyright Yasnov Kirill»

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE

## Авторы
#### Яснов Кирилл
https://github.com/YasnovKS
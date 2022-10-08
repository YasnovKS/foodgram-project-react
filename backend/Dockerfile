FROM python:3.10.7-slim

LABEL author="Yasnov Kirill"

WORKDIR /backend

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY ./requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

WORKDIR /backend/foodgram

ENTRYPOINT [ "../entrypoint.sh" ]

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]
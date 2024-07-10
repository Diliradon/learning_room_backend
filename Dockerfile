FROM python:3.10.4-slim-buster

LABEL maintainer=kravetsbodj@gmail.com

ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN sed -i 's|http://deb.debian.org/debian|http://ftp.us.debian.org/debian|g' /etc/apt/sources.list && \
    apt-get clean && \
    apt-get update --fix-missing && \
    apt-get -y install libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

WORKDIR /app

COPY . .

RUN mkdir -p /vol/web/media

RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user

RUN chown -R django-user:django-user /vol/
RUN chmod -R 755 /vol/web/

USER django-user

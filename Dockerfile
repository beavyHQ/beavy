FROM python:3.5
MAINTAINER ben@create-build-execute.com

RUN apt-get update && apt-get upgrade -y

ENV PYTHONUNBUFFERED 1
ENV BEAVY_ENV PRODUCTION
RUN mkdir -p /app
WORKDIR /app
ADD beavy/ /app/beavy/
ADD beavy_modules /app/beavy_modules/
ADD beavy_apps /app/beavy_apps/
ADD migrations /app/migrations/
ADD var/assets/ /app/assets/
ADD config.yml /app/
ADD .infrastructure/docker/Procfile /app
ADD .infrastructure/docker/run.sh /app/run.sh

ADD *.py /app/

RUN pip install pyyaml
RUN python install.py

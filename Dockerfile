FROM python:3.5
MAINTAINER ben@create-build-execute.com

RUN apt-get update && apt-get upgrade -y

RUN groupadd app && useradd --create-home --home-dir /APP -g app app

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /APP
WORKDIR /APP
ADD beavy/ /APP/beavy/
ADD beavy_modules /APP/beavy_modules/
ADD beavy_apps /APP/beavy_apps/
ADD migrations /APP/migrations/
ADD config.yml /APP/
ADD *.py /APP/

RUN pip install pyyaml
RUN python install.py

USER app

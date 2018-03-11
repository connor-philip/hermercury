# FROM python:2.7-slim
FROM ubuntu:16.04
LABEL maintainer="connor.philip12@hotmail.com"

USER root

WORKDIR /app
ENV PYTHONPATH /app

RUN apt-get update && apt-get -y install \
python \
python-pip

RUN pip install --upgrade pip
RUN pip install feedparser
RUN pip install psutil


CMD ["python", "tests/run_tests.py"]

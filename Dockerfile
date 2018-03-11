FROM python:2.7-stretch
LABEL maintainer="connor.philip12@hotmail.com"

USER root

WORKDIR /app
ENV PYTHONPATH /app

RUN pip install feedparser
RUN pip install psutil


CMD ["python", "tests/run_tests.py"]

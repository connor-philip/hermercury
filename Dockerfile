FROM python:2.7-stretch
LABEL maintainer="connor.philip12@hotmail.com"

USER root
WORKDIR /app
ENV PYTHONPATH /app
ADD . .
RUN pip install -r /app/requirements.txt


CMD ["python", "tests/run_tests.py"]
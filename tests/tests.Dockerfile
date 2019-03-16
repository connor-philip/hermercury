FROM python:3.6-stretch
LABEL maintainer="connor.philip12@hotmail.com"

USER root
WORKDIR /app
ENV PYTHONPATH /app
RUN pip install -r /app/requirements.txt


CMD ["python", "tests/run_tests.py"]

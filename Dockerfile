FROM python:2.7.14-alpine3.6
MAINTAINER Keiran Smith <opensource@keiran.scot>
RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "main.py"]

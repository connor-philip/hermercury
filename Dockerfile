From python:3.8-slim

WORKDIR app
COPY . /app

RUN pip install -r requirements.txt


ENTRYPOINT ["python", "main.py"]
CMD ["start",            \
     "--foreground",     \
     "--frequency=15"    \
]

# Hermercury

A program used to search RSS feeds and send email notifications.

-----


## Setup

### Build
docker built -t hermercury:latest .
docker run -d --name hermecury hermercury:latest

### Dockerhub
docker run -d --name -v ./config.py:/app/config.py affixxx/hermercury:latest

### Python Locally
$ pip install -r requirements.txt
$ python main.py

## Config
There is already a setup notification config along with it's mail template ready to use, however some manual configuration that you need to setup is the emailConfig section of the config.

|Key | Description | Example |
|----|-------------|---------|
| senderAddress | email the notification is sent from | hermercurynotify@gmail.com |
| senderAddressPassword | password of email the notification is sent from | Password123! |
| mailServer | mail server to connect to for the sender email with the port | smtp.gmail.com:587 |
| targetAddress | email to notify to, can be the same address as the senderAddress, or different. Can be an array of emails | myemail@example.com |

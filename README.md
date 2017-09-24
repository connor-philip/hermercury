# Hermercury

A program used to search RSS feeds and send email notifications.

-----


### Setup
Most of the setup required to run will be done by the [setup.sh](https://github.com/connor-philip/hermercury/blob/master/environment/setup.sh) file. You can run this in the [vagrant](https://www.vagrantup.com/intro/getting-started/up.html) environment provided, by using `vagrant up` in the project directory.


### Config
There is already a setup notification config along with it's mail template ready to use, however some manual configuration that you need to setup is the emailConfig section of the config.

|Key | Description | Example |
|----|-------------|---------|
| senderAddress | email the notification is sent from | hermercurynotify@gmail.com |
| senderAddressPassword | password of email the notification is sent from | SuperSecurePassword123! |
| mailServer | mail server to connect to for the sender email with the port | smtp.gmail.com:587 |
| targetAddress | email to notify to, can be the same address as the senderAddress, or different. Can be an array of emails | myemail@example.com |
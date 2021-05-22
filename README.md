# Hermercury
[![Build Status](https://travis-ci.org/connor-philip/lazy_unit_tester.svg?branch=master)](https://travis-ci.org/connor-philip/hermercury)


A Python3 program used to notify via email updates to your watched RSS & Atom feeds.
-----

## Running Hermercury

---

## Locally

### Setup
* Clone the repo
* Inside a terminal at the hermercury directory, enter `pip install -r requirements.txt` to install the python modules
* Rename `config_template.json` to `config.json`, or create a new file file with that name.
* Fill out the config to meet your needs, see the Config section of the readme for details.

### Running
After following the set up and configuration, the intended method to run hermercury is `python main.py start` which will start a process in the background with a default frequency of 15min.

Entering `python main.py --help`  will show a list of the available commands and their description.

---

## Docker
### Setup
* Rename `config_template.json` to `config.json`, or create a new file file with that name.
* Fill out the config to meet your needs, see the Config section of the readme for details.

### Running
You can run the app using docker or docker-compose. The quickest way to start the container to run in the background is: `docker-compose run -d app`

---

#### Config
There is already a set up notification config along with it's mail template ready to use, however the emailConfig section is required to be filled out manually


##### Email Config
|Key                    | Description                                                                                               | Example                       |
|-----------------------|-----------------------------------------------------------------------------------------------------------|-------------------------------|
| senderAddress         | Email the notification is sent from.                                                                      | hermercurynotify@gmail.com    |
| senderAddressPassword | Password of email the notification is sent from.                                                          | Password123                   |
| mailServer            | Mail server to connect to for the sender email with the port.                                             | smtp.gmail.com:587            |
| targetAddress         | Email to notify to, can be the same address as the senderAddress, or different. Can be an array of emails.| myemail@example.com           |

##### Notification Configs
Examples are already present in the [config_template.json](https://github.com/connor-philip/hermercury/blob/master/config_template.json)

|Key            | Description                                                                                                       |
|---------------|-------------------------------------------------------------------------------------------------------------------|
|name           | Arbitrary name of the notification set up.                                                                        |
|feedAddress    | The URL of the RSS/Atom feed.                                                                                     |
|searchString   | A string which matches a sub string of an entries title. RegEx is supported.                                      |
|mailTemplate   | Name of the mailTemplate to send on feed entry match.                                                             |
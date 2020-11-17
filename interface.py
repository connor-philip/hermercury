from hermercury import helper_functions
from hermercury.notify import EmailControl
from hermercury.rss import RSS

import logging
import os


PROJECTDIR = os.path.dirname(os.path.abspath(__file__))
CONFIGPATH = os.path.join(PROJECTDIR, "config.json")
PIDFILE = os.path.join(PROJECTDIR, "hermercury.pid")
NOTIFICATIONHISTORYJSONPATH = os.path.join(PROJECTDIR, "notification_history_json")
logger = logging.getLogger("Hermercury")



def find_and_notify_of_updates():
    configs = helper_functions.read_config(CONFIGPATH)
    notificationConfigs = configs["notificationConfigs"]
    emailConfig = configs["emailConfig"]

    senderAddress = emailConfig["senderAddress"]
    senderAddressPassword = emailConfig["senderAddressPassword"]
    mailServer = emailConfig["mailServer"]
    targetAddress = emailConfig["targetAddress"]

    for notificationConfig in notificationConfigs:
        logger.info(f"")
        feed = RSS(notificationConfig)
        feedUpdates = feed.find_updates(NOTIFICATIONHISTORYJSONPATH)
        mailTemplate = notificationConfig["mailTemplate"]
        fullMailTemplateFilePath = os.path.join(PROJECTDIR, "mail_templates", mailTemplate)

        if feedUpdates:
            logger.info(f"Starting to send mail for matches in {notificationConfig['feedAddress']}")
            logger.info(f"Using mail template: {fullMailTemplateFilePath}")
            for update in feedUpdates:
                subjectName = update["name"]
                searchMatch = update["searchMatch"]

                EmailControlInstance = EmailControl(senderAddress, senderAddressPassword, mailServer, targetAddress)
                email = EmailControlInstance.build_notification_email(subjectName, fullMailTemplateFilePath, searchMatch)

                logger.debug(f"Email: {email}")
                # EmailControlInstance.send_email(email)
        else:
            logger.info(f"No feedUpdates in {notificationConfig['feedAddress']}")
            continue


if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)
    find_and_notify_of_updates()
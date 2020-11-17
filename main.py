from hermercury.process_control import ProcessControl
from hermercury import helper_functions
from hermercury.notify import EmailControl
from hermercury.rss import RSS
import platform
import schedule
import argparse
import logging
import time
import sys
import os

PROJECTDIR = os.path.dirname(os.path.abspath(__file__))
CONFIGPATH = os.path.join(PROJECTDIR, "config.json")
PIDFILE = os.path.join(PROJECTDIR, "hermercury.pid")
NOTIFICATIONHISTORYJSONPATH = os.path.join(PROJECTDIR, "notification_history_json")
logger = logging.getLogger("Hermercury")

parser = argparse.ArgumentParser(prog="command")
subparsers = parser.add_subparsers(help='sub-command help')


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
                EmailControlInstance.send_email(email)
        else:
            logger.info(f"No feedUpdates in {notificationConfig['feedAddress']}")
            continue


def start_scheduler(args):
    frequency = args.frequency

    schedule.every(frequency).minutes.do(find_and_notify_of_updates)
    while True:
        schedule.run_pending()
        time.sleep(1)


def start_background_process(args):
    frequency = str(args.frequency)
    pythonExePath = helper_functions.find_python_executable()
    # pythonExePath = f"python{platform.python_version()}"
    userMessage = ProcessControl(PIDFILE).create_process([pythonExePath, os.path.abspath(__file__), "start", "-f", frequency, "--foreground"])
    sys.stdout.write("{}\n".format(userMessage))


def stop_background_process(args):
    userMessage = ProcessControl(PIDFILE).stop_process()
    sys.stdout.write("{}\n".format(userMessage))


def process_status(args):
    running = ProcessControl(PIDFILE).process_is_running()

    if running:
        sys.stdout.write("Hermercury process is running\n")
    elif running is False:
        sys.stdout.write("No hermercury process running\n")


def return_feed_example(args):
    feedAddress = args.feedAddress
    RSSInstance = RSS(feedAddress)
    firstEntry = RSSInstance.find_entry_by_title(RSSInstance.feedContent, ".+")
    sys.stdout.write("[{:<}]: {:^}\n-----------------------\n".format("Key", "Value"))

    for key in firstEntry:
        value = helper_functions.string_unicode_handler(firstEntry[key])
        sys.stdout.write("[{:<}]: {:^}\n\n".format(key, value))


def test_feeds(args):
    configs = helper_functions.read_config(CONFIGPATH)
    notificationConfigs = configs["notificationConfigs"]

    for notificationConfig in notificationConfigs:
        feed = notificationConfig["feedAddress"]

        print("Trying feed connection for:", feed + "...")
        RSSInstance = RSS(feed)
        if RSSInstance.feedContent:
            print("Connection okay\n")
        else:
            print("NO FEED FOUND\n")


def function_switch(args):
    if args.foreground:
        start_scheduler(args)
    elif args.onceNow:
        logging.basicConfig(level = logging.INFO)
        find_and_notify_of_updates()
    else:
        start_background_process(args)


startParser = subparsers.add_parser("start", help="Starts Hermercury")
startParser.add_argument("-f", "--frequency", type=int, default=15, help="Sets the frequency at which Hermercury should run. In minutes. Default set to 15.")
startParser.add_argument("--foreground", action="store_true", help="Starts Hermercury in the foreground. Does not change the currently running process.")
startParser.add_argument("--onceNow", action="store_true", help="Starts Hermercury in the foreground to run once immediatly.")
startParser.set_defaults(commandFunction=function_switch)

statusParser = subparsers.add_parser("status", help="Returns the status of the program.")
statusParser.set_defaults(commandFunction=process_status)

feedExampleParser = subparsers.add_parser("feedExample", help="Shows the available keys in the given feed.")
feedExampleParser.add_argument("--feedAddress", type=str, help="Feed address")
feedExampleParser.set_defaults(commandFunction=return_feed_example)

feedTestParser = subparsers.add_parser("testFeeds", help="Tests connections to feeds in the config.")
feedTestParser.set_defaults(commandFunction=test_feeds)


stopParser = subparsers.add_parser("stop", help="Stops Hermercury")
stopParser.set_defaults(commandFunction=stop_background_process)

if __name__ == "__main__":
    args = parser.parse_args()
    args.commandFunction(args)

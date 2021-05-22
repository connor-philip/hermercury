from hermercury.process_control import ProcessControl
from hermercury import helper_functions
from hermercury.notify import EmailControl
from hermercury.rss import RSS
from tests.run_tests import testRunner, suite

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


def run_unittests(args):
    testRunner.run(suite)

def function_switch(args):
    logging.basicConfig(format="%(asctime)s - %(message)s",
                        datefmt="%Y.%m.%d %I:%M:%S",
                        level=logging.getLevelName(args.verbosity))
    if args.foreground:
        start_scheduler(args)
    elif args.onceNow:
        find_and_notify_of_updates()
    else:
        start_background_process(args)


startParser = subparsers.add_parser("start", help="Starts Hermercury")
startParser.add_argument("-f", "--frequency", type=int, default=15, help="Sets the frequency at which Hermercury should run. In minutes. Default set to 15.")
startParser.add_argument("-v", "--verbosity", type=str, default="ERROR", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Verbosity of Hermercury.")
startParser.add_argument("--foreground", action="store_true", help="Starts Hermercury in the foreground. Does not change the currently running process.")
startParser.add_argument("--onceNow", action="store_true", help="Starts Hermercury in the foreground to run once immediatly.")
startParser.set_defaults(commandFunction=function_switch)

statusParser = subparsers.add_parser("status", help="Returns the status of the program.")
statusParser.set_defaults(commandFunction=process_status)

stopParser = subparsers.add_parser("stop", help="Stops Hermercury")
stopParser.set_defaults(commandFunction=stop_background_process)

statusParser = subparsers.add_parser("runUnitTests", help="Run hermercury unittests.")
statusParser.set_defaults(commandFunction=run_unittests)

if __name__ == "__main__":
    args = parser.parse_args()
    args.commandFunction(args)

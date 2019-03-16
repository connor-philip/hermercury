from hermercury.process_control import ProcessControl
from hermercury import helper_functions
from hermercury.notify import EmailControl
from hermercury.rss import RSS
import schedule
import argparse
import time
import sys
import os

PROJECTDIR = os.path.dirname(os.path.abspath(__file__))
CONFIGPATH = os.path.join(PROJECTDIR, "config.json")
PIDFILE = os.path.join(PROJECTDIR, "hermercury.pid")

parser = argparse.ArgumentParser(prog="command")
subparsers = parser.add_subparsers(help='sub-command help')


class Notification:

    def __init__(self, notificationConfig, emailConfig):
        self.name = notificationConfig["name"]
        self.feed = notificationConfig["feed"]
        self.search = notificationConfig["search"]
        self.mailTemplate = notificationConfig["mailTemplate"]

        self.senderAddress = emailConfig["senderAddress"]
        self.senderAddressPassword = emailConfig["senderAddressPassword"]
        self.mailServer = emailConfig["mailServer"]
        self.targetAddress = emailConfig["targetAddress"]

        self.fullJsonFilePath = "%s/json/%s.json" % (PROJECTDIR, self.name)
        self.fullMailTemplateFilePath = "%s/mail_templates/%s" % (PROJECTDIR, self.mailTemplate)

    def search_for_notification(self):
        RSSInstance = RSS(self.feed)
        RSSInstance.search_for_notification(self.name, self.search, self.fullJsonFilePath)
        self.entry = RSSInstance.entry
        self.notificationPending = RSSInstance.notificationPending
        if self.entry and self.notificationPending:
            self.notificationObject = RSSInstance.notificationObject

    def send_notification(self):
        EmailControlInstance = EmailControl(self.senderAddress, self.senderAddressPassword, self.mailServer, self.targetAddress)
        email = EmailControlInstance.build_notification_email(self.name, self.fullMailTemplateFilePath, self.notificationObject)
        EmailControlInstance.send_email(email)


def main():
    configs = helper_functions.read_config(CONFIGPATH)
    notificationConfigs = configs["notificationConfigs"]
    emailConfig = configs["emailConfig"]

    for notificationConfig in notificationConfigs:
        Instance = Notification(notificationConfig, emailConfig)
        Instance.search_for_notification()
        if Instance.entry and Instance.notificationPending:
            Instance.send_notification()


def start_scheduler(args):
    frequency = args.frequency

    schedule.every(frequency).minutes.do(main)
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


def return_feed_example(args):
    feedAddress = args.feedAddress
    RSSInstance = RSS(feedAddress)
    firstEntry = RSSInstance.find_entry_by_title(RSSInstance.feedContent, ".+")
    sys.stdout.write("[{:<}]: {:^}\n-----------------------\n".format("Key", "Value"))

    for key in firstEntry:
        value = helper_functions.string_unicode_handler(firstEntry[key])
        sys.stdout.write("[{:<}]: {:^}\n\n".format(key, value))


def function_switch(args):
    if args.foreground:
        start_scheduler(args)
    elif args.onceNow:
        main()
    else:
        start_background_process(args)


startParser = subparsers.add_parser("start", help="Starts Hermercury")
startParser.add_argument("-f", "--frequency", type=int, default=15, help="Sets the frequency at which Hermercury should run. In minutes. Default set to 15")
startParser.add_argument("--foreground", action="store_true", help="Starts Hermercury in the foreground. Does not change the currently running process")
startParser.add_argument("--onceNow", action="store_true", help="Starts Hermercury in the foreground to run once immediatly")
startParser.set_defaults(commandFunction=function_switch)

statusParser = subparsers.add_parser("status", help="Returns the status of the program")
statusParser.set_defaults(commandFunction=process_status)

feedExampleParser = subparsers.add_parser("feedExample", help="Shows the available keys in the given feed")
feedExampleParser.add_argument("--feedAddress", type=str, help="Feed address")
feedExampleParser.set_defaults(commandFunction=return_feed_example)

stopParser = subparsers.add_parser("stop", help="Stops Hermercury")
stopParser.set_defaults(commandFunction=stop_background_process)

if __name__ == "__main__":
    args = parser.parse_args()
    args.commandFunction(args)

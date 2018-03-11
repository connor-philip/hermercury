from config import NotificationConfigs
from process_control import ProcessControl
import schedule
import argparse
import notify
import time
import rss
import os

PROJECTDIR = os.path.dirname(os.path.abspath(__file__))
PIDFILE = os.path.join(PROJECTDIR, "hermercury.pid")
parser = argparse.ArgumentParser(prog="command")
subparsers = parser.add_subparsers(help='sub-command help')


class Notification:

    def __init__(self, NotificationConfig):
            self.Name = NotificationConfig["name"]
            self.Feed = NotificationConfig["feed"]
            self.Search = NotificationConfig["search"]
            self.StoreList = NotificationConfig["storeList"]
            self.MailTemplate = NotificationConfig["mailTemplate"]

            self.FullJsonFilePath = "%s/json/%s.json" % (PROJECTDIR, self.Name)
            self.FullMailTemplateFilePath = "%s/mail_templates/%s" % (PROJECTDIR, self.MailTemplate)

    def search_for_notification(self):
        FeedContent = rss.open_feed(self.Feed)
        self.Entry = rss.search_method_switch(FeedContent, self.Search)
        Object = rss.create_object_with_wanted_parameters(self.Entry, self.StoreList)
        self.NotificationPending = rss.compare_notification_id(self.FullJsonFilePath, self.Name, Object)
        if self.Entry and self.NotificationPending:
            rss.save_object_as_json_to_disk(Object, self.FullJsonFilePath, self.Name)
            self.NotificationObject = rss.load_notification_object(self.FullJsonFilePath)

    def send_notification(self):
        Email = notify.build_notification_email(self.Name, self.FullMailTemplateFilePath, self.NotificationObject)
        notify.send_email(Email)


def main():
    for NotificationConfig in NotificationConfigs:
        Instance = Notification(NotificationConfig)
        Instance.search_for_notification()
        if Instance.Entry and Instance.NotificationPending:
            Instance.send_notification()


def start_scheduler(args):
    frequency = args.frequency

    schedule.every(frequency).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)


def start_background_process(args):
    frequency = str(args.frequency)
    ProcessControl(PIDFILE).create_process(["python", os.path.abspath(__file__), "start", "-f", frequency, "--foreground"])


def stop_background_process(args):
    ProcessControl(PIDFILE).stop_process()


startParser = subparsers.add_parser("start", help="Starts Hermercury")
startParser.add_argument("-f", "--frequency", type=int, default=15, help="Sets the frequency at which Hermercury should run. In minutes. Default set to 15")
startParser.add_argument("--foreground", action="store_true", help="Starts Hermercury in the foreground. Does not change the currently running process")
startParser.set_defaults(commandFunction=start_background_process)

stopParser = subparsers.add_parser("stop", help="Stops Hermercury")
stopParser.set_defaults(commandFunction=stop_background_process, foreground=False)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.foreground:
        start_scheduler(args)
    else:
        args.commandFunction(args)

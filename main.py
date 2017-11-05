from config import NotificationConfigs
import rss
import notify
import os

PROJECTDIR = os.path.dirname(os.path.abspath(__file__))


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


# Main loop
for NotificationConfig in NotificationConfigs:
    Instance = Notification(NotificationConfig)
    Instance.search_for_notification()
    if Instance.Entry and Instance.NotificationPending:
        Instance.send_notification()

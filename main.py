from config import NotificationConfigs
import rss
import notify


class Notification:

    def __init__(self, NotificationConfig):
            self.Name = NotificationConfig["name"]
            self.Feed = NotificationConfig["feed"]
            self.Search = NotificationConfig["search"]
            self.StoreList = NotificationConfig["storeList"]
            self.MailTemplate = NotificationConfig["mailTemplate"]

    def search_for_notification(self):
        FeedContent = rss.open_feed(self.Feed)
        self.Entry = rss.search_method_switch(FeedContent, self.Search)
        Object = rss.create_object_with_wanted_parameters(self.Entry, self.StoreList)
        self.NotificationPending = rss.compare_notification_id(self.Name, Object)
        if self.Entry and self.NotificationPending:
            rss.save_object_as_json_to_disk(Object, self.Name)
            self.NotificationObject = rss.load_notification_object(self.Name)

    def send_notification(self):
        Email = notify.build_notification_email(self.Name, self.MailTemplate, self.NotificationObject)
        notify.send_email(Email)


# Main loop
for NotificationConfig in NotificationConfigs:
    Instance = Notification(NotificationConfig)
    Instance.search_for_notification()
    if Instance.Entry and Instance.NotificationPending:
        Instance.send_notification()

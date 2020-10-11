import logging
import json
import os


logger = logging.getLogger("Hermercury")


class NotificationHistory:

    def __init__(self, searchConfig, notificationHistoryDir):
        self.notificationHistoryDir = notificationHistoryDir
        self._create_json_dir_if_none()
        self.searchName = searchConfig["name"]
        self.notificationHistoryFileName = self._form_file_name(self.searchName)
        self.notificationHistoryFilePath = os.path.abspath(os.path.join(self.notificationHistoryDir,
                                                                        self.notificationHistoryFileName))
        self._create_notification_json_if_none()


    def get_last_matched_id(self) -> str:
        if not os.path.exists(self.notificationHistoryFilePath):
            return ""

        return self._load_notification_json()["lastNotificationId"]


    def update_last_matched_id(self):
        pass

    def add_error_count(self):
        pass

    def reset_error_count(self):
        pass

    def _form_file_name(self, notificationName: str) -> str:
        notificationName = notificationName.replace(" ", "_")
        fileName = f"{notificationName.lower()}.json"

        return fileName

    def _create_json_dir_if_none(self) -> None:
        if not os.path.exists(self.notificationHistoryDir):
            logger.info(f"Creating json path {self.notificationHistoryDir}")
            os.makedirs(self.notificationHistoryDir)

    def _create_notification_json_if_none(self):
        if not os.path.exists(self.notificationHistoryFilePath):
            logger.info(f"Creating json file {self.notificationHistoryFilePath}")
            notificationJson = {
                "name": self.searchName,
                "previousError": False,
                "previousSequentialErrors": 0,
                "lastNotificationId": ""
            }

            self._write_notification_json(notificationJson)

    def _write_notification_json(self, notificationJson: dict) -> None:
        with open(self.notificationHistoryFilePath, "w") as SaveFile:
            json.dump(notificationJson,
                      SaveFile,
                      sort_keys=True,
                      indent=4,
                      separators=(',', ': '))

    def _load_notification_json(self):
        with open(self.notificationHistoryFilePath, "r") as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()

        return jsonObject

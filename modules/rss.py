from hashlib import md5
import hermercury.helper_functions
import feedparser
import json
import os
import re


class RSS:

    def __init__(self, feed):
        self.feed = feed

    def find_entry_by_title(self, searchList, searchString):
        entryMatch = None

        for counter, entry in enumerate(searchList):
            match = re.search(searchString, entry["title"], re.I)
            if match:
                entryMatch = searchList[counter]
                break

        return entryMatch

    def get_feed_content(self, feedAddress: str):
        return feedparser.parse(feedAddress).entries

    def create_match_notification_id(self, feedEntry: dict):
        encodedTitle = feedEntry["title"].encode("utf-8")
        return md5(encodedTitle).hexdigest()

    def save_object_as_json_to_disk(self, dictionaryObject, file, name, hermercuryId, recentError):
        if dictionaryObject:
            dictionaryObject["hermercuryName"] = name
            dictionaryObject["hermercuryId"] = hermercuryId
            dictionaryObject["hermercuryPreviousError"] = recentError
            with open(file, "w") as SaveFile:
                json.dump(dictionaryObject,
                          SaveFile,
                          sort_keys=True,
                          indent=4,
                          separators=(',', ': '))

    def compare_notification_id(self, file, compareId):
        fullFilePath = file
        if os.path.isfile(fullFilePath):
            with open(fullFilePath, "r") as jsonFile:
                jsonObject = json.load(jsonFile)
                jsonFile.close()

            if compareId == jsonObject["hermercuryId"]:
                return False
            else:
                return True
        else:
            return True

    def load_notification_object(self, file):
        if os.path.isfile(file):
            with open(file, "r") as jsonFile:
                jsonObject = json.load(jsonFile)
                jsonFile.close()

        return jsonObject

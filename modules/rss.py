from typing import List
from hashlib import md5
import feedparser
import logging
import json
import os
import re


logging.basicConfig(level = logging.INFO)
logger = logging.getLogger("Hermercury")


class RSS:

    def __init__(self, notificationConfig: dict):
        self.feedAddress = notificationConfig["feedAddress"]
        self.feedSearches = notificationConfig["searches"]

    def find_entry_by_title(self, searchList, searchString):
        entryMatch = None


    def find_matches_by_title(self, feedContent: str, searchString: str) -> List[int]:
        matchIndexes = []

        for counter, entry in enumerate(feedContent):
            match = re.search(searchString, entry["title"], re.I)
            if match:
                logger.info(f"Got match for the search: {searchString}")
                logger.debug(f"match object: {match}")
                entryMatchIndex = matchIndexes.append(counter)

        return matchIndexes if matchIndexes else None

    def get_feed_content(self):
        return feedparser.parse(self.feedAddress).entries

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

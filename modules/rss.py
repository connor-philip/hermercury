from hashlib import md5
import hermercury.helper_functions
import collections
import feedparser
import json
import six
import os
import re


class RSS:

    def __init__(self, feed):
        self.feed = feed
        self.feedContent = feedparser.parse(self.feed).entries

    def find_entry_by_title(self, searchList, searchString):
        entryMatch = None

        for counter, entry in enumerate(searchList):
            match = re.search(searchString, entry["title"], re.I)
            if match:
                entryMatch = searchList[counter]
                break

        return entryMatch

    def find_entry_by_index(self, searchList, index):
        try:
            return searchList[index]
        except IndexError:
            return None

    def create_object_with_wanted_parameters(self, originalObject, keyList):
        storeObject = {}

        if originalObject:
            for key in (key for key in keyList if key in originalObject):
                storeObject[key] = originalObject[key]

        return storeObject

    def create_notification_id(self, dictionaryObject):
        orderedDict = collections.OrderedDict(sorted(dictionaryObject.items()))
        stringToHash = ""

        for key in orderedDict:
            stringToHash += orderedDict[key]

        encodedString =  hermercury.helper_functions.string_unicode_handler(stringToHash, py3Encoding=True)
        return md5(encodedString).hexdigest()

    def save_object_as_json_to_disk(self, dictionaryObject, file, name):
        if dictionaryObject:
            dictionaryObject["name"] = name
            hashDict = collections.OrderedDict(sorted(dictionaryObject.items()))
            dictionaryObject["id"] = self.create_notification_id(hashDict)
            with open(file, "w") as SaveFile:
                json.dump(dictionaryObject, SaveFile, sort_keys=True, indent=4, separators=(',', ': '))

    def compare_notification_id(self, file, name, dictionaryObject):
        fullFilePath = file
        if os.path.isfile(fullFilePath):
            with open(fullFilePath, "r") as jsonFile:
                jsonObject = json.load(jsonFile)
                jsonFile.close()

                dictionaryObject["name"] = name
                hashDict = collections.OrderedDict(sorted(dictionaryObject.items()))
                compareId = self.create_notification_id(hashDict)

                if compareId == jsonObject["id"]:
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

    def search_method_switch(self, feed, searchStringOrIndex):
            if isinstance(searchStringOrIndex, six.string_types):
                entry = self.find_entry_by_title(feed, searchStringOrIndex)
            elif isinstance(searchStringOrIndex, int):
                entry = self.find_entry_by_index(feed, searchStringOrIndex)
            else:
                return None
            return entry

    def search_for_notification(self, name, search, storeList, fullJsonFilePath):
        self.entry = self.search_method_switch(self.feedContent, search)
        dictObject = self.create_object_with_wanted_parameters(self.entry, storeList)
        self.notificationPending = self.compare_notification_id(fullJsonFilePath, name, dictObject)
        if self.entry and self.notificationPending:
            self.save_object_as_json_to_disk(dictObject, fullJsonFilePath, name)
            self.notificationObject = self.load_notification_object(fullJsonFilePath)

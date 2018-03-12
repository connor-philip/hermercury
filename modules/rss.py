from hashlib import md5
import feedparser
import json
import os
import re


def open_feed(feedHost):
    feedData = feedparser.parse(feedHost)
    return feedData.entries


def find_entry_by_title(searchList, searchString):
    entryMatch = None

    for counter, entry in enumerate(searchList):
        match = re.search(searchString, entry["title"], re.I)
        if match:
            entryMatch = searchList[counter]
            break

    return entryMatch


def find_entry_by_index(searchList, index):
    try:
        return searchList[index]
    except IndexError:
        return None


def create_object_with_wanted_parameters(originalObject, keyList):
    storeObject = {}

    if originalObject:
        for key in (key for key in keyList if key in originalObject):
            storeObject[key] = originalObject[key]

    return storeObject


def save_object_as_json_to_disk(dictionaryObject, file, name):
    if dictionaryObject:
        dictionaryObject["name"] = name
        dictionaryObject["id"] = md5(str(dictionaryObject)).hexdigest()
        with open(file, "w") as SaveFile:
            json.dump(dictionaryObject, SaveFile, sort_keys=True, indent=4, separators=(',', ': '))


def compare_notification_id(file, name, dictionaryObject):
    fullFilePath = file
    if os.path.isfile(fullFilePath):
        with open(fullFilePath, "r") as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()

            dictionaryObject["name"] = name
            compareId = md5(str(dictionaryObject)).hexdigest()

            if compareId == jsonObject["id"]:
                return False
            else:
                return True
    else:
        return True


def load_notification_object(file):
    if os.path.isfile(file):
        with open(file, "r") as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()

    return jsonObject


def search_method_switch(feed, searchStringOrIndex):
        if type(searchStringOrIndex) == unicode:
            entry = find_entry_by_title(feed, searchStringOrIndex)
        elif type(searchStringOrIndex) == int:
            entry = find_entry_by_index(feed, searchStringOrIndex)
        else:
            return None
        return entry

from typing import List
from hashlib import md5
import feedparser
import logging
import json
import os
import re


logger = logging.getLogger("Hermercury")


class RSS:

    def __init__(self, notificationConfig: dict):
        self.feedAddress = notificationConfig["feedAddress"]
        self.feedSearches = notificationConfig["searches"]


    def find_updates(self, previouslyMatchedIds: list):
        feedEntries = self.get_feed_content()
        logger.info(f"Starting to search for updates in {self.feedAddress}")

        for searchConfig in self.feedSearches:
            matchIds = set()

            logger.info(f" Searching feed content for {searchConfig['name']}")
            matches = self.find_matches_by_title(feedEntries, searchConfig["searchString"])

            if matches is None:
                logger.info(f"  No matches found for {searchConfig['name']}")
                continue

            for match in matches:
                hermercuryId = self.create_match_notification_id(match)
                matchIds.add(hermercuryId)
                logger.info(f"  Found match with id: {hermercuryId}")

    def find_new_matches_by_title(self, feedEntries: list, searchString: str, lastMatchedId: str) -> List[dict]:
        newMatches = []

        for entry in feedEntries:
            hermercuryId = self.create_match_notification_id(entry)
            match = re.search(searchString, entry["title"], re.I)
            if match and hermercuryId == lastMatchedId:
                logger.info(f"  Found last known match {hermercuryId}")
                break

            elif match:
                logger.info(f"  Found new match {hermercuryId}")
                entry["hermercuryId"] = hermercuryId
                newMatches.append(entry)

        return newMatches if newMatches else None


    def get_feed_content(self) -> list:
        return feedparser.parse(self.feedAddress).entries

    def create_match_notification_id(self, feedEntry: dict):
        encodedTitle = feedEntry["title"].encode("utf-8")
        return md5(encodedTitle).hexdigest()

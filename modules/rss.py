from hermercury.notification_history_json_controller import NotificationHistory

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


    def find_updates(self, notificationHistoryDir):
        feedEntries = self.get_feed_content()
        feedMatches = []
        logger.info(f"Starting to search for updates in {self.feedAddress}")

        for searchConfig in self.feedSearches:
            nh = NotificationHistory(searchConfig, notificationHistoryDir)
            lastMatchedId = nh.get_last_matched_id()

            logger.info(f" Searching feed content for {searchConfig['name']}")
            searchMatches = self.find_new_matches_by_title(feedEntries, searchConfig["searchString"], lastMatchedId)

            if searchMatches is None:
                logger.info(f"  No matches found for {searchConfig['name']}")
                continue

            logger.info(f"   {len(searchMatches)} new matches found")
            logger.debug(f"  New matches: {searchMatches}")

            mostRecentMatch = searchMatches[0]['hermercuryId']
            logger.info(f"  Setting last match id to: {mostRecentMatch}")
            nh.update_last_matched_id(mostRecentMatch)

            searchMatches = [{"name": searchConfig["name"], "searchMatch": searchMatch} for searchMatch in searchMatches]
            feedMatches.extend(searchMatches)


        logger.debug(f"Returning feedMatches: {feedMatches}")
        return feedMatches


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

from hermercury.rss import RSS

import unittest
import shutil
import json
import os
from hypothesis import given
from hypothesis.strategies import text


CURRENTDIR = os.path.dirname(os.path.abspath(__file__))
PROJECTDIR = os.path.abspath(os.path.join(CURRENTDIR, os.pardir))
JSONDIR = os.path.join(PROJECTDIR, "json")


class TestFindNewMatchesByTitle(unittest.TestCase):

    def setUp(self):
        mockNotificationConfig = {"feedAddress": "mockFeedAddress",
                                  "searches": "mockfeedSearch"}
        self.RSSInstance = RSS(mockNotificationConfig)
        self.TestDict1 = {"title": "Title1"}
        self.TestDict2 = {"title": "Title2"}
        self.TestDict3 = {"title": "Title2", "key": "value"}
        self.TestList = [self.TestDict1, self.TestDict2, self.TestDict3]

    def test_returns_list_of_matches(self):
        result = self.RSSInstance.find_new_matches_by_title(self.TestList, "Title1", "")

        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)

    def test_finds_title(self):
        result = self.RSSInstance.find_new_matches_by_title(self.TestList, "Title1", "")

        self.assertEqual(self.TestDict1, result[0])

    def test_ignore_case(self):
        result = self.RSSInstance.find_new_matches_by_title(self.TestList, "tItLe1", "")

        self.assertEqual(self.TestDict1, result[0])

    def test_no_match_return_none(self):
        result = self.RSSInstance.find_new_matches_by_title(self.TestList, "No Such Title Exists", "")

        self.assertIsNone(result)

    def test_try_match_non_string(self):
        with self.assertRaises(TypeError):
            self.RSSInstance.find_new_matches_by_title(self.TestList, 1, "")

    def test_try_iterate_non_iterable(self):
        with self.assertRaises(TypeError):
            self.RSSInstance.find_new_matches_by_title(1, "title", "")

    def test_returns_all_matches(self):
        result = self.RSSInstance.find_new_matches_by_title(self.TestList, "Title2", "")

        self.assertEqual([self.TestDict2, self.TestDict3], result)

    def test_evaluates_search_string_as_regex(self):
        result = self.RSSInstance.find_new_matches_by_title(self.TestList, ".+", "")

        self.assertEqual(self.TestList, result)

    def test_search_stops_when_last_known_id_found(self):
        lastId = self.RSSInstance.create_match_notification_id(self.TestDict2)
        result = self.RSSInstance.find_new_matches_by_title(self.TestList, ".+", lastId)

        self.assertEqual([self.TestDict1], result)

    def test_hermercury_id_added_to_match(self):
        result = self.RSSInstance.find_new_matches_by_title(self.TestList, "Title1", "")
        matchKeys = result[0].keys()
        matchContainsHermercuryId = "hermercuryId" in matchKeys

        self.assertTrue(matchContainsHermercuryId)


class TestCreateMatchNotificationId(unittest.TestCase):

    def setUp(self):
        mockNotificationConfig = {"feedAddress": "mockFeedAddress",
                                  "searches": "mockfeedSearch"}
        self.RSSInstance = RSS(mockNotificationConfig)
        self.TestDict1 = {"title": "Title1"}

    def test_string_is_returned(self):
        returned_value = self.RSSInstance.create_match_notification_id(self.TestDict1)

        self.assertIsInstance(returned_value, str)

    def test_notification_id_is_predictable(self):
        returned_id = self.RSSInstance.create_match_notification_id(self.TestDict1)
        expected_id = "b4c0b4ef700c9a34a3b3ea20bd520322"

        self.assertEqual(expected_id, returned_id)

    @given(text())
    def test_different_inputs_types_do_not_raise_exceptions(self, input):
        TestFeedEntry = {"title": input}
        returned_id = self.RSSInstance.create_match_notification_id(TestFeedEntry)

        self.assertEqual(len(returned_id), 32)


class TestGetFeedContent(unittest.TestCase):

    def setUp(self):
        # FeedAddress will typically be a url, however,
        # we can pass in a string as a mock.
        mockFeed = """<rss version="2.0">
                      <channel>
                      <title>Sample Feed</title>
                      <item><title>one</title></item>
                      <item><title>two</title></item>
                      <item><title>two again</title></item>
                      </channel>
                      </rss>"""

        mockNotificationConfig = {"feedAddress": mockFeed,
                                  "searches": "mockfeedSearch"}
        self.RSSInstance = RSS(mockNotificationConfig)


    def test_list_is_returned(self):
        returnedValue = self.RSSInstance.get_feed_content()

        self.assertIsInstance(returnedValue, list)

    def test_entries_returned_in_list(self):
        returnedValue = self.RSSInstance.get_feed_content()

        self.assertEqual(returnedValue[0]["title"], "one")
        self.assertEqual(returnedValue[1]["title"], "two")


class TestFindUpdates(unittest.TestCase):

    def setUp(self):
        # FeedAddress will typically be a url, however,
        # we can pass in a string as a mock.
        mockFeed = """<rss version="2.0">
                      <channel>
                      <title>Sample Feed</title>
                      <item><title>one</title></item>
                      <item><title>two</title></item>
                      <item><title>two again</title></item>
                      </channel>
                      </rss>"""
        mockfeedSearchOne = {"name": "test_search_one",
                          "searchString": "one"}
        mockfeedSearchTwo = {"name": "test_search_two",
                          "searchString": "two"}
        mockNotificationConfig = {"feedAddress": mockFeed,
                                  "searches": [mockfeedSearchOne, mockfeedSearchTwo]}
        self.RSSInstance = RSS(mockNotificationConfig)

        CURRENTDIR = os.path.dirname(os.path.abspath(__file__))
        self.testJsonDir = os.path.join(CURRENTDIR, "test_json")

    def tearDown(self):
         if os.path.exists(self.testJsonDir):
            shutil.rmtree(self.testJsonDir)

    def test_list_is_returned(self):
        returnedValue = self.RSSInstance.find_updates(self.testJsonDir)

        self.assertIsInstance(returnedValue, list)

    def test_expected_matches_are_returned(self):
        returnedValue = self.RSSInstance.find_updates(self.testJsonDir)
        returnedTitles = [i["searchMatch"]["title"] for i in returnedValue]
        expectedTitles = ["one", "two", "two again"]

        self.assertEqual(returnedTitles, expectedTitles)

    def test_search_name_is_returned_alongside_match(self):
        returnedValue = self.RSSInstance.find_updates(self.testJsonDir)
        returnedNames = [i["name"] for i in returnedValue]
        expectedNames = ["test_search_one", "test_search_two", "test_search_two"]

        self.assertEqual(returnedNames, expectedNames)


    def test_only_new_matches_are_returned(self):
        self.RSSInstance.find_updates(self.testJsonDir)
        returnedValue = self.RSSInstance.find_updates(self.testJsonDir)
        expectedTitles = []

        self.assertEqual(returnedValue, expectedTitles)



if __name__ == "__main__":
    unittest.main()

from hermercury.rss import RSS

import json
import os
import unittest
from hypothesis import given
from hypothesis.strategies import text


CURRENTDIR = os.path.dirname(os.path.abspath(__file__))
PROJECTDIR = os.path.abspath(os.path.join(CURRENTDIR, os.pardir))
JSONDIR = os.path.join(PROJECTDIR, "json")


class TestFindMatchesByTitle(unittest.TestCase):

    def setUp(self):
        mockNotificationConfig = {"feedAddress": "mockFeedAddress",
                                  "searches": "mockfeedSearch"}
        self.RSSInstance = RSS(mockNotificationConfig)
        self.TestDict1 = {"title": "Title1"}
        self.TestDict2 = {"title": "Title2"}
        self.TestDict3 = {"title": "Title2", "key": "value"}
        self.TestList = [self.TestDict1, self.TestDict2, self.TestDict3]

    def test_returns_list_of_matches(self):
        Result = self.RSSInstance.find_matches_by_title(self.TestList, "Title1")

        self.assertIsInstance(Result, list)
        self.assertIsInstance(Result[0], dict)

    def test_finds_title(self):
        Result = self.RSSInstance.find_matches_by_title(self.TestList, "Title1")

        self.assertEqual(self.TestDict1, Result[0])

    def test_ignore_case(self):
        Result = self.RSSInstance.find_matches_by_title(self.TestList, "tItLe1")

        self.assertEqual(self.TestDict1, Result[0])

    def test_no_match_return_none(self):
        Result = self.RSSInstance.find_matches_by_title(self.TestList, "No Such Title Exists")

        self.assertIsNone(Result)

    def test_try_match_non_string(self):
        with self.assertRaises(TypeError):
            self.RSSInstance.find_matches_by_title(self.TestList, 1)

    def test_try_iterate_non_iterable(self):
        with self.assertRaises(TypeError):
            self.RSSInstance.find_matches_by_title(1, "title")

    def test_returns_all_matches(self):
        Result = self.RSSInstance.find_matches_by_title(self.TestList, "Title2")

        self.assertEqual([self.TestDict2, self.TestDict3], Result)

    def test_evaluates_search_string_as_regex(self):
        Result = self.RSSInstance.find_matches_by_title(self.TestList, ".+")

        self.assertEqual(self.TestList, Result)


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



if __name__ == "__main__":
    unittest.main()

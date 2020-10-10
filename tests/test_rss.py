from hermercury.rss import RSS

import json
import os
import unittest
from hypothesis import given
from hypothesis.strategies import text


CURRENTDIR = os.path.dirname(os.path.abspath(__file__))
PROJECTDIR = os.path.abspath(os.path.join(CURRENTDIR, os.pardir))
JSONDIR = os.path.join(PROJECTDIR, "json")


class TestFindEntryByTitle(unittest.TestCase):

    def setUp(self):
        self.RSSInstance = RSS("")
        self.TestDict1 = {"title": "Title1"}
        self.TestDict2 = {"title": "Title2"}
        self.TestDict3 = {"title": "Title2", "key": "value"}
        self.TestList = [self.TestDict1, self.TestDict2, self.TestDict3]

    def test_finds_title(self):
        Result = self.RSSInstance.find_entry_by_title(self.TestList, "Title1")

        self.assertEqual(self.TestDict1, Result)

    def test_ignore_case(self):
        Result = self.RSSInstance.find_entry_by_title(self.TestList, "tItLe1")

        self.assertEqual(self.TestDict1, Result)

    def test_no_match_return_none(self):
        Result = self.RSSInstance.find_entry_by_title(self.TestList, "No Such Title Exists")

        self.assertIsNone(Result)

    def test_try_match_non_string(self):
        with self.assertRaises(TypeError):
            self.RSSInstance.find_entry_by_title(self.TestList, 1)

    def test_try_iterate_non_iterable(self):
        with self.assertRaises(TypeError):
            self.RSSInstance.find_entry_by_title(1, "title")

    def test_return_first_found(self):
        Result = self.RSSInstance.find_entry_by_title(self.TestList, "Title2")

        self.assertEqual(self.TestDict2, Result)
        self.assertNotEqual(self.TestDict3, Result)


class TestSaveObjectAsJsonToDisk(unittest.TestCase):

    def setUp(self):
        self.RSSInstance = RSS("")
        self.jsonDir = JSONDIR
        self.EmptyObject = {}
        self.TestCaseFileName = "test_case_file_name"
        self.Object = {"summary": "summary!",
                       "link": "http://test/case/link/",
                       "title": self.TestCaseFileName}
        self.hermercuryId = self.RSSInstance.create_notification_id(self.Object)
        self.CompareObject = {"title": self.TestCaseFileName,
                              "link": "http://test/case/link/",
                              "hermercuryName": self.TestCaseFileName,
                              "hermercuryId": "bb5cea22fe8cb6ac87227f27be3a611d",
                              "hermercuryPreviousError": False,
                              "summary": "summary!"}
        self.FullFilePath = self.jsonDir + self.TestCaseFileName + ".json"

    def tearDown(self):
        if os.path.isfile(self.FullFilePath):
            os.remove(self.FullFilePath)

    def test_object_is_saved(self):
        self.RSSInstance.save_object_as_json_to_disk(self.Object,
                                                     self.FullFilePath,
                                                     self.TestCaseFileName,
                                                     self.hermercuryId,
                                                     False)

        with open(self.FullFilePath, "r+") as TestCaseFile:
            TestCaseFileObject = json.load(TestCaseFile)
            TestCaseFile.close()

        self.assertEqual(self.CompareObject, TestCaseFileObject)

    def test_empty_object_is_not_saved(self):
        self.RSSInstance.save_object_as_json_to_disk(self.EmptyObject,
                                                     self.FullFilePath,
                                                     self.TestCaseFileName,
                                                     self.hermercuryId,
                                                     False)

        Result = os.path.isfile(self.FullFilePath)

        self.assertEqual(False, Result)


class TestCompareNotificationID(unittest.TestCase):

    def setUp(self):
        self.RSSInstance = RSS("")
        self.jsonDir = JSONDIR
        self.TestCaseFileName = "test_case_file_name"
        self.FullFilePath = self.jsonDir + self.TestCaseFileName + ".json"
        self.Object = {"summary": "summary!",
                       "link": "http://test/case/link/",
                       "title": self.TestCaseFileName}
        self.hermercuryId = self.RSSInstance.create_notification_id(self.Object)
        self.RSSInstance.save_object_as_json_to_disk(self.Object,
                                                     self.FullFilePath,
                                                     self.TestCaseFileName,
                                                     self.hermercuryId,
                                                     False)

    def tearDown(self):
        if os.path.isfile(self.FullFilePath):
            os.remove(self.FullFilePath)

    def test_returns_false_when_id_matches(self):
        Result = self.RSSInstance.compare_notification_id(self.FullFilePath,
                                                          self.hermercuryId)

        self.assertEqual(Result, False)

    def test_returns_true_when_id_does_not_match(self):
        self.hermercuryId = "changed"
        Result = self.RSSInstance.compare_notification_id(self.FullFilePath,
                                                          self.hermercuryId)

        self.assertEqual(Result, True)

    def test_returns_true_when_file_does_not_exist(self):
        if os.path.isfile(self.FullFilePath):
            os.remove(self.FullFilePath)

        Result = self.RSSInstance.compare_notification_id(self.FullFilePath,
                                                          self.hermercuryId)

        self.assertEqual(Result, True)


class TestCreateNotificationId(unittest.TestCase):

    def setUp(self):
        self.RSSInstance = RSS("")
        self.TestDict1 = {"title": "Title1"}

    def test_string_is_returned(self):
        returned_value = self.RSSInstance.create_notification_id(self.TestDict1)

        self.assertIsInstance(returned_value, str)

    def test_notification_id_is_predictable(self):
        returned_id = self.RSSInstance.create_notification_id(self.TestDict1)
        expected_id = "b4c0b4ef700c9a34a3b3ea20bd520322"

        self.assertEqual(expected_id, returned_id)

    @given(text())
    def test_different_inputs_types_do_not_raise_exceptions(self, input):
        TestFeedEntry = {"title": input}
        returned_id = self.RSSInstance.create_notification_id(TestFeedEntry)

        self.assertEqual(len(returned_id), 32)



if __name__ == "__main__":
    unittest.main()

from hermercury.rss import RSS
import json
import os
import unittest
import sys


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

        self.assertEqual(None, Result)

    def test_try_match_non_string(self):
        try:
            Result = self.RSSInstance.find_entry_by_title(self.TestList, 1)
        except TypeError:
            Result = TypeError

        self.assertEqual(TypeError, Result)

    def test_try_iterate_non_iterable(self):
        try:
            Result = self.RSSInstance.find_entry_by_title("list", "title")
        except TypeError:
            Result = TypeError

        self.assertEqual(TypeError, Result)

    def test_return_first_found(self):
        Result = self.RSSInstance.find_entry_by_title(self.TestList, "Title2")

        self.assertEqual(self.TestDict2, Result)
        self.assertNotEqual(self.TestDict3, Result)


class TestFindEntryByIndex(unittest.TestCase):

    def setUp(self):
        self.RSSInstance = RSS("")
        self.TestDict1 = {"title": "Title1"}
        self.TestDict2 = {"title": "Title2"}
        self.TestDict3 = {"title": "Title3", "key": "value"}
        self.TestList = [self.TestDict1, self.TestDict2, self.TestDict3]

    def test_returns_correct_index(self):
        Result1 = self.RSSInstance.find_entry_by_index(self.TestList, 0)
        Result2 = self.RSSInstance.find_entry_by_index(self.TestList, 1)
        Result3 = self.RSSInstance.find_entry_by_index(self.TestList, 2)

        self.assertEqual(self.TestDict1, Result1)
        self.assertEqual(self.TestDict2, Result2)
        self.assertEqual(self.TestDict3, Result3)

    def test_out_of_index(self):
        Result = self.RSSInstance.find_entry_by_index(self.TestList, 100)

        self.assertEqual(None, Result)

    def test_try_find_with_non_int(self):
        try:
            Result = self.RSSInstance.find_entry_by_index(self.TestList, "1")
        except TypeError:
            Result = TypeError

        self.assertEqual(TypeError, Result)


class TestCreateObjectWithWantedParameters(unittest.TestCase):

    def setUp(self):
        self.RSSInstance = RSS("")
        self.TestDict = {"title": "Title1", "parameter2": 2, "parameter3": "three", "parameter4": [1, 2, 3, 4]}

    def test_keys_are_saved(self):
        Result = self.RSSInstance.create_object_with_wanted_parameters(self.TestDict, ["title", "parameter2", "parameter4"])
        ExpectedResult = {"title": "Title1", "parameter2": 2, "parameter4": [1, 2, 3, 4]}

        self.assertEqual(ExpectedResult, Result)

    def test_key_missing_from_original_object_throws_no_error(self):
        Result = self.RSSInstance.create_object_with_wanted_parameters(self.TestDict, ["title", "does_not_exist"])
        ExpectedResult = {"title": "Title1"}

        self.assertEqual(ExpectedResult, Result)

    def test_returns_empty_dictionary_when_nothing_found(self):
        Result = self.RSSInstance.create_object_with_wanted_parameters(self.TestDict, ["does_not_exist"])
        ExpectedResult = {}

        self.assertEqual(ExpectedResult, Result)

    def test_if_original_object_nonetype_return_empty_dic(self):
        Result = self.RSSInstance.create_object_with_wanted_parameters(None, ["title"])
        ExpectedResult = {}

        self.assertEqual(ExpectedResult, Result)


class TestSaveObjectAsJsonToDisk(unittest.TestCase):

    def setUp(self):
        self.RSSInstance = RSS("")
        self.jsonDir = JSONDIR
        self.EmptyObject = {}
        self.TestCaseFileName = "test_case_file_name"
        self.Object = {"summary": "summary!", "link": "http://test/case/link/", "title": self.TestCaseFileName}
        self.CompareObject = {"title": self.TestCaseFileName, "link": "http://test/case/link/", "name": self.TestCaseFileName, "id": "2dd66ccfe382b544ab4e27acacb43afb", "summary": "summary!"}
        self.FullFilePath = self.jsonDir + self.TestCaseFileName + ".json"

    def tearDown(self):
        if os.path.isfile(self.FullFilePath):
            os.remove(self.FullFilePath)

    def test_object_is_saved(self):
        self.RSSInstance.save_object_as_json_to_disk(self.Object, self.FullFilePath, self.TestCaseFileName)

        with open(self.FullFilePath, "r+") as TestCaseFile:
            TestCaseFileObject = json.load(TestCaseFile)
            TestCaseFile.close()

        self.assertEqual(self.CompareObject, TestCaseFileObject)

    def test_empty_object_is_not_saved(self):
        self.RSSInstance.save_object_as_json_to_disk(self.EmptyObject, self.FullFilePath, self.TestCaseFileName)

        Result = os.path.isfile(self.FullFilePath)

        self.assertEqual(False, Result)


class TestCompareNotificationID(unittest.TestCase):

    def setUp(self):
        self.RSSInstance = RSS("")
        self.jsonDir = JSONDIR
        self.TestCaseFileName = "test_case_file_name"
        self.FullFilePath = self.jsonDir + self.TestCaseFileName + ".json"
        self.Object = {"summary": "summary!", "link": "http://test/case/link/", "title": self.TestCaseFileName}
        self.CompareObject = {"summary": "summary!", "link": "http://test/case/link/", "title": self.TestCaseFileName}
        self.RSSInstance.save_object_as_json_to_disk(self.Object, self.FullFilePath, self.TestCaseFileName)

    def tearDown(self):
        if os.path.isfile(self.FullFilePath):
            os.remove(self.FullFilePath)

    def test_returns_false_when_id_matches(self):
        Result = self.RSSInstance.compare_notification_id(self.FullFilePath, self.TestCaseFileName, self.CompareObject)

        self.assertEqual(Result, False)

    def test_returns_true_when_id_does_not_match(self):
        self.CompareObject["random_param_to_change_id"] = "anything"
        Result = self.RSSInstance.compare_notification_id(self.FullFilePath, self.TestCaseFileName, self.CompareObject)

        self.assertEqual(Result, True)

    def test_returns_true_when_file_does_not_exist(self):
        if os.path.isfile(self.FullFilePath):
            os.remove(self.FullFilePath)

        Result = self.RSSInstance.compare_notification_id(self.FullFilePath, self.TestCaseFileName, self.CompareObject)

        self.assertEqual(Result, True)


if __name__ == "__main__":
    unittest.main()

import hermercury.notification_history_json_controller as nhjc

import unittest
import shutil
import os



class TestNotificationHistoryInit(unittest.TestCase):

    def setUp(self):
        CURRENTDIR = os.path.dirname(os.path.abspath(__file__))
        self.testJsonDir = os.path.join(CURRENTDIR, "test_json")
        self.searchConfig = {"name": "test name", "searchString": "test search"}
        self.nh = nhjc.NotificationHistory(self.searchConfig, self.testJsonDir)

    def tearDown(self):
         if os.path.exists(self.testJsonDir):
            shutil.rmtree(self.testJsonDir)


    def test_json_dir_created_if_none(self):
        self.assertTrue(os.path.exists(self.testJsonDir))


    def test_notification_json_created_if_none(self):
        jsonPath = os.path.join(self.testJsonDir, "test_name.json")
        jsonFileExists = os.path.exists(jsonPath)
        self.assertTrue(jsonFileExists)


    def test_notification_json_not_overwritten_if_exists(self):
        jsonPath = os.path.join(self.testJsonDir, "test_name.json")
        testJson = {"test": "test"}
        self.nh._write_notification_json(testJson)

        testInstance = nhjc.NotificationHistory(self.searchConfig, self.testJsonDir)
        loadedJson = testInstance._load_notification_json()

        self.assertEqual(loadedJson, testJson)



class TestFormFileName(unittest.TestCase):

    def setUp(self):
        CURRENTDIR = os.path.dirname(os.path.abspath(__file__))
        self.testJsonDir = os.path.join(CURRENTDIR, "test_json")
        searchConfig = {"name": "test name", "searchString": "test search"}
        self.nh = nhjc.NotificationHistory(searchConfig, self.testJsonDir)

    def tearDown(self):
         if os.path.exists(self.testJsonDir):
            shutil.rmtree(self.testJsonDir)

    def test_string_is_returned(self):
        returnedName = self.nh._form_file_name("a name with spaces")

        self.assertIsInstance(returnedName, str)

    def test_spaces_replaced_with_underscores(self):
        returnedName = self.nh._form_file_name("a name with spaces")
        expectedNameSubString = "a_name_with_spaces"

        self.assertTrue(expectedNameSubString in returnedName)

    def test_file_extension_appended(self):
        returnedName = self.nh._form_file_name("a name with spaces")
        expectedName = "a_name_with_spaces.json"

        self.assertEqual(returnedName, expectedName)


    def test_name_made_to_lowercase(self):
        returnedName = self.nh._form_file_name("A NAME WITH SPACES")
        expectedNameSubString = "a_name_with_spaces"

        self.assertTrue(expectedNameSubString in returnedName)


class TestGetLastMatchedId(unittest.TestCase):

    def setUp(self):
        CURRENTDIR = os.path.dirname(os.path.abspath(__file__))
        self.testJsonDir = os.path.join(CURRENTDIR, "test_json")
        searchConfig = {"name": "test name", "searchString": "test search"}
        self.nh = nhjc.NotificationHistory(searchConfig, self.testJsonDir)

    def tearDown(self):
         if os.path.exists(self.testJsonDir):
            shutil.rmtree(self.testJsonDir)

    def test_string_is_returned(self):
        returnedId = self.nh.get_last_matched_id()

        self.assertIsInstance(returnedId, str)

    def test_empty_string_is_returned_when_notification_history_file_doesnt_exist(self):
        self.tearDown()
        returnedId = self.nh.get_last_matched_id()

        self.assertEqual(returnedId, "")

    def test_id_is_returned_when_file_exists(self):
        notification = {
                "lastNotificationId": "test_id"
        }
        self.nh._write_notification_json(notification)
        returnedId = self.nh.get_last_matched_id()

        self.assertEqual(returnedId, "test_id")


if __name__ == "__main__":
    unittest.main()

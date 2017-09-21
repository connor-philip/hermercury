import os
import unittest
from config import emailConfig
import notify


class TestBuildNotificationEmail(unittest.TestCase):

    def setUp(self):
        self.SENDERADDRESS = emailConfig["senderAddress"]
        self.TARGETADDRESS = emailConfig["targetAddress"]
        self.testMessageTemplateFile = "unit_test_notification_template.txt"
        self.variableStore = {"variable": "this value replaces the variable"}
        self.MAILTEMPLATEDIR = notify.MAILTEMPLATEDIR

        with open(self.MAILTEMPLATEDIR + self.testMessageTemplateFile, "w") as testMessageTemplateFile:
            testMessageTemplateFile.write("test string\n")
            testMessageTemplateFile.write("{{variable}}")
            testMessageTemplateFile.close()

    def tearDown(self):
        os.remove(self.MAILTEMPLATEDIR + self.testMessageTemplateFile)

    def test_function_returns_built_email(self):
        emailResult = notify.build_notification_email("subject", self.testMessageTemplateFile, {})
        expectedEmail = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (self.SENDERADDRESS, self.TARGETADDRESS, "subject", "test string\n{{variable}}")

        self.assertEqual(expectedEmail, emailResult)

    def test_function_returns_string(self):
        emailResult = notify.build_notification_email("subject", self.testMessageTemplateFile, {})

        self.assertIsInstance(emailResult, str)

    def test_variables_in_double_curly_bracks_are_replaced(self):
        emailResult = notify.build_notification_email("subject", self.testMessageTemplateFile, self.variableStore)
        expectedEmail = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (self.SENDERADDRESS, self.TARGETADDRESS, "subject", "test string\nthis value replaces the variable")

        self.assertEqual(expectedEmail, emailResult)

    def test_continue_if_no_variables_found(self):
        with open(self.MAILTEMPLATEDIR + self.testMessageTemplateFile, "w") as testMessageTemplateFile:
            testMessageTemplateFile.write("test string")
            testMessageTemplateFile.close()

        emailResult = notify.build_notification_email("subject", self.testMessageTemplateFile, self.variableStore)
        expectedEmail = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (self.SENDERADDRESS, self.TARGETADDRESS, "subject", "test string")

        self.assertEqual(expectedEmail, emailResult)

    def test_continue_if_variable_store_contains_no_replacement(self):
        self.variableStore = {}

        emailResult = notify.build_notification_email("subject", self.testMessageTemplateFile, self.variableStore)
        expectedEmail = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (self.SENDERADDRESS, self.TARGETADDRESS, "subject", "test string\n{{variable}}")

        self.assertEqual(expectedEmail, emailResult)


if __name__ == "__main__":
    unittest.main()

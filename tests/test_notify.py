from modules.helper_functions import read_config
from modules import notify
import unittest
import os


CURRENTDIR = os.path.dirname(os.path.abspath(__file__))
PROJECTDIR = os.path.abspath(os.path.join(CURRENTDIR, os.pardir))
MAILTEMPLATEDIR = os.path.join(PROJECTDIR, "mail_templates")
emailConfig = read_config()["emailConfig"]


class TestBuildNotificationEmail(unittest.TestCase):

    def setUp(self):
        self.senderAddress = emailConfig["senderAddress"]
        self.targetAddress = emailConfig["targetAddress"]
        self.variableStore = {"variable": "this value replaces the variable"}
        self.mailTemplateFilePath = os.path.join(MAILTEMPLATEDIR, "unit_test_notification_template.txt")

        with open(self.mailTemplateFilePath, "w") as testMessageTemplateFile:
            testMessageTemplateFile.write("test string\n")
            testMessageTemplateFile.write("{{variable}}")
            testMessageTemplateFile.close()

    def tearDown(self):
        os.remove(self.mailTemplateFilePath)

    def test_function_returns_built_email(self):
        emailResult = notify.build_notification_email("subject", self.mailTemplateFilePath, {})
        expectedEmail = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (self.senderAddress, self.targetAddress, "subject", "test string\n{{variable}}")

        self.assertEqual(expectedEmail, emailResult)

    def test_function_returns_str(self):
        emailResult = notify.build_notification_email("subject", self.mailTemplateFilePath, {})

        self.assertIsInstance(emailResult, str)

    def test_variables_in_double_curly_bracks_are_replaced(self):
        emailResult = notify.build_notification_email("subject", self.mailTemplateFilePath, self.variableStore)
        expectedEmail = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (self.senderAddress, self.targetAddress, "subject", "test string\nthis value replaces the variable")

        self.assertEqual(expectedEmail, emailResult)

    def test_continue_if_no_variables_found(self):
        with open(self.mailTemplateFilePath, "w") as testMessageTemplateFile:
            testMessageTemplateFile.write("test string")
            testMessageTemplateFile.close()

        emailResult = notify.build_notification_email("subject", self.mailTemplateFilePath, self.variableStore)
        expectedEmail = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (self.senderAddress, self.targetAddress, "subject", "test string")

        self.assertEqual(expectedEmail, emailResult)

    def test_continue_if_variable_store_contains_no_replacement(self):
        self.variableStore = {}

        emailResult = notify.build_notification_email("subject", self.mailTemplateFilePath, self.variableStore)
        expectedEmail = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (self.senderAddress, self.targetAddress, "subject", "test string\n{{variable}}")

        self.assertEqual(expectedEmail, emailResult)


if __name__ == "__main__":
    unittest.main()

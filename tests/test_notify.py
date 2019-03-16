from hermercury.notify import EmailControl
import unittest
import os


CURRENTDIR = os.path.dirname(os.path.abspath(__file__))
PROJECTDIR = os.path.abspath(os.path.join(CURRENTDIR, os.pardir))
MAILTEMPLATEDIR = os.path.join(PROJECTDIR, "mail_templates")


class TestBuildNotificationEmail(unittest.TestCase):

    def setUp(self):
        self.senderAddress = "sender@address.com"
        self.senderAddressPassword = "password"
        self.targetAddress = "target@address.com"
        self.mailServer = "mailServer"
        self.variableStore = {"variable": "this value replaces the variable"}
        self.mailTemplateFilePath = os.path.join(MAILTEMPLATEDIR, "unit_test_notification_template.txt")

        self.EmailControlInstance = EmailControl(self.senderAddress, self.senderAddressPassword, self.mailServer, self.targetAddress)

        with open(self.mailTemplateFilePath, "w") as testMessageTemplateFile:
            testMessageTemplateFile.write("test string\n")
            testMessageTemplateFile.write("{{variable}}")
            testMessageTemplateFile.close()

    def tearDown(self):
        os.remove(self.mailTemplateFilePath)

    def test_function_returns_built_email(self):
        emailResult = self.EmailControlInstance.build_notification_email("subject", self.mailTemplateFilePath, {})
        expectedEmail = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (self.senderAddress, self.targetAddress, "subject", "test string\n{{variable}}")

        self.assertEqual(expectedEmail, emailResult)

    def test_function_returns_str(self):
        emailResult = self.EmailControlInstance.build_notification_email("subject", self.mailTemplateFilePath, {})

        self.assertIsInstance(emailResult, str)

    def test_variables_in_double_curly_bracks_are_replaced(self):
        emailResult = self.EmailControlInstance.build_notification_email("subject", self.mailTemplateFilePath, self.variableStore)
        expectedEmail = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (self.senderAddress, self.targetAddress, "subject", "test string\nthis value replaces the variable")

        self.assertEqual(expectedEmail, emailResult)

    def test_continue_if_no_variables_found(self):
        with open(self.mailTemplateFilePath, "w") as testMessageTemplateFile:
            testMessageTemplateFile.write("test string")
            testMessageTemplateFile.close()

        emailResult = self.EmailControlInstance.build_notification_email("subject", self.mailTemplateFilePath, self.variableStore)
        expectedEmail = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (self.senderAddress, self.targetAddress, "subject", "test string")

        self.assertEqual(expectedEmail, emailResult)

    def test_continue_if_variable_store_contains_no_replacement(self):
        self.variableStore = {}

        emailResult = self.EmailControlInstance.build_notification_email("subject", self.mailTemplateFilePath, self.variableStore)
        expectedEmail = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (self.senderAddress, self.targetAddress, "subject", "test string\n{{variable}}")

        self.assertEqual(expectedEmail, emailResult)


if __name__ == "__main__":
    unittest.main()

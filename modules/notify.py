import smtplib
import re


class EmailControl:

    def __init__(self, senderAddress, senderAddressPassword, mailServer, targetAddress):
        self.senderAddress = senderAddress
        self.senderAddressPassword = senderAddressPassword
        self.mailServer = mailServer
        self.targetAddress = targetAddress

    def build_notification_email(self, subject, mailTemplate, variableStore):
        with open(mailTemplate, "r") as mailBodyTemplateFile:
            mailBody = str(mailBodyTemplateFile.read())
            mailBodyTemplateFile.close()

        matchList = re.findall("{{\w+}}", mailBody)
        for match in (match for match in matchList if matchList):
            key = match.strip("{}")
            if key in variableStore:
                mailBody = re.sub(match, variableStore[key], mailBody)

        email = "From: {}\nTo: {}\nSubject: {}\n\n{}".format(self.senderAddress, self.targetAddress, subject, mailBody)

        return email

    def send_email(self, email):
        server = smtplib.SMTP(self.mailServer)
        server.ehlo()
        server.starttls()
        server.login(self.senderAddress, self.senderAddressPassword)
        server.sendmail(self.senderAddress, self.targetAddress, email)
        server.quit()

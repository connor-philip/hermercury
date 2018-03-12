from config import emailConfig
import smtplib
import re

SENDERADDRESS = emailConfig["senderAddress"]
SENDERADDRESSPASSWORD = emailConfig["senderAddressPassword"]
MAILSERVER = emailConfig["mailServer"]
TARGETADDRESS = emailConfig["targetAddress"]

dictionary = {"title": "this is the title", "link": "this is the link"}


def build_notification_email(subject, mailTemplate, variableStore):
    with open(mailTemplate, "r") as mailBodyTemplateFile:
        mailBody = str(mailBodyTemplateFile.read())
        mailBodyTemplateFile.close()

    matchList = re.findall("{{\w+}}", mailBody)
    for match in (match for match in matchList if matchList):
        key = match.strip("{}")
        if key in variableStore:
            mailBody = re.sub(match, variableStore[key], mailBody)

    email = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (SENDERADDRESS, TARGETADDRESS, subject, mailBody)

    return email


def send_email(email):
    server = smtplib.SMTP(MAILSERVER)
    server.ehlo()
    server.starttls()
    server.login(SENDERADDRESS, SENDERADDRESSPASSWORD)
    server.sendmail(SENDERADDRESS, TARGETADDRESS, email)
    server.quit()

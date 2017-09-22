emailConfig = {
    "senderAddress": "email to send from",
    "senderAddressPassword": "password of email to send from",
    "mailServer": "mail server to connect to for the sender email",
    "targetAddress": "email to notify to"
}
NotificationConfigs = [
    {
        "name": "hermercury github",
        "feed": "https://github.com/connor-philip/hermercury/commits/master.atom",
        "search": 0,
        "storeList": ["author", "link"],
        "mailTemplate": "hermercury_example.txt"
    }
]

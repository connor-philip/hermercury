import json
import sys
import os

CURRENTDIR = os.path.dirname(os.path.abspath(__file__))
PROJECTDIR = os.path.abspath(os.path.join(CURRENTDIR, os.pardir))
CONFIGPATH = os.path.join(PROJECTDIR, "config.json")


def read_config():
    with open(CONFIGPATH, "r") as jsonFile:
        configData = json.load(jsonFile)
        jsonFile.close()

    return configData


def string_unicode_handler(inputString, py3Encoding=False):
    PY2 = sys.version_info[0] == 2
    PY3 = sys.version_info[0] == 3

    if PY3 and py3Encoding:
        return str(inputString).encode("utf-8")
    elif PY3:
        return str(inputString)
    elif PY2:
        return unicode(inputString).encode("utf-8")

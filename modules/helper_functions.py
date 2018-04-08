from hashlib import md5
import collections
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


hashDict = {u"summary": u"summary!", u"link": u"http://test/case/link/", u"title": u"test_case_file_name"}
hashDict = collections.OrderedDict(sorted(hashDict.items()))
res = string_unicode_handler(hashDict, py3Encoding=True)
resHash = md5(res).hexdigest()
sys.stdout.write(string_unicode_handler(res))
sys.stdout.write(resHash)
# get this to give the same id using python 2 & 3, or change unit tests to calculate id based on python version.

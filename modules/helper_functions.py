import json
import os

CURRENTDIR = os.path.dirname(os.path.abspath(__file__))
PROJECTDIR = os.path.abspath(os.path.join(CURRENTDIR, os.pardir))
CONFIGPATH = os.path.join(PROJECTDIR, "config.json")


def read_config():
    with open(CONFIGPATH, "r") as jsonFile:
        configData = json.load(jsonFile)
        jsonFile.close()

    return configData

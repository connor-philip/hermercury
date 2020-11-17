import json
import sys
import os


def read_config(configPath):
    with open(configPath, "r") as jsonFile:
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


def find_python_executable():
    PY3 = sys.version_info[0] == 3
    pyVersion = f"python{sys.version_info[0]}.{sys.version_info[1]}"
    linux = "linux" in sys.platform
    pythonDir = os.path.dirname(sys.executable)

    if PY3 and linux:
        pyPath = os.path.join(pythonDir, pyVersion)
    else:
        pyPath = os.path.join(pythonDir, "python")

    return pyPath

from hashlib import md5
import subprocess
import psutil
import json
import os


class ProcessControl:

    def __init__(self, pidFile):
        self.pidFile = pidFile

    def __write_pid_file__(self, pidData):
        with open(self.pidFile, "w") as fileObj:
            json.dump(pidData, fileObj, sort_keys=True, indent=4, separators=(',', ': '))
            fileObj.close()

    def __read_pid_file__(self):
        pidData = {}
        if os.path.exists(self.pidFile):
            with open(self.pidFile, "r") as fileObj:
                pidData = json.load(fileObj)
                fileObj.close()

        return pidData

    def create_pid_data(self, pid):
        processObj = psutil.Process(pid)
        creationTime = processObj.create_time()
        cid = md5(str(pid) + str(creationTime)).hexdigest()

        pidData = {
            "pid": pid,
            "creationTime": creationTime,
            "cid": cid
        }

        return pidData

    def process_is_running(self):
        writtenPidData = self.__read_pid_file__()
        if writtenPidData:
            writtenPid = writtenPidData["pid"]
        else:
            return False

        if psutil.pid_exists(writtenPid):
            runningPidData = self.create_pid_data(writtenPid)
        else:
            return False

        if writtenPidData["cid"] == runningPidData["cid"]:
            return True
        else:
            return False

    def create_process(self, commandStringList):
        if self.process_is_running():
            return "Process already running"
        else:
            process = subprocess.Popen(commandStringList)
            pid = process.pid
            pidData = self.create_pid_data(pid)
            self.__write_pid_file__(pidData)
            return "Process started"

    def stop_process(self):
        if self.process_is_running():
            pidData = self.__read_pid_file__()
            pid = pidData["pid"]
            processObj = psutil.Process(pid)
            processObj.terminate()
            processObj.wait()
            return "Process terminated"
        else:
            return "Process not running"

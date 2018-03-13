from modules.process_control import ProcessControl
import unittest
import json
import os

CURRENTTDIR = os.path.dirname(os.path.abspath(__file__))
TESTSCRIPT = os.path.join(CURRENTTDIR, "process_for_tests.py")
PIDFILE = os.path.join(CURRENTTDIR, "test.pid")


class TestWritePidFile(unittest.TestCase):

    def setUp(self):
        self.pidData = {
            "pid": 1111,
            "creationTime": 1520718076.0,
            "cid": "01bb03aef04386e980c57466d2f0b013"
        }

    def tearDown(self):
        os.remove(PIDFILE)

    def test_file_is_written_as_expected(self):
        ProcessControl(PIDFILE).__write_pid_file__(self.pidData)

        with open(PIDFILE, "r") as fileObj:
            pidData = json.load(fileObj)
            fileObj.close()

        self.assertEqual(self.pidData, pidData)


class TestReadPidFile(unittest.TestCase):

    def setUp(self):
        self.pidData = {
            "pid": 1111,
            "creationTime": 1520718076.0,
            "cid": "01bb03aef04386e980c57466d2f0b013"
        }
        ProcessControl(PIDFILE).__write_pid_file__(self.pidData)

    def tearDown(self):
        os.remove(PIDFILE)

    def test_file_is_successfully_read(self):
        pidData = ProcessControl(PIDFILE).__read_pid_file__()

        self.assertEqual(self.pidData, pidData)


class TestCreateProcess(unittest.TestCase):

    def tearDown(self):
        os.remove(PIDFILE)
        ProcessControl(PIDFILE).stop_process()

    def test_proccess_is_created(self):
        instance = ProcessControl(PIDFILE)
        instance.create_process(["python", TESTSCRIPT])
        isRunning = instance.process_is_running()

        self.assertTrue(isRunning)

    def test_expected_string_returned_when_process_is_created(self):
        returnedValue = ProcessControl(PIDFILE).create_process(["python", TESTSCRIPT])
        expectedValue = "Process started"

        self.assertEqual(returnedValue, expectedValue)

    def test_expected_string_returned_when_process_is_already_running(self):
        ProcessControl(PIDFILE).create_process(["python", TESTSCRIPT])
        returnedValue = ProcessControl(PIDFILE).create_process(["python", TESTSCRIPT])
        expectedValue = "Process already running"

        self.assertEqual(returnedValue, expectedValue)


class TestStopProcess(unittest.TestCase):

    def setUp(self):
        ProcessControl(PIDFILE).stop_process()
        ProcessControl(PIDFILE).create_process(["python", TESTSCRIPT])

    def tearDown(self):
        os.remove(PIDFILE)

    def test_process_is_terminated(self):
        instance = ProcessControl(PIDFILE)
        instance.stop_process()
        isRunning = instance.process_is_running()

        self.assertFalse(isRunning)

    def test_expected_string_returned_when_process_is_terminated(self):
        returnedValue = ProcessControl(PIDFILE).stop_process()
        expectedValue = "Process terminated"

        self.assertEqual(returnedValue, expectedValue)

    def test_expected_string_returned_when_process_is_not_running(self):
        ProcessControl(PIDFILE).stop_process()
        returnedValue = ProcessControl(PIDFILE).stop_process()
        expectedValue = "Process not running"

        self.assertEqual(returnedValue, expectedValue)


class TestCreatePidData(unittest.TestCase):

    def setUp(self):
        self.instance = ProcessControl(PIDFILE)
        self.instance.create_process(["python", TESTSCRIPT])
        self.pidData = self.instance.__read_pid_file__()

    def tearDown(self):
        self.instance.stop_process()

    def test_dictionary_is_returned(self):

        self.assertIsInstance(self.pidData, dict)

    def value_are_expected_data_types(self):
        pid = self.pidData["pid"]
        creationTime = self.pidData["creationTime"]
        cid = self.pidData["cid"]

        self.assertIsInstance(pid, int)
        self.assertIsInstance(creationTime, float)
        self.assertIsInstance(cid, str)


class TestProcessIsRunning(unittest.TestCase):

    def setUp(self):
        self.instance = ProcessControl(PIDFILE)
        self.instance.create_process(["python", TESTSCRIPT])
        self.pidData = self.instance.__read_pid_file__()

    def test_true_is_returned_when_process_is_running(self):
        returnedValue = self.instance.process_is_running()

        self.assertTrue(returnedValue)

    def test_false_is_returned_when_pid_isnt_running(self):
        self.instance.stop_process()
        returnedValue = self.instance.process_is_running()

        self.assertFalse(returnedValue)

    def test_false_is_returned_when_pid_is_running_but_cid_dont_match(self):
        self.pidData["cid"] = "01"
        self.instance.__write_pid_file__(self.pidData)

        returnedValue = self.instance.process_is_running()

        self.assertFalse(returnedValue)

    def test_false_is_returned_when_pid_file_doesnt_exist(self):
        self.instance.stop_process()
        os.remove(PIDFILE)
        returnedValue = self.instance.process_is_running()

        self.assertFalse(returnedValue)


if __name__ == "__main__":
    unittest.main()

import unittest
import os

DIRPATH = os.path.dirname(os.path.realpath(__file__))

loader = unittest.TestLoader()
suite = loader.discover(DIRPATH)

testRunner = unittest.runner.TextTestRunner()
testRunner.run(suite)

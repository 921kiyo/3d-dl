import sys

ext = 'D:/Anaconda3/envs/tensorflow/Lib/site-packages/'
boop = 'D:/PycharmProjects/Lobster/src/'
if not (ext in sys.path):
    sys.path.append(ext)
if not (boop in sys.path):
    sys.path.append(boop)

import coverage

cov = coverage.Coverage()
cov.start()


from rendering.testBlenderAPI.TestBlenderObjects import BlenderObjectTest
from rendering.testBlenderAPI.TestBlenderCamera import BlenderCameraTest

import unittest

if __name__ == '__main__':

    suites = []
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderObjectTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderCameraTest))
    alltests = unittest.TestSuite(suites)
    success = unittest.TextTestRunner().run(alltests).wasSuccessful()

cov.stop()
cov.save()
cov.html_report()


import sys


boop = 'D:/PycharmProjects/Lobster/src/'
if not (boop in sys.path):
    sys.path.append(boop)
ext = 'D:/Anaconda3/envs/tensorflow/Lib/site-packages/'
if not (ext in sys.path):
    sys.path.append(ext)

import coverage

cov = coverage.Coverage()
cov.start()


from rendering.testBlenderAPI.TestBlenderObjects import BlenderObjectTest
from rendering.testBlenderAPI.TestBlenderCamera import BlenderCameraTest
from rendering.testBlenderAPI.TestBlenderShapes import BlenderShapeTest
from rendering.testBlenderAPI.TestBlenderScene import BlenderSceneTest
from rendering.testBlenderAPI.TestBlenderMesh import BlenderMeshTest
from rendering.testBlenderAPI.TestBlenderLamps import BlenderLampsTest
from rendering.testBlenderAPI.TestBlenderNode import BlenderMixShaderNodeTest



import unittest

if __name__ == '__main__':

    suites = []
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderObjectTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderCameraTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderShapeTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderSceneTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderMeshTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderLampsTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderMixShaderNodeTest))
    alltests = unittest.TestSuite(suites)
    success = unittest.TextTestRunner().run(alltests).wasSuccessful()

cov.stop()
cov.save()
cov.html_report()


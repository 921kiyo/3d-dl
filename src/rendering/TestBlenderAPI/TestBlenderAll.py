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


from rendering.TestBlenderAPI.TestBlenderObjects import BlenderObjectTest
from rendering.TestBlenderAPI.TestBlenderCamera import BlenderCameraTest
from rendering.TestBlenderAPI.TestBlenderShapes import BlenderShapeTest
from rendering.TestBlenderAPI.TestBlenderScene import BlenderSceneTest
from rendering.TestBlenderAPI.TestBlenderScene import BlenderRandomSceneTest
from rendering.TestBlenderAPI.TestBlenderMesh import BlenderMeshTest
from rendering.TestBlenderAPI.TestBlenderLamps import BlenderLampsTest
from rendering.TestBlenderAPI.TestBlenderNode import BlenderNodeTest



import unittest

if __name__ == '__main__':

    suites = []
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderObjectTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderCameraTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderShapeTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderSceneTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderRandomSceneTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderMeshTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderLampsTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderNodeTest))
    alltests = unittest.TestSuite(suites)
    success = unittest.TextTestRunner().run(alltests).wasSuccessful()

cov.stop()
cov.save()
cov.html_report()


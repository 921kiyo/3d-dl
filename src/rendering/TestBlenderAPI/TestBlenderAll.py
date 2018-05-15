import sys


boop = 'D:\\PycharmProjects\\Lobster\\src\\'
if not (boop in sys.path):
    sys.path.append(boop)
ext = 'D:\\Python\\Python35\\Lib\\site-packages'
if not (ext in sys.path):
    sys.path.append(ext)

import coverage

cov = coverage.Coverage()
cov.start()


from .TestBlenderObjects import BlenderObjectTest
from .TestBlenderCamera import BlenderCameraTest
from .TestBlenderShapes import BlenderShapeTest
from .TestBlenderScene import BlenderSceneTest
from .TestBlenderScene import BlenderRandomSceneTest
from .TestBlenderMesh import BlenderMeshTest
from .TestBlenderLamps import BlenderLampsTest
from .TestBlenderNode import BlenderNodeTest



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


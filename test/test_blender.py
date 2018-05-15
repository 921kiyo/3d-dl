import sys
import unittest
import os


# Get arguments passed to blender
argv = sys.argv
if "--" not in argv:
    argv = []  # as if no args are passed
else:
    argv = argv[argv.index("--") + 1:]  # get all args after "--"

# Ensure source directory in Blender python path
project_dir = argv[0]
sys.path.append(os.path.join(project_dir, 'src'))

# Ensure coverage directory in Blender python path
site_packages_dir = argv[1]
sys.path.append(site_packages_dir)
import coverage

# User-supplied branch preference
if argv[2] == 'True':
    report_branch = True
else:
    report_branch = False

""" --------------- Configure Coverage.py ------------- """
coverage_data_dir = os.path.join(project_dir, 'test', 'coverage', 'data_blender')
cov = coverage.Coverage(include=["*/BlenderAPI/*.py"], branch=report_branch, data_file=coverage_data_dir)

cov.start()


""" --------------- Module Imports ------------- """
from rendering.TestBlenderAPI.TestBlenderObjects import BlenderObjectTest
from rendering.TestBlenderAPI.TestBlenderCamera import BlenderCameraTest
from rendering.TestBlenderAPI.TestBlenderShapes import BlenderShapeTest
from rendering.TestBlenderAPI.TestBlenderScene import BlenderSceneTest
from rendering.TestBlenderAPI.TestBlenderScene import BlenderRandomSceneTest
from rendering.TestBlenderAPI.TestBlenderMesh import BlenderMeshTest
from rendering.TestBlenderAPI.TestBlenderLamps import BlenderLampsTest

if __name__ == '__main__':

    suites = []
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderObjectTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderCameraTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderShapeTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderSceneTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderMeshTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderLampsTest))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderRandomSceneTest))

    alltests = unittest.TestSuite(suites)
    success = unittest.TextTestRunner().run(alltests).wasSuccessful()

cov.stop()
cov.save()

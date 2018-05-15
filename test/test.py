import sys
import os
import pathlib
import unittest
import coverage
import argparse
import subprocess
import site

# Ensure source directory is in python path
project_dir = str(pathlib.Path(__file__).parents[1].resolve())
sys.path.append(os.path.join(project_dir, 'src'))
sys.path.append(os.path.join(project_dir, 'flask_webserver'))
sys.path.append(os.path.join(project_dir, 'kerasmodels'))

# for keras
sys.path.append(project_dir)

""" --------------- CLI setup ------------- """
parser = argparse.ArgumentParser(description='Run all Ocado project tests and record coverage.')

parser.add_argument('-b', '--blender_tests', action='store_true',
                    help='run BlenderAPI tests (requires blender to be installed and in system path)')

parser.add_argument('-k', '--keras_tests', action='store_true',
                    help='run keras tests')

parser.add_argument('-s', '---scene_tests', action='store_true',
                    help='run RandomLib and SceneLib tests')

parser.add_argument('-p', '--pipeline_tests', action='store_true',
                    help='run pipeline tests')

parser.add_argument('-f', '--flask_tests', action='store_true',
                    help='run flask tests')

parser.add_argument('-at', '--all_tests', action='store_true',
                    help='run all tests')

parser.add_argument('-rt', '--report_tests', action='store_true',
                    help='include test files in coverage report')

parser.add_argument('-rb', '--report_branch', action='store_true',
                    help='include branch coverage (see XML report for detailed figures)')


args = parser.parse_args()

print(args)

""" --------------- Run blender tests ------------- """

# virtualenv uses its own site module, which doesn't include getsitepackages()
from distutils.sysconfig import get_python_lib

# site_packages = site.getsitepackages()[0]
site_packages = get_python_lib()

# set path to blender
# blender_path = 'blender'
blender_path = '/vol/project/2017/530/g1753002/Blender/blender-2.79-linux-glibc219-x86_64/blender' # for GPU04

if args.blender_tests or args.all_tests:
    blender_script_dir = os.path.join(project_dir, 'test', 'test_blender.py')
    blender_args = [blender_path, '--background', '--python', blender_script_dir,
                    '--', project_dir, site_packages, str(args.report_branch)]

    print('Running Blender tests')
    subprocess.check_call(blender_args)
    print('Blender tests complete')


""" --------------- Configure Coverage.py ------------- """
coverage_data_dir = os.path.join(project_dir, 'test', 'coverage', 'data')
cov = coverage.Coverage(omit=['*lib*', '*__init__*'], branch=args.report_branch, data_file=coverage_data_dir)

cov.start()

""" --------------- Module Imports ------------- """
# Import keras
if args.keras_tests or args.all_tests:
    # from kerasmodels.testRetrainTest.keras_eval_test import KerasEvalTest
    from kerasmodels.retrain_unittest import TestKerasRetrain

# Import scenes
if args.scene_tests or args.all_tests:
    # Import randomLib
    from src.rendering.TestRandomLib.TestMetaballs import Testturbulence
    from src.rendering.TestRandomLib.TestRandomRender import Testturbulence as render_Testturbulence
    from src.rendering.TestRandomLib.TestTurbulence import Testturbulence as turbulence_Testturbulence
    from src.rendering.TestRandomLib.TestRandBack import TestResizeImages as rand_TestResizeImages

    # Import merge/resize
    from src.rendering.TestSceneLib.TestMergeResize import TestResizeImages

# Import pipelines
if args.pipeline_tests or args.all_tests:
    from src.rendering.TestPipeline.TestRenderPipeline import TestPipeline
    from src.rendering.TestPipeline.TestSlackReporter import TestSlack

# Import flask
if args.flask_tests or args.all_tests:
    from flask_webserver.flask_tests import TestFlaskImplementations

""" --------------- Load Test Cases ------------- """
suites = []

# Load Keras tests
if args.keras_tests or args.all_tests:
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(TestKerasRetrain))

# Load scene tests
if args.scene_tests or args.all_tests:
    # Load randomLib
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(Testturbulence))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(render_Testturbulence))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(turbulence_Testturbulence))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(rand_TestResizeImages))

    # Load sceneLib
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(TestResizeImages))

# Load pipeline tests
if args.pipeline_tests or args.all_tests:
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(TestPipeline))
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(TestSlack))

# Load flask tests
if args.flask_tests or args.all_tests:
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(TestFlaskImplementations))


""" --------------- Run tests ------------- """

if suites:
    tests = unittest.TestSuite(suites)
    success = unittest.TextTestRunner().run(tests).wasSuccessful()

cov.stop()


""" ---------------Save and Combine Results ------------- """
cov.save()

data_paths = [os.path.join(project_dir, 'test', 'coverage', 'data')]
if args.blender_tests or args.all_tests:
    data_paths.append(os.path.join(project_dir, 'test', 'coverage', 'data_blender'))

# if args.keras_tests or args.all_tests:
#     data_paths.append(os.path.join(project_dir, 'test', 'coverage', 'data_keras'))

if args.blender_tests or args.all_tests:
    cov.combine(data_paths=data_paths)


omit = ['*testBlenderAPI*', '*TestRandomLib*', '*TestSceneLib*', '*test_*', '*retrain_unittest*', '*flask_tests*', '*testRetrainTest*']
if args.report_tests:
    omit = []

cov.report(omit=omit)

coverage_html_dir = os.path.join(project_dir, 'test', 'coverage', 'htmlcov')
coverage_xml_dir = os.path.join(project_dir, 'test', 'coverage', 'xmlcov', 'report.xml')
cov.html_report(omit=omit, directory=coverage_html_dir)
cov.xml_report(omit=omit, outfile=coverage_xml_dir)


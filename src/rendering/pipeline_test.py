import site
import os
import subprocess
import pathlib
import sys


# Ensure source directory is in python path
src_dir = str(pathlib.Path(__file__).parents[1].resolve())
sys.path.append(os.path.join(src_dir))

print(src_dir)


def generate_poses(object_folder, output_folder):
    "Make a call to Blender to generate poses"
    # python_sites = site.getsitepackages()[0]
    # python_sites = '/vol/project/2017/530/g1753002/ocadovenv/ocadovenv/lib/python3.5/site-packages'

    blender_path = '/vol/project/2017/530/g1753002/Blender/blender-2.79-linux-glibc219-x86_64/blender'
    blender_script_path = os.path.join(src_dir, 'rendering', 'render_poses.py')
    config_file_path = os.path.join(src_dir, 'rendering', 'config.json')

    blender_args = [blender_path, '--background', '--python', blender_script_path, '--',
                    src_dir,
                    config_file_path,
                    object_folder,
                    output_folder]

    # blender_args = [blender_path, '--background', '--python']

    print('Rendering')
    subprocess.check_call(blender_args)
    print('Renedring done!')

generate_poses('', '');


# """ --------------- Run blender tests ------------- """
# if args.blender_tests:
#     blender_script_dir = os.path.join(project_dir, 'test', 'test_blender.py')
#     blender_args = ['blender', '--background', '--python', blender_script_dir,
#                     '--', project_dir, site.getsitepackages()[0], str(args.report_branch)]
#
#     print('Running Blender tests')
#     subprocess.check_call(blender_args)
#     print('Blender tests complete')





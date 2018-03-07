"""
This example script creates a box in the middle of a half room
"""

import os
import bpy
import rendering.BlenderAPI as bld

class RenderInterface(object):
    """
    Provides a high-level interface to the rendering engine (and the background
    generation as well hopefully)
    The main attribute of this interface is the BlenderRandomScene self.scene.
    This provides all the require methods to generate a random scene with
    the specified subject, with respect to the distributions on the random
    variables involved.
    """
    def __init__(self, num_images=None):
        """
        :param num_images: number of images to render on render_all()
        """
        self.num_images = num_images
        self.scene = None
        self.setup_blender()

    def setup_blender(self):
        """
        To be called on the first time blender is launched. Performs clean-up and
        setup of the scene, and instantiates the BlenderRandomScene class that
        controls all rendering
        :return: None
        """
        C = bpy.context
        C.user_preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
        C.user_preferences.addons['cycles'].preferences.devices[0].use = True
        C.scene.render.engine = 'CYCLES'
        # instantiate scene
        self.scene = bld.BlenderRandomScene(bpy.data.scenes[0])
        # delete the initial cube
        cube = bld.BlenderCube(reference=bpy.data.objects['Cube'])
        cube.delete()
        # Fetch the camera and lamp
        cam = bld.BlenderCamera(bpy.data.objects['Camera'])
        self.scene.set_render()
        self.scene.add_camera(cam)

    def load_subject(self, obj_path, texture_path, output_file):
        """
        Loads a single subject into the RandomScene
        :param obj_path:
        :param texture_path:
        :param output_file:
        :return:
        """
        self.output_file = output_file
        self.scene.load_subject_from_path(obj_path=obj_path, texture_path=texture_path)

    def change_output_file(self, new_output_file):
        self.output_file = new_output_file

    def set_attribute_distribution_params(self, *args):
        """
        Interface to the method with identical name in BlenderRandomScene:

        Description from BlenderRandomScene:
        Sets the parameter of the distribution of an attribute attr.
        param has to exist in the distribution that is is associated with
        attr. For instance, if attr is assigned a UniformCDist, and
        is asked to change the param "mu", this will throw a KeyError.

        :param args:
        :return:
        """
        self.scene.set_attribute_distribution_params(*args)

    def set_attribute_distribution(self, attr, params):
        """
        Interface to the method with identical name in BlenderRandomScene:

        Description from BlenderRandomScene:

        Sets the distribution of attribute specified by attr. params is
        a dictionary containig the following:

        - 'dist': str ( this gives the distribution name which will go
        into a lookup table in random_render.DIstributionFactory, and will
        return a distribution object identified by the name. Look in
        RandomLib.random_render.py for a full list)
        - everything else will be a dict of kwargs that the constructor for
        the specified distribution expects.

        For instance, to assign a uniform distribution to lamp_energy with
        lower bound 500.0 and upper bound 1000.0. Since the constructor for
        UniformCDist is: "def __init__(self, l=None, r=None, **kwargs)", and
        DistributionFactory maps "UniformD" to that distribution, we should
        specify param as:
        {'dist':'UniformD', 'l':500.0, 'r':1000.0}

        :param attr:
        :param params:
        :return:
        """
        self.scene.set_attribute_distribution(attr, params)

    def render_all(self, dump_logs=False, visualize=False):
        for i in range(self.num_images):
            # **********************  RENDER N SAVE **********************
            render_path = os.path.join(self.output_file, 'render%d.png' % i)
            self.scene.render_to_file(render_path)
        logs = self.scene.retrieve_logs()

        if dump_logs:
            import json
            dump_file = os.path.join(self.output_file, 'randomvars_dump.json')
            with open(dump_file, "w+") as f:
                json.dump(logs, f, sort_keys=True, indent=4, separators=(',', ': '))

        if visualize:
            from mpl_toolkits.mplot3d import Axes3D
            import matplotlib.pyplot as plt
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            camera_locations = logs['camera_loc']
            X = [loc[0] for loc in camera_locations]
            Y = [loc[1] for loc in camera_locations]
            Z = [loc[2] for loc in camera_locations]
            ax.scatter(X, Y, zs=Z)
            ax.set_zlim([-1, 1])
            ax.set_ylim([-1, 1])
            ax.set_xlim([-1, 1])
            dump_file = os.path.join(self.output_file, 'camera_loc.png')
            plt.savefig(dump_file)


        return logs
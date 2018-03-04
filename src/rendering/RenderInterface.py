"""
This example script creates a box in the middle of a half room
"""

import os
import bpy
import rendering.BlenderAPI as bld

class RenderInterface(object):
    def __init__(self, num_images=None):
        self.num_images = num_images
        self.scene = None
        self.setup_blender()

    def setup_blender(self):
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
        self.output_file = output_file
        self.scene.load_subject_from_path(obj_path=obj_path, texture_path=texture_path)

    def set_attribute_distribution_params(self, *args):
        self.scene.set_attribute_distribution_params(*args)

    def set_attribute_distribution(self, attr, params):
        self.scene.set_attribute_distribution(attr, params)

    def render_all(self):
        for i in range(self.num_images):
            # **********************  RENDER N SAVE **********************
            render_path = os.path.join(self.output_file, 'render%d.png' % i)
            self.scene.render_to_file(render_path)
        return self.scene.retrieve_logs()
import bpy
import math
import random
import mathutils as mathU
import itertools

from BlenderObjects import *
from BlenderNodes import *


class BlenderMesh(BlenderObject):

    def __init__(self, **kwargs):
        super(BlenderMesh, self).__init__(**kwargs)
        self.nodes = {}
        self.links = None
        self.node_tree = None
        self.material = None
        self.setup_node_tree()

    def setup_node_tree(self):

        obj_name = self.reference.name
        if (len(self.reference.data.materials) == 0):
            mat = bpy.data.materials.new(name="Mat" + "_" + obj_name)  # set new material to variable
            self.reference.data.materials.append(mat)  # add the material to the object
        self.material = self.reference.data.materials[0]
        self.reference.data.materials[0].use_nodes = True

        self.node_tree = self.material.node_tree
        self.nodes['node_mat'] = BlenderMaterialOutputNode(self.node_tree,
                                                           reference=self.node_tree.nodes['Material Output'])
        self.nodes['node_diff'] = BlenderDiffuseBSDFNode(self.node_tree, reference=self.node_tree.nodes['Diffuse BSDF'])
        self.nodes['node_gloss'] = BlenderGlossyBSDFNode(self.node_tree)
        self.nodes['node_mix'] = BlenderMixShaderNode(self.node_tree)
        self.links = self.node_tree.links
        self.links.new(self.nodes['node_mix'].get_shader_output(), self.nodes['node_mat'].get_surface_input())
        self.links.new(self.nodes['node_diff'].get_bsdf_output(), self.nodes['node_mix'].get_shader1_input())
        self.links.new(self.nodes['node_gloss'].get_bsdf_output(), self.nodes['node_mix'].get_shader2_input())

    def set_diffuse(self, color=(0.5, 0.5, 0.5, 1), rough=0.5):
        self.nodes['node_diff'].set_color(*color)
        self.nodes['node_diff'].set_roughness(rough)

    def set_gloss(self, color=(0.5, 0.5, 0.5, 1), rough=0.5):
        self.nodes['node_gloss'].set_color(*color)
        self.nodes['node_gloss'].set_roughness(rough)

    def set_mixer(self, factor):
        self.nodes['node_mix'].set_fac(factor)

    def add_image_texture(self, image_path, projection='FLAT', mapping='UV'):

        if not 'node_imgtex' in self.nodes.keys():
            self.nodes['node_imgtex'] = BlenderImageTextureNode(self.node_tree)
        if not 'node_texcoord' in self.nodes.keys():
            self.nodes['node_texcoord'] = BlenderTexCoordNode(self.node_tree)

        try:
            img = bpy.data.images.load(image_path)
        except:
            return False

        success = self.nodes['node_imgtex'].set_projection(projection) and self.nodes['node_imgtex'].set_image(img)
        if not success:
            return success

        if mapping not in ['UV', 'Generated']:
            return False

        if mapping == 'Generated':
            vector = self.nodes['node_texcoord'].get_Generated_output()
        else:
            vector = self.nodes['node_texcoord'].get_UV_output()
        self.links.new(vector, self.nodes['node_imgtex'].get_vector_input())
        self.links.new(self.nodes['node_imgtex'].get_color_output(), self.nodes['node_diff'].get_color_input())
        self.links.new(self.nodes['node_imgtex'].get_color_output(), self.nodes['node_gloss'].get_color_input())

    def toggle_smooth(self):
        for poly in self.reference.data.polygons:
            poly.use_smooth = True


class BlenderCube(BlenderMesh):
    def __init__(self, **kwargs):
        super(BlenderCube, self).__init__(**kwargs)

    def blender_create_operation(self, location):
        bpy.ops.mesh.primitive_cube_add(location=location)


class BlenderPlane(BlenderMesh):
    def __init__(self, **kwargs):
        super(BlenderPlane, self).__init__(**kwargs)

    def blender_create_operation(self, location):
        bpy.ops.mesh.primitive_plane_add(location=location)


class BlenderImportedShape(BlenderMesh):
    def __init__(self, **kwargs):
        super(BlenderImportedShape, self).__init__(**kwargs)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

    def blender_create_operation(self, location, obj_path=None):
        assert obj_path is not None, "Required keyword argument for importing shape: obj_path=[filepath]"
        bpy.ops.import_scene.obj(filepath=obj_path)





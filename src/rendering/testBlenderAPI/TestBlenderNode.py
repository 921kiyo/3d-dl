import bpy
import sys

boop = "/Users/maxbaylis/Lobster/src/"
if not (boop in sys.path):
    sys.path.append(boop)

import rendering.BlenderAPI as bld
from rendering.BlenderAPI.BlenderNodes import *

import unittest



class TestBlenderNode(unittest.TestCase):


    # to create a blendernode ob, pass node tree for hwhich it belongs to.
    # Node tree has to be tied to a mesg.
    # 1. creat by.ops.object. cube.ad cube
    #  pass subes node tree to belndernode
    # create bendelernoe ot type something
    # chechek nodetree has node of type in it.
    #
    # import bpu
    import bpy.data.on
    # changes render engine to cycles render as this is where nodes work.
    # cube.materials.use_ndoes=true
    # cube.data.m,aterials[0].nodetree.nodes.['Diffuse'].inputs
    #2. get the node tree into
    # but iwth a dummy sub class
    #node = BlenderNode(nodetree, type=Glossy...)

    #install blender on exe.


    # add code to writeup?

    def setUp(self):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        self.reference = self.node_tree.nodes.new(type=type)

        self.nodes = {}
        self.links = None
        self.node_tree = None
        self.material = None

        obj_name = self.reference.name
        if len(self.reference.data.materials == 0):
            mat = bpy.data.materials.new(name="Mat" + "_" + obj_name)  # set new material to variable
            self.reference.data.materials.append(mat)  # add the material to the object

        self.material = self.reference.data.materials[0]
        self.reference.data.materials[0].use_nodes = True # creates a node tree

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

    def tearDown(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()


    def test_get_input(self):
        self.fail()

    def test_get_output(self):
        self.fail()

    def test_set_input(self):
        self.fail()


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestBlenderNode)
    # suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(BlenderSunTest))
    success = unittest.TextTestRunner(verbosity=True).run(suite).wasSuccessful()



import bpy
import sys
import unittest

boop = "/Users/maxbaylis/Lobster/src/"
if not (boop in sys.path):
    sys.path.append(boop)

import rendering.BlenderAPI as bld
from rendering.BlenderAPI.BlenderExceptions import *


class BlenderNodeTest(unittest.TestCase):

    def setUp(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        C = bpy.context
        C.scene.render.engine = 'CYCLES' # required for nodes to work

        status = bpy.ops.node.new_node_tree(type='ShaderNodeTree', name="NodeTree")
        self.assertEqual(status, {'FINISHED'})
        self.tree = bpy.data.node_groups["NodeTree"]

    def tearDown(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        bpy.data.node_groups.remove(self.tree)

    def test_get_shader1_input(self):
        # Use the node tree
        mix_shader_node = bld.BlenderMixShaderNode(self.tree)
        inputa = mix_shader_node.get_input(1)
        inputb = mix_shader_node.get_shader1_input()
        self.assertEqual(inputa, inputb)

        shader_node_ref = self.tree.nodes[0]
        mix_shader_node.set_fac(0.3)
        self.assertAlmostEqual(shader_node_ref.inputs["Fac"].default_value, 0.3)
        mix_shader_node.set_fac(0.9)
        self.assertAlmostEqual(shader_node_ref.inputs["Fac"].default_value, 0.9)

        caught = False
        try:
            mix_shader_node.set_fac(-0.3)
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)

    def test_glossy_bsdf_inputs(self):
        glossy_node = bld.BlenderGlossyBSDFNode(self.tree)
        glossy_node_ref = self.tree.nodes[0]
        glossy_node.set_color(0.5,0.5,0.5,1.0)
        self.assertAlmostEqual(glossy_node_ref.inputs["Color"].default_value[0], 0.5)
        self.assertAlmostEqual(glossy_node_ref.inputs["Color"].default_value[1], 0.5)
        self.assertAlmostEqual(glossy_node_ref.inputs["Color"].default_value[2], 0.5)
        self.assertAlmostEqual(glossy_node_ref.inputs["Color"].default_value[3], 1.0)

        glossy_node.set_color(0.8, 0.5, 0.2, 0.3)
        self.assertAlmostEqual(glossy_node_ref.inputs["Color"].default_value[0], 0.8)
        self.assertAlmostEqual(glossy_node_ref.inputs["Color"].default_value[1], 0.5)
        self.assertAlmostEqual(glossy_node_ref.inputs["Color"].default_value[2], 0.2)
        self.assertAlmostEqual(glossy_node_ref.inputs["Color"].default_value[3], 0.3)

        caught = False
        try:
            glossy_node.set_color(0.8, 0.5, 0.2, 1.5)
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)

        glossy_node.set_roughness(0.3)
        self.assertAlmostEqual(glossy_node_ref.inputs["Roughness"].default_value, 0.3)
        glossy_node.set_roughness(0.9)
        self.assertAlmostEqual(glossy_node_ref.inputs["Roughness"].default_value, 0.9)

        caught = False
        try:
            glossy_node.set_roughness(-0.3)
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)


    def test_diffuse_bsdf_inputs(self):
        diffuse_node = bld.BlenderDiffuseBSDFNode(self.tree)
        diffuse_node_ref = self.tree.nodes[0]
        diffuse_node.set_color(0.5,0.5,0.5,1.0)
        self.assertAlmostEqual(diffuse_node_ref.inputs["Color"].default_value[0], 0.5)
        self.assertAlmostEqual(diffuse_node_ref.inputs["Color"].default_value[1], 0.5)
        self.assertAlmostEqual(diffuse_node_ref.inputs["Color"].default_value[2], 0.5)
        self.assertAlmostEqual(diffuse_node_ref.inputs["Color"].default_value[3], 1.0)

        diffuse_node.set_color(0.8, 0.5, 0.2, 0.3)
        self.assertAlmostEqual(diffuse_node_ref.inputs["Color"].default_value[0], 0.8)
        self.assertAlmostEqual(diffuse_node_ref.inputs["Color"].default_value[1], 0.5)
        self.assertAlmostEqual(diffuse_node_ref.inputs["Color"].default_value[2], 0.2)
        self.assertAlmostEqual(diffuse_node_ref.inputs["Color"].default_value[3], 0.3)

        caught = False
        try:
            diffuse_node.set_color(0.8, 0.5, 0.2, 1.5)
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)

        diffuse_node.set_roughness(0.3)
        self.assertAlmostEqual(diffuse_node_ref.inputs["Roughness"].default_value, 0.3)
        diffuse_node.set_roughness(0.9)
        self.assertAlmostEqual(diffuse_node_ref.inputs["Roughness"].default_value, 0.9)

        caught = False
        try:
            diffuse_node.set_roughness(-0.3)
        except InvalidInputError:
            caught = True
        self.assertTrue(caught)

    def test_get_invalid_inputs(self):
        mix_shader_node = bld.BlenderMixShaderNode(self.tree)
        input = mix_shader_node.get_input(1000)
        self.assertIsNone(input)
        input = mix_shader_node.get_input('InvalidInput')
        self.assertIsNone(input)
        output = mix_shader_node.get_output(1000)
        self.assertIsNone(output)
        input = mix_shader_node.get_output('InvalidOutput')
        self.assertIsNone(output)

        success = mix_shader_node.set_input(1000, 3)
        self.assertFalse(success)
        success = mix_shader_node.set_input('InvalidInput', 3)
        self.assertFalse(success)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestBlenderMixShaderNode)
    success = unittest.TextTestRunner(verbosity=True).run(suite).wasSuccessful()



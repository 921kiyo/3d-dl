import bpy
import sys
import unittest

boop = "/Users/maxbaylis/Lobster/src/"
if not (boop in sys.path):
    sys.path.append(boop)

import rendering.BlenderAPI as bld


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



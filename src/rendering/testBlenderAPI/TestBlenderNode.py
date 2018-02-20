import bpy
import sys
import unittest

boop = "/Users/maxbaylis/Lobster/src/"
if not (boop in sys.path):
    sys.path.append(boop)

import rendering.BlenderAPI as bld


class TestBlenderMixShaderNode(unittest.TestCase):

    def setUp(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        C = bpy.context
        C.scene.render.engine = 'CYCLES'

    def tearDown(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    def test_get_shader1_input(self):
        # bpy.ops.mesh.primitive_cube_add(location=(1, 1, 1))
        # cube = bpy.data.objects[0]
        # mat = bpy.data.materials.new(name="Material")
        # cube.data.materials.append(mat)
        # cube.data.materials[0].use_nodes = True
        # tree = cube.data.materials[0].node_tree
        # print(tree)


        bpy.ops.node.new_node_tree(type='ShaderNodeTree', name="NodeTree")
        tree = bpy.data.node_groups["NodeTree"]
        # print(tree)


        mix_shader_node = bld.BlenderMixShaderNode(tree, 'ShaderNodeTree')

        input = mix_shader_node.get_shader1_input()


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestBlenderMixShaderNode)
    success = unittest.TextTestRunner(verbosity=True).run(suite).wasSuccessful()



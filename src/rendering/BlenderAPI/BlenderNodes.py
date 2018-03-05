import bpy
import math
import random
import mathutils as mathU
import itertools


class BlenderNode(object):
    """
    Generic Node object in Blender, with operations to create node, and reference node inputs and outputs
    via indexing or key name. Node tree must always be given, if reference is given, a BlenderNode
    of that reference type is created
    """

    def __init__(self, node_tree, type, reference=None):
        """
        @param node_tree : (Blender Native Object) required, node tree in which this node lives
        @param type : (string) type name of node. ignored if reference provided.
        @param reference : (Blender Native Object) optional, reference to an existing node
        """
        self.node_tree = node_tree
        self.type = type
        if reference is None:
            self.reference = self.node_tree.nodes.new(type=type)
        else:
            self.reference = reference

    def get_input(self, idx):
        if (type(idx) is int) and (idx > len(self.reference.inputs.keys())):
            return None
        if (type(idx) is str) and (idx not in self.reference.inputs.keys()):
            return None
        return self.reference.inputs[idx]

    def get_output(self, idx):
        if (type(idx) is int) and (idx > len(self.reference.outputs.keys())):
            return None
        if (type(idx) is str) and (idx not in self.reference.outputs.keys()):
            return None
        return self.reference.outputs[idx]

    def set_input(self, idx, val):
        input = self.get_input(idx)
        if input is None:
            return False
        input.default_value = val
        return True


class BlenderMixShaderNode(BlenderNode):
    """
    subclass of BlenderNode object
    Mix Shader nodes take in different shader nodes as inputs and outputs a resulting
    mixed shader with respect to a mixing factor
    """

    def __init__(self, node_tree, reference=None):
        super(BlenderMixShaderNode, self).__init__(node_tree, 'ShaderNodeMixShader', reference)

    def get_shader1_input(self):
        return self.get_input(1)

    def get_shader2_input(self):
        return self.get_input(2)

    def get_shader_output(self):
        return self.get_output('Shader')

    def set_fac(self, fac):
        if fac > 1.0:
            fac = 1.0
        self.set_input('Fac', fac)


class BlenderMaterialOutputNode(BlenderNode):
    """
    subclass of BlenderNode object
    Material node takes in a shader node and outputs a surface, used by the rendering
    engine to determine the properties of a material surface
    """

    def __init__(self, node_tree, reference=None):
        super(BlenderMaterialOutputNode, self).__init__(node_tree, None, reference)

    def get_surface_input(self):
        return self.get_input('Surface')


class BlenderDiffuseBSDFNode(BlenderNode):
    """
    subclass of BlenderNode object
    Describes the diffuse properties of a shading. Can be plugged into a mix shader
    """

    def __init__(self, node_tree, reference=None):
        super(BlenderDiffuseBSDFNode, self).__init__(node_tree, 'ShaderNodeBsdfDiffuse', reference)

    def set_color(self, r, g, b, a):
        args = (r, g, b, a)
        for i, arg in enumerate(args):
            if arg > 1.0:
                args[i] = 1.0
        self.set_input('Color', args)

    def set_roughness(self, r):
        if r > 1.0:
            r = 1.0
        self.set_input('Roughness', r)

    def get_bsdf_output(self):
        return self.get_output('BSDF')

    def get_color_input(self):
        return self.get_input('Color')


class BlenderGlossyBSDFNode(BlenderNode):
    """
    subclass of BlenderNode object
    Describes the glossy properties of a shading. Can be plugged into a mix shader
    """

    def __init__(self, node_tree, reference=None):
        super(BlenderGlossyBSDFNode, self).__init__(node_tree, 'ShaderNodeBsdfGlossy', reference)

    def set_color(self, r, g, b, a):
        args = (r, g, b, a)
        for i, arg in enumerate(args):
            if arg > 1.0:
                args[i] = 1.0
        self.set_input('Color', args)

    def set_roughness(self, r):
        if r > 1.0:
            r = 1.0
        self.set_input('Roughness', r)

    def get_bsdf_output(self):
        return self.get_output('BSDF')

    def get_color_input(self):
        return self.get_input('Color')


class BlenderImageTextureNode(BlenderNode):
    """
    subclass of BlenderNode
    Outputs a Color based on a Vector mapping for the surface, given an image.
    """

    def __init__(self, node_tree, reference=None):
        super(BlenderImageTextureNode, self).__init__(node_tree, 'ShaderNodeTexImage', reference)

    def set_projection(self, projection):
        try:
            self.reference.projection = projection
        except TypeError:
            return False
        return True

    def set_image(self, image):
        try:
            self.reference.image = image
        except TypeError:
            return False
        return True

    def get_vector_input(self):
        return self.get_input('Vector')

    def get_color_output(self):
        return self.get_output('Color')


class BlenderTexCoordNode(BlenderNode):
    """
    subclass of BlenderNode
    Outputs a mapping type (usually 'UV' or 'Generated') to be given to a Texture Node,
    to determine the mapping of the colors onto a surface
    """

    def __init__(self, node_tree, reference=None):
        super(BlenderTexCoordNode, self).__init__(node_tree, 'ShaderNodeTexCoord', reference)

    def get_UV_output(self):
        return self.get_output('UV')

    def get_Generated_output(self):
        return self.get_output('Generated')


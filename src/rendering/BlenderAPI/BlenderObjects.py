import bpy
import math
import random
import mathutils as mathU
import itertools


def random_color():
    return random.random(), random.random(), random.random()


def rotate(vector, quaternion):
    vecternion = mathU.Quaternion([0, vector[0], vector[1], vector[2]])
    quanjugate = quaternion.copy()
    quanjugate.conjugate()
    return quaternion * vecternion * quanjugate


def to_quaternion(w, x, y, z):
    m = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    w = math.pi * w / 180.0
    if m == 0:
        q = [0, 0, 0, 0]
    else:
        q = mathU.Quaternion([x / m, y / m, z / m], w)
    return q


def random_shell_coords(radius):
    theta = math.radians(random.uniform(0.0, 360.0))
    phi = math.radians(random.uniform(0.0, 360.0))
    x = radius * math.cos(theta) * math.sin(phi)
    y = radius * math.sin(theta) * math.sin(phi)
    z = radius * math.cos(phi)
    return x, y, z


def random_cartesian_coords(mux, muy, muz, sigma, lim):
    x = min(random.gauss(mux, sigma), lim)
    y = min(random.gauss(muy, sigma), lim)
    z = min(random.gauss(muz, sigma), lim)
    return x, y, z


class BlenderObject(object):
    """
	This class is intended as a wrapper for all objects that can be referenced via the
	bpy.data.objects Collection.
	This includes a number of items like lamps, camera, meshes, assemblies to name a few

	This class is an interface to all these objects, and is meant as an abstract class,
	as the blender_create operation is left to the subclass to implement

	Also included are concrete implementations of methods that are common to all these
	objects. This mostly include geometric operations like rotation, translation etc.

	Also a delete method is implemented
	"""

    def __init__(self, location=(0, 0, 0), orientation=(0, 0, 0, 0), scale=(1, 1, 1), reference=None, **kwargs):
        if reference is None:
            bpy.ops.object.select_all(action='DESELECT')  # deselect everything
            self.blender_create_operation(location, **kwargs)
            assert len(bpy.context.selected_objects) == 1, "more than one selected objects!"
            # make sure the only selected object is the recently created object
            self.reference = bpy.context.selected_objects[0]
        else:
            self.reference = reference
        self.set_rot(*orientation)
        self.set_scale(scale)

    def blender_create_operation(self, location):
        # Attention: for subclass to implement
        raise NotImplementedError

    def set_location(self, location):
        self.reference.location = location

    def set_scale(self, scale):
        self.reference.scale = scale

    def set_rot(self, w, x, y, z):
        self.reference.rotation_mode = 'QUATERNION'
        q = to_quaternion(w, x, y, z)
        self.reference.rotation_quaternion = q

    def get_rot(self):
        return self.reference.rotation_quaternion

    def rotate(self, w, x, y, z):
        self.reference.rotation_mode = 'QUATERNION'
        q = to_quaternion(w, x, y, z)
        q = q * self.reference.rotation_quaternion
        print(q)
        self.reference.rotation_quaternion = q

    def delete(self):
        # deselect all
        bpy.ops.object.select_all(action='DESELECT')
        # selection
        self.reference.select = True
        # remove it
        bpy.ops.object.delete()

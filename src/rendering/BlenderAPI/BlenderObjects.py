import bpy
import math
import random
import mathutils as mathU
import itertools


def random_color():
    """
    utility function for random color, returns a 3-tuple, each element in [0,1]
    :return: 3-tuple representing a color
    """
    return random.random(), random.random(), random.random()


def rotate(vector, quaternion):
    """
    utility function to rotate a vector, given a rotation in the form of a quaternion
    :param vector: vector to rotate
    :param quaternion: rotation in the form of quaternion
    :return : rotated vector
    """
    vecternion = mathU.Quaternion([0, vector[0], vector[1], vector[2]])
    quanjugate = quaternion.copy()
    quanjugate.conjugate()
    return quaternion * vecternion * quanjugate


def to_quaternion(w, x, y, z):
    """
    utility function, given a rotation axis vector x,y,z and and angle w, return the corresponding quaternion
    :param w: angle to rotate
    :param x: x component of the axis vector
    :param y: y component of the axis vector
    :param z: z component of the axis vector
    :return: 4-tuple quaternion
    """
    m = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    w = math.pi * w / 180.0
    if m == 0:
        q = [0, 0, 0, 0]
    else:
        q = mathU.Quaternion([x / m, y / m, z / m], w)
    return q


def random_shell_coords(radius):
    """
    given a shell radius, return a random shell coordinate centred around (0,0,0)
    :param radius: radius of shell
    :return: 3-tuple shell coordinate
    """
    theta = math.radians(random.uniform(0.0, 360.0))
    phi = math.radians(random.uniform(0.0, 360.0))
    x = radius * math.cos(theta) * math.sin(phi)
    y = radius * math.sin(theta) * math.sin(phi)
    z = radius * math.cos(phi)
    return x, y, z


def random_cartesian_coords(mux, muy, muz, sigma, lim):
    """
    given a centre (mux, muy, muz), a standard deviation sigma, and a cube width lim,
    generate a gaussian-distributed random coordinate within the cube centered at (mux,muy,muz)
    :param mux: x centre
    :param muy: y centre
    :param muz: z centre
    :param sigma: standard deviation
    :param lim: cube limit width
    :return: 3-tuple gaussian random coordinate
    """
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
        # Attention: Pure virtual, for subclass to implement
        raise NotImplementedError

    def set_location(self, x, y, z):
        """
        set location of current 
        """
        self.reference.location = (x,y,z)

    def set_scale(self, scale):
        """
        set the scale of current object
        :param scale: 3-tuple specifying scale of the x,y,z axes
        """
        self.reference.scale = scale

    def set_rot(self, w, x, y, z):
        """
        set rotation of object, w.r.t to initial pose
        :param w: angle
        :param x: x component of rotation vector
        :param y: y component of rotation vector
        :param z: z component of rotation vector
        """
        self.reference.rotation_mode = 'QUATERNION'
        q = to_quaternion(w, x, y, z)
        self.reference.rotation_quaternion = q

    def get_rot(self):
        """
        get rotation of object, w.r.t to initial pose
        :return: 4-tuple quternion
        """
        return self.reference.rotation_quaternion

    def rotate(self, w, x, y, z):
        """
        rotate object, w.r.t to current pose
        :return: None
        """
        self.reference.rotation_mode = 'QUATERNION'
        q = to_quaternion(w, x, y, z)
        q = q * self.reference.rotation_quaternion
        print(q)
        self.reference.rotation_quaternion = q

    def delete(self):
        """
        delete current object, by deleting its reference
        """
        # deselect all
        bpy.ops.object.select_all(action='DESELECT')
        # selection
        self.reference.select = True
        # remove it
        bpy.ops.object.delete()

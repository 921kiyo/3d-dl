import bpy
import math
import random
import mathutils as mathU
import itertools

from rendering.BlenderAPI.BlenderObjects import *
from rendering.BlenderAPI.BlenderExceptions import *


class BlenderLamp(BlenderObject):
    """
    subclasses BlenderObject.
    This is the base class to represent all types of lamps, including but not limited to:
    Point Lamps, Area Lamps, and Sun. 
    Every lamp has the following attributes:
    i. data - reference to the native lamp data structure
    ii. default brightness - some default value chosen by eye for an adequate lighting condition
    iii default size - the larger the size, the more diffuse the casted shadows will be    
    """
    
    def __init__(self, obj_reference=None, **kwargs):
        super(BlenderLamp, self).__init__(reference=obj_reference, **kwargs)
        self.data = self.reference.data
        self.default_brightness = 0.0
        self.default_size = 0.0

    def blender_create_operation(self):
        """
        interface method for all BlenderObjects
        """
        bpy.ops.object.lamp_add()

    def delete(self):
        self.turn_on()
        if self.reference is None:
            return # object reference already deleted
        # deselect all
        bpy.ops.object.select_all(action='DESELECT')
        # selection
        self.reference.select = True
        # remove it
        bpy.ops.object.delete()
        self.reference = None
        
    def set_size(self, size):
        if not check_scalar_non_negative(size):
            raise InvalidInputError('lamp size must be non negative')
        self.data.shadow_soft_size = size

    def set_brightness(self, strength):
        """
        Use nodes to set brightness
        """
        if not check_scalar_non_negative(strength):
            raise InvalidInputError('lamp strength must be non negative')
        self.data.use_nodes = True
        self.data.node_tree.nodes["Emission"].inputs["Strength"].default_value = strength

    def turn_off(self):
        """
        push it to second layer to hide
        """
        self.reference.layers[1] = True
        self.reference.layers[0] = False

    def turn_on(self):
        """
        push it to the topmost layer to show
        """
        self.reference.layers[0] = True
        self.reference.layers[1] = False

    def is_on(self):
        return self.reference.layers[0] is True
        
    def face_towards(self, x, y, z):
        """
        given a coordinate x, y, z
        calculate a rotational axis and angle, such that when applied, the central axis
        passes through x,y,z
        """
        # vector of target w.r.t camera
        target = mathU.Vector([x, y, z]) - mathU.Vector(self.reference.location)
        target.normalize()
        # rotational origin of camera is (0,0,-1) for some reason
        rot_origin = mathU.Vector([0, 0, -1])
        rot_origin.normalize()
        # get the rotational axis and angle by crossing the two vectors
        rot_axis = rot_origin.cross(target)
        rot_angle = math.degrees(math.acos(rot_origin.dot(target)))
        # set rotation quaternion
        self.set_rot(rot_angle, rot_axis[0], rot_axis[1], rot_axis[2])


class BlenderSun(BlenderLamp):
    """
    Directional, but position invariant (always from above, at infinity)
    """
    def __init__(self, obj_reference=None, default_brightness=15.0, default_size=0.1, **kwargs):
        super(BlenderSun, self).__init__(obj_reference, **kwargs)
        self.data.type = 'SUN'
        self.default_brightness = default_brightness
        self.default_size = default_size
        self.set_brightness(default_brightness)
        self.set_size(default_size)


class BlenderArea(BlenderLamp):
    """
    Directional, and depends on position. Area 'behind the lamp' will not be illuminated
    """
    def __init__(self, obj_reference=None, default_brightness=500.0, default_size=5.0, **kwargs):
        super(BlenderArea, self).__init__(obj_reference, **kwargs)
        self.data.type = 'AREA'
        self.default_brightness = default_brightness
        self.default_size = default_size
        self.set_brightness(default_brightness)
        self.set_size(default_size)


class BlenderPoint(BlenderLamp):
    """
    Non-directional, source concentrated in a spot.
    """
    def __init__(self, obj_reference=None, default_brightness=5000.0, default_size=5.0, **kwargs):
        super(BlenderPoint, self).__init__(obj_reference, **kwargs)
        self.data.type = 'POINT'
        self.default_brightness = default_brightness
        self.default_size = default_size
        self.set_brightness(default_brightness)
        self.set_size(default_size)


class BlenderTestLamp(BlenderLamp):
    """
    Dummy lamp to test BlenderLamp class without relying on other subclasses
    """
    def __init__(self, obj_reference=None, **kwargs):
        super(BlenderTestLamp, self).__init__(obj_reference, **kwargs)

import bpy
import math
import random
import mathutils as mathU
import itertools

from BlenderObjects import *


class BlenderLamp(BlenderObject):
    def __init__(self, obj_reference):
        super(BlenderLamp, self).__init__(reference=obj_reference)
        self.data = self.reference.data
        self.default_brightness = 0.0
        self.default_size = 0.0

    def blender_create_operation(self, location):
        bpy.ops.object.lamp_add(location=location)

    def set_size(self, size):
        self.data.shadow_soft_size = size

    def set_brightness(self, strength):
        self.data.use_nodes = True
        self.data.node_tree.nodes["Emission"].inputs["Strength"].default_value = strength

    def turn_off(self):
        self.reference.layers[1] = True
        self.reference.layers[0] = False

    def turn_on(self):
        self.reference.layers[0] = True
        self.reference.layers[1] = False

    def face_towards(self, x, y, z):
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

    def random_lighting_conditions(self, reference_location=(0.0, 0.0, 0.0), location_variance=1.0):
        loc = random_cartesian_coords(0.0, 0.0, 0.0, location_variance, 6.0)
        self.face_towards(*loc)
        self.set_brightness(random.gauss(self.default_brightness, 0.3 * self.default_brightness))
        self.set_size(random.gauss(self.default_size, 0.3 * self.default_size))


class BlenderSun(BlenderLamp):
    def __init__(self, obj_reference, default_brightness=15.0, default_size=0.1):
        super(BlenderSun, self).__init__(obj_reference)
        self.data.type = 'SUN'
        self.default_brightness = default_brightness
        self.default_size = default_size
        self.set_brightness(default_brightness)
        self.set_size(default_size)


class BlenderArea(BlenderLamp):
    def __init__(self, obj_reference, default_brightness=500.0, default_size=5.0):
        super(BlenderArea, self).__init__(obj_reference)
        self.data.type = 'AREA'
        self.default_brightness = default_brightness
        self.default_size = default_size
        self.set_brightness(default_brightness)
        self.set_size(default_size)


class BlenderPoint(BlenderLamp):
    def __init__(self, obj_reference, default_brightness=5000.0, default_size=5.0):
        super(BlenderPoint, self).__init__(obj_reference)
        self.data.type = 'POINT'
        self.default_brightness = default_brightness
        self.default_size = default_size
        self.set_brightness(default_brightness)
        self.set_size(default_size)


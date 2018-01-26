import bpy
import math
import random
import mathutils as mathU
import itertools

from BlenderObjects import *


class BlenderCamera(BlenderObject):
    def __init__(self, reference, **kwargs):
        super(BlenderCamera, self).__init__(reference=reference, **kwargs)

    def spin(self, angle):
        q = self.get_rot()
        focal_origin = mathU.Vector([0, 0, -1])
        T = q.to_matrix()
        focal_axis = T * focal_origin
        focal_axis.normalize()
        self.rotate(angle, *focal_axis)

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




import bpy
import math
import random
import mathutils as mathU
import itertools

from rendering.BlenderAPI.BlenderObjects import *


class BlenderCamera(BlenderObject):
    def __init__(self, reference=None, **kwargs):
        super(BlenderCamera, self).__init__(reference=reference, **kwargs)

    def spin(self, angle):
        """
        Spin camera at an angle about its central (focal axis)
        :param angle: spin angle
        :return: None
        """
        q = self.get_rot()
        focal_origin = mathU.Vector([0, 0, -1])
        T = q.to_matrix()
        focal_axis = T * focal_origin
        focal_axis.normalize()
        self.rotate(angle, *focal_axis)

    def blender_create_operation(self, location):
        bpy.ops.object.camera_add(location=location)

    def face_towards(self, x, y, z):
        """
        This function commands the camera central axis to rotate and intersect the coordinates (x,y,z).
        Algorithm:
            - Align camera central axis (focal axis) with -z direction (0,0,-1) - this is its original configuration
            - Calculate target vector w.r.t camera origin: target = (x,y,z) - (x0,y0,z0)
            - Normalize target vector and rotational origin
            - Get rotational axis and angle : cross(rot_origin, target), dot(rot_origin, target)

        Warning: given a current camera location (x0,y0,z0) when asked to rotate towards (x,y,z) the resulting spin
        of the camera w.r.t world coordinate axes is always the same. This is because we always start from the same
        rotational origin. To randomize the spin angle, use spin()

        :param x: x coordinate of target
        :param y: y coordinate of target
        :param z: z coordinate of target
        :return: None
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




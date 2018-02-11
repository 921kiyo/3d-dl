import bpy
import math
import random
import mathutils as mathU
import itertools

from BlenderObjects import *
from BlenderShapes import *

class BlenderRoom(object):
    def __init__(self, radius):
        self.walls = []
        self.walls.append(
            BlenderPlane(location=(-radius, 0, 0), scale=(radius, radius, radius), orientation=(90, 0, 1, 0)))
        self.walls.append(
            BlenderPlane(location=(0, radius, 0), scale=(radius, radius, radius), orientation=(90, 1, 0, 0)))
        self.walls.append(BlenderPlane(location=(0, 0, -radius), scale=(radius, radius, radius)))
        self.walls.append(
            BlenderPlane(location=(radius, 0, 0), scale=(radius, radius, radius), orientation=(90, 0, 1, 0)))
        self.walls.append(
            BlenderPlane(location=(0, -radius, 0), scale=(radius, radius, radius), orientation=(90, 1, 0, 0)))
        self.walls.append(BlenderPlane(location=(0, 0, radius), scale=(radius, radius, radius)))


    def delete(self):
        for wall in self.walls:
            wall.delete()
        self.walls = []  # drop deleted references


class BlenderScene(object):
    def __init__(self, data):
        self.lamp = None
        self.background = None
        self.objects_fixed = []
        self.objects_unfixed = []
        self.camera = None
        self.subject = None
        self.data = data

    def add_background(self, background):
        self.background = background

    def add_camera(self, camera):
        self.camera = camera

    def add_subject(self, subject):
        self.subject = subject

    def add_object_fixed(self, object):
        self.objects_fixed.append(object)

    def add_object_unfixed(self, object):
        self.objects_unfixed.append(object)

    def add_lamp(self, lamp):
        self.lamp = lamp

    def delete_all(self):
        for obj in self.objects_fixed:
            obj.delete()
        for obj in self.objects_unfixed:
            obj.delete()
        self.subject.delete()
        self.objects_fixed = []
        self.objects_unfixed = []

    def set_render(self):
        self.data.cycles.film_transparent = True
        self.data.cycles.max_bounces = 3
        self.data.cycles.min_bounces = 1
        self.data.cycles.transparent_max_bounces = 3
        self.data.cycles.transparent_min_bounces = 1
        self.data.cycles.samples = 64
        self.data.cycles.device = 'GPU'
        self.data.render.tile_x = 512
        self.data.render.tile_y = 512
        self.data.render.resolution_x = 300
        self.data.render.resolution_y = 300
        self.data.render.resolution_percentage = 100

    def render_to_file(self, filepath):
        self.data.render.filepath = filepath
        bpy.ops.render.render(write_still=True)





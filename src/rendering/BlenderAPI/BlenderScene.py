import bpy
import math
import rendering.RandomLib
import mathutils as mathU
import itertools

from rendering.BlenderAPI.BlenderObjects import *
from rendering.BlenderAPI.BlenderShapes import *
from rendering.BlenderAPI.BlenderLamps import BlenderPoint
import rendering.RandomLib.random_render as rnd


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
        self.lamps = []
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
        self.lamps.append(lamp)

    def delete_all(self):
        for obj in self.objects_fixed:
            obj.delete()
        for obj in self.objects_unfixed:
            obj.delete()
        if self.subject is not None:
            self.subject.delete()
            self.subject = None
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

    def remove_subject(self):
        if self.subject is not None:
            self.subject.delete()

    def remove_lamps(self):
        for lamp in self.lamps:
            lamp.delete()

class BlenderRandomScene(BlenderScene):
    def __init__(self, data):
        super(BlenderRandomScene, self).__init__(data)
        self.params = {}
        '''light params'''
        self.params['num_lights']       = {'dist': 'uniform_d', 'l': 1, 'r': 4}
        self.params['light_dist']       = {'dist': 'trunc_norm', 'mu':5.0, 'sigmu': 1.0, 'l': 0.0, 'r': None}
        self.params['light_energy']     = {'dist': 'trunc_norm', 'mu': 0.0, 'sigmu': 0.0, 'l': 0.0, 'r': None}
        '''camera params'''
        self.params['camera_radius']    = {'dist': 'trunc_norm', 'mu': 6.0, 'sigmu': 0.0, 'l': 0.0, 'r': None}
        self.params['spin_angle']       = {'dist': 'uniform_c', 'l':0.0, 'r':360.0}
        self.params['camera_phi_sigma'] = {'dist': 'constant', 'k': 30.0}
        self.params['subject_size']     = {'dist': 'trunc_norm', 'mu':8.0, 'sigmu': 0.0, 'l':0.0, 'r': None}

    def set_num_lights(self, N):
        self.num_lights = N
        self.remove_lamps()
        for i in range(self.num_lights):
            self.add_lamp(BlenderPoint(None))

    def load_subject_from_path(self, obj_path, texture_path):
        self.remove_subject()
        self.add_subject(BlenderImportedShape(obj_path=obj_path, location=(-1,0,-1) ,orientation=(180,0,1,0)))
        self.subject.set_mesh_bbvol(self.params['subject_size']['mu'])  # size of original cube
        self.subject.add_image_texture(texture_path)
        # texture appearance are fixe for now
        self.subject.set_diffuse(color=(1, 0, 0, 1), rough=0.1)
        self.subject.set_gloss(rough=0.1)
        self.subject.set_mixer(0.3)
        self.subject.set_location(0., 0., 0.)

    def sample_param_trunc_norm(self, params):
        return rnd.sample_trunc_norm(params['mu'], params['sigma'], params['l'], params['r'])

    def sample_param_uniformc(self, params):
        return rnd.uniform(params['l'], params['r'])

    def sample_param_uniformd(self, params):
        return rnd.randint(params['l'], params['r'])

    def sample_param_norm(self, params):
        return random.gauss(params['mu'], params['sigma'])






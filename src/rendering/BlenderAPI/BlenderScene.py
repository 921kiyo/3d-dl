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
        self.data.render.tile_x = 128
        self.data.render.tile_y = 128
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
        self.lamps = []

class BlenderRandomScene(BlenderScene):
    """
    Subclass of blender scene. Controls random variables associated with
    rendering by assigning it a distribution instead of a fixed constant
    value. When rendering, it samples from this distribution to generate
    the scene.

    There are methods to change these distributions on the fly, as well
    as change the distribution parameters, namely the set_attribute_distribution
    and set_attribute_distribution_params method.
    """
    def __init__(self, data):
        """
        Initialization method. Here are listed all the default distributions
        for each variable. Note that there may be incompatible variable -
        distribution combos, since some distributions are specified over
        vectors.
        :param data: bpy scene data structure
        """
        super(BlenderRandomScene, self).__init__(data)
        '''light params'''
        self.num_lamps     = rnd.UniformDDist(l=1,r=3)
        self.lamp_loc      = rnd.UniformShellCoordinateDist()
        self.lamp_distance = rnd.TruncNormDist(mu=5.0,sigmu=0.3,l=0.0,r=None)
        self.lamp_energy   = rnd.TruncNormDist(mu=5000.,sigmu=0.3,l=0.0,r=None)
        self.lamp_size     = rnd.TruncNormDist(mu=5., sigmu=0.3, l=0.0, r=None)
        '''camera params'''
        self.camera_loc     = rnd.CompositeShellRingDist(phi_sigma=10.0,normals='YZ')
        self.camera_radius  = rnd.TruncNormDist(mu=6.0,sigmu=0.3,l=0.0,r=None)
        self.spin_angle     = rnd.UniformCDist(l=0.0,r=360.0)
        '''mesh params'''
        self.subject_size   = rnd.NormDist(mu=8.0,sigma=0.0)

        self.max_num_lamps = 0
        self.set_num_lamps(self.num_lamps.r)

    def set_num_lamps(self, N):
        if N == self.max_num_lamps:
            return
        self.max_num_lamps = N
        self.remove_lamps()
        for i in range(self.max_num_lamps):
            self.add_lamp(BlenderPoint(None))

    def load_subject_from_path(self, obj_path, texture_path):
        self.remove_subject()
        self.add_subject(BlenderImportedShape(obj_path=obj_path, location=(-1,0,-1) ,orientation=(90,1,0,0)))
        self.subject.set_mesh_bbvol(self.subject_size.sample_param())  # size of original cube
        self.subject.add_image_texture(texture_path)
        # texture appearance are fixed for now
        self.subject.set_diffuse(color=(1, 0, 0, 1), rough=0.1)
        self.subject.set_gloss(rough=0.1)
        self.subject.set_mixer(0.3)
        self.subject.set_location(0., 0., 0.)

    def set_attribute_distribution(self, attr, params):
        """

        Sets the distribution of attribute specified by attr. params is
        a dictionary containig the following:

        - 'dist': str ( this gives the distribution name which will go
        into a lookup table in random_render.DIstributionFactory, and will
        return a distribution object identified by the name. Look in
        RandomLib.random_render.py for a full list)
        - everything else will be a dict of kwargs that the constructor for
        the specified distribution expects.

        For instance, to assign a uniform distribution to lamp_energy with
        lower bound 500.0 and upper bound 1000.0. Since the constructor for
        UniformCDist is: "def __init__(self, l=None, r=None, **kwargs)", and
        DistributionFactory maps "UniformD" to that distribution, we should
        specify param as:
        {'dist':'UniformD', 'l':500.0, 'r':1000.0}

        :param attr: attribute name
        :param params: required params to specify distribution
        :return: None
        """
        self_dict = vars(self)
        if attr not in self_dict.keys():
            raise KeyError('Cannot find specified attribute!')
        self_dict[attr] = rnd.DistributionFactory(**params)

    def set_attribute_distribution_params(self, attr, param, val):
        """
        Sets the parameter of the distribution of an attribute attr.
        param has to exist in the distribution that is is associated with
        attr. For instance, if attr is assigned a UniformCDist, and
        is asked to change the param "mu", this will throw a KeyError.

        :param attr: Attribute name to change
        :param param: Parameter name to change
        :param val: Value to set parameter to
        :return: None
        """
        self_dict = vars(self)
        if attr not in self_dict.keys():
            raise KeyError('Cannot find specified attribute!')
        dist_dict = vars(self_dict[attr])
        if param not in dist_dict.keys():
            raise KeyError('Cannot find specified attribute!')
        dist_dict[param] = val

    def random_lighting_conditions(self, blender_lamp):
        '''location'''
        (x,y,z) = self.lamp_loc.sample_param()
        r = self.lamp_distance.sample_param()
        loc = (r*x, r*y, r*z)
        blender_lamp.set_location(*loc)
        '''energy'''
        brightness = self.lamp_energy.sample_param()
        blender_lamp.set_brightness(brightness)
        size = self.lamp_size.sample_param()
        blender_lamp.set_size(size)

    def scene_setup(self):
        """
        To be run before every render. This method performs sampling of all
        render parameters, and sets the scene up.
        :return: None
        """
        # **********************  LIGHTS **********************
        # turn everything off
        for lamp in self.lamps:
            lamp.turn_off()

        # set random lighting conditions
        self.set_num_lamps(self.num_lamps.r)
        num_active_lamps = self.num_lamps.sample_param()
        for l in range(num_active_lamps):
            lamp = self.lamps[l]
            lamp.turn_on()
            self.random_lighting_conditions(lamp)

        # **********************  CAMERA **********************
        # random location of camera along shell coordinates
        (x, y, z) = self.camera_loc.sample_param()
        r = self.camera_radius.sample_param()
        loc = (r*x, r*y, r*z)
        self.camera.set_location(*loc)
        # face towards the centre
        self.camera.face_towards(0.0, 0.0, 0.0)

        # randomize spin of camera
        spin_angle = self.spin_angle.sample_param()
        self.camera.spin(spin_angle)

        # ********************* SUBJECT **********************
        self.subject.set_mesh_bbvol(self.subject_size.sample_param())  # size of original cube

    def render_to_file(self, filepath):
        """Overrides parent class implementation"""
        self.scene_setup()
        self.data.render.filepath = filepath
        bpy.ops.render.render(write_still=True)

    def clear_logs(self):
        """
        Clears the logs of all sampled parameters
        :return: None
        """
        self_dict = vars(self)
        for attr_name in self_dict.keys():
            attr = self_dict[attr_name]
            if hasattr(attr, 'sample_param'):
                attr.clear_log()

    def retrieve_logs(self, clear=True):
        """
        Returns a dictionary of logs of every parameter
        :param clear: True to clear logs as soon as retrieved, False to keep
        :return: dictionary of logs
        """
        logs = {}
        self_dict = vars(self)

        for attr_name in self_dict.keys():
            attr = self_dict[attr_name]
            if hasattr(attr, 'sample_param'):
                logs[attr_name] = attr.log

        if clear:
            self.clear_logs()

        return logs

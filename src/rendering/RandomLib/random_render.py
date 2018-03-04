"""
metballs!
"""

import numpy as np
import random
import math

def random_color():
    """
    utility function for random color, returns a 3-tuple, each element in [0,1]
    :return: 3-tuple representing a color
    """
    return random.random(), random.random(), random.random()

def random_shell_coords(radius):
    """
    given a shell radius, return a random shell coordinate centred around (0,0,0)
    :param radius: radius of shell
    :return: 3-tuple shell coordinate
    """
    
    if(radius<0):
        raise ValueError("Cannot have negative radius")
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
    if(sigma<0 or lim<0):
        raise ValueError("Cannot have negative sigma and cube width lim")
    
    x = min(random.gauss(mux, sigma), lim)
    y = min(random.gauss(muy, sigma), lim)
    z = min(random.gauss(muz, sigma), lim)
    return x, y, z

def sample_trunc_norm(mu, sigma, a = None , b = None):
    if sigma < 0:
        raise ValueError("Cannot have negative variance!")
    x = None
    while((x is None) or ((x < a) and (a is not None)) or ((x > b) and (b is not None))):
        x = random.gauss(mu, sigma)
    return x

def random_shell_coords_cons(radius, phi_sigma):

    if (radius < 0 or phi_sigma < 0):
        raise ValueError("Cannot have negative radius or sigma values!")

    theta = math.radians(random.uniform(0.0, 360.0))
    phi = math.radians(sample_trunc_norm(90.0, phi_sigma, 0.0, 180.0))
    x = radius * np.cos(theta) * np.sin(phi)
    y = radius * np.sin(theta) * np.sin(phi)
    z = radius * np.cos(phi)
    return x, y, z

def random_lighting_conditions(blender_lamp, reference_location=(0.0, 0.0, 0.0), location_variance=1.0):
    """
    choose a random coordinate to face
    choose a random brightness and size
    both according to a gaussian distribution with mean (0,0,0), default brightness and size
    and variance being 30% of mean (negative values of brightness and size will be evaluated
    to zero)
    """
    loc = random_cartesian_coords(*reference_location, location_variance, 6.0)
    blender_lamp.face_towards(*loc)
    brightness = sample_trunc_norm(blender_lamp.default_brightness, 0.3 * blender_lamp.default_brightness, 0.0, None)
    blender_lamp.set_brightness(brightness)
    blender_lamp.set_size(random.gauss(blender_lamp.default_size, 0.3 * blender_lamp.default_size))

def check_required_kwargs(kwarg_dict, kw_list):
    for kw in kw_list:
        if not kw in kwarg_dict.keys():
            raise KeyError()

class Distribution(object):
    def __init__(self, **kwargs):
        self.params = kwargs

    def sample_param(self):
        return NotImplementedError

class TruncNormDist(Distribution):
    def __init__(self, **kwargs):
        check_required_kwargs(kwargs, ['mu','sigmu','l','r'])
        super(TruncNormDist, self).__init__(**kwargs)

    def sample_param(self):
        return sample_trunc_norm(self.params['mu'], self.params['sigmu']*self.params['mu'], self.params['l'], self.params['r'])

class NormDist(Distribution):
    def __init__(self, **kwargs):
        check_required_kwargs(kwargs, ['mu','sigma'])
        super(NormDist, self).__init__(**kwargs)

    def sample_param(self):
        return random.gauss(self.params['mu'], self.params['sigma'])

class UniformCDist(Distribution):
    def __init__(self, **kwargs):
        check_required_kwargs(kwargs, ['l','r'])
        super(UniformCDist, self).__init__(**kwargs)

    def sample_param(self):
        return random.uniform(self.params['l'], self.params['r'])

class UniformDDist(Distribution):
    def __init__(self, **kwargs):
        check_required_kwargs(kwargs, ['l','r'])
        super(UniformDDist, self).__init__(**kwargs)

    def sample_param(self):
        return random.randint(self.params['l'], self.params['r'])

class ShellRingCoordinateDist(Distribution):
    def __init__(self, **kwargs):
        check_required_kwargs(kwargs, ['phi_sigma', 'normal'])
        super(ShellRingCoordinateDist, self).__init__(**kwargs)
        if self.params['normal'] not in ['X','Y','Z']:
            raise ValueError('Normal must be one of X, Y , or Z!')
        self.theta = UniformCDist(l=0.0, r=360.0)
        self.phi = TruncNormDist(mu=90.0,sigmu=self.params['phi_sigma']/90.0,l=0.0,r=180.0)

    def sample_param(self):

        theta = math.radians(self.theta.sample_param())
        phi = math.radians(self.phi.sample_param())

        x = np.cos(theta) * np.sin(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(phi)

        if self.params['normal'] == 'X':
            coords = (-z, y, x)
        elif self.params['normal'] == 'Y':
            coords = (x, z, -y)
        elif self.params['normal'] == 'Z':
            coords = (x, y, z)

        return coords

class CompositeShellRingDist(Distribution):
    def __init__(self, **kwargs):
        check_required_kwargs(kwargs, ['phi_sigma', 'normals'])
        super(CompositeShellRingDist, self).__init__(**kwargs)
        if self.params['normals'] not in ['X','Y','Z','XY','XZ','YZ','XYZ']:
            raise ValueError('Normal must be one of ["X","Y","Z","XY","XZ","YZ","XYZ"]!')
        self.distributions = []
        for normal in self.params['normals']:
            self.distributions.append(ShellRingCoordinateDist(phi_sigma=self.params['phi_sigma'], normal=normal))
        self.distribution_select = UniformDDist(l=0,r=len(self.distributions)-1)

    def sample_param(self):
        selection = self.distribution_select.sample_param()
        selected_distribution = self.distributions[selection]
        return selected_distribution.sample_param()


class UniformShellCoordinateDist(Distribution):
    def __init__(self, **kwargs):
        self.theta = UniformCDist(l=0.0, r=360.0)
        self.phi = TruncNormDist(mu=90.0,sigmu=30.0/90.0,l=0.0,r=180.0)
        super(UniformShellCoordinateDist, self).__init__(**kwargs)

    def sample_param(self):

        theta = math.radians(self.theta.sample_param())
        phi = math.radians(self.phi.sample_param())

        x = np.cos(theta) * np.sin(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(phi)

        return (x,y,z)


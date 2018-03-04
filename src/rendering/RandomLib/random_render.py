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
    x = None
    while((x is None) or ((a is not None) and (x < a)) or ((b is not None) and (x > b))):
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

def check_required_kwargs(kwarg_dict, kw_list):
    for kw in kw_list:
        if not kw in kwarg_dict.keys():
            raise KeyError()

class Distribution(object):
    def __init__(self, **kwargs):
        self.log = []
        pass

    def sample_param(self):
        return NotImplementedError

    def log_param(self, val):
        self.log.append(val)

    def clear_log(self):
        self.log = []

class TruncNormDist(Distribution):
    def __init__(self, mu=None, sigmu=None, l=None, r=None, **kwargs):
        self.mu = mu
        self.sigmu= sigmu
        self.l = l
        self.r = r
        super(TruncNormDist, self).__init__(**kwargs)

    def sample_param(self):
        y = sample_trunc_norm(self.mu, self.sigmu*self.mu, self.l, self.r)
        self.log_param(y)
        return y

class NormDist(Distribution):
    def __init__(self, mu=None, sigma=None, **kwargs):
        self.mu = mu
        self.sigma = sigma
        super(NormDist, self).__init__(**kwargs)

    def sample_param(self):
        y = random.gauss(self.mu, self.sigma)
        self.log_param(y)
        return y

class UniformCDist(Distribution):
    def __init__(self, l=None, r=None, **kwargs):
        self.l = l
        self.r = r
        if self.l > self.r:
            raise ValueError('Lower bound greater than upper bound!')
        super(UniformCDist, self).__init__(**kwargs)

    def sample_param(self):
        y = random.uniform(self.l, self.r)
        self.log_param(y)
        return y

class UniformDDist(Distribution):
    def __init__(self, l=None, r=None, **kwargs):
        self.l = l
        self.r = r
        if self.l > self.r:
            raise ValueError('Lower bound greater than upper bound!')
        super(UniformDDist, self).__init__(**kwargs)

    def sample_param(self):
        y = random.randint(self.l, self.r)
        self.log_param(y)
        return y

class ShellRingCoordinateDist(Distribution):
    def __init__(self, phi_sigma = None, normal = None, **kwargs):
        self.normal = normal
        self.phi_sigma = phi_sigma
        super(ShellRingCoordinateDist, self).__init__(**kwargs)
        if self.normal not in ['X','Y','Z']:
            raise ValueError('Normal must be one of X, Y , or Z!')
        self.theta = UniformCDist(l=0.0, r=360.0)
        self.phi = TruncNormDist(mu=90.0,sigmu=self.phi_sigma/90.0,l=0.0,r=180.0)

    def sample_param(self):

        theta = math.radians(self.theta.sample_param())
        phi = math.radians(self.phi.sample_param())

        x = np.cos(theta) * np.sin(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(phi)

        if self.normal == 'X':
            coords = (-z, y, x)
        elif self.normal == 'Y':
            coords = (x, z, -y)
        elif self.normal == 'Z':
            coords = (x, y, z)

        self.log_param(coords)

        return coords

class CompositeShellRingDist(Distribution):
    def __init__(self, phi_sigma = None, normals = None, **kwargs):
        self.phi_sigma = phi_sigma
        self.normals = normals
        super(CompositeShellRingDist, self).__init__(**kwargs)
        if self.normals not in ['X','Y','Z','XY','XZ','YZ','XYZ']:
            raise ValueError('Normals must be one of ["X","Y","Z","XY","XZ","YZ","XYZ"]!')
        self.distributions = []
        for normal in self.normals:
            self.distributions.append(ShellRingCoordinateDist(phi_sigma=self.phi_sigma, normal=normal))
        self.distribution_select = UniformDDist(l=0,r=len(self.distributions)-1)

    def sample_param(self):
        selection = self.distribution_select.sample_param()
        selected_distribution = self.distributions[selection]
        coords = selected_distribution.sample_param()
        self.log_param(coords)
        return coords


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
        coords = (x,y,z)
        self.log_param(coords)
        return coords

def DistributionFactory(**params):
    check_required_kwargs(params, ['dist'])
    return {
        'TruncNorm': TruncNormDist(**params),
        'Norm': TruncNormDist(**params),
        'UniformC': UniformCDist(**params),
        'UniformD': UniformDDist(**params),
        'ShellRingCoordinate': ShellRingCoordinateDist(**params),
        'CompositeShellRing': CompositeShellRingDist(**params),
        'UniformShellCoordinate': UniformShellCoordinateDist(**params)
    }[params['dist']]

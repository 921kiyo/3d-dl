"""
Contains the means to sample from various trivial and non trivial distributions
An abstract parent class Distribution defines the interface, while each of
its child classes define the logic, pased on the desired distribution.
"""

import numpy as np
import random
import math
from .random_exceptions import ImprobableError

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

def sample_trunc_norm(mu, sigma, a = None , b = None, tol=1e06):
    """
    Sample from a truncated normal distribution. The distribution of x is
    normal conditional on a<=x<=b. a = None means a = -inf, b = None means
    b = inf
    :param mu: mean of the normal
    :param sigma: standard deviation of the normal
    :param a: lower bound, None means -infinity
    :param b: upper bound, None means infinity
    :return: x, a sample
    """
    x = None
    if not(a is None or b is None) and a > b:
        raise ValueError('Lower bound greater than upper bound!')
    count = 0
    while((x is None) or ((a is not None) and (x < a)) or ((b is not None) and (x > b))):
        if count > tol:
            raise ImprobableError('rejected samples has exceeded {}!'.format(tol))
        x = random.gauss(mu, sigma)
        count += 1
    return x

def random_shell_coords_cons(radius, phi_sigma):
    """
    Returns a cartesian coordinates of a point on the surface of sphere defined 
    by radius (given), theta angle (drawn from uniform distribution 
    0° to 360°) and sigma which is drawn from trunctated normal distribution 
    centered at 90° with sigma of the distribution given.
    :param radius: radius of the sphere
    :param phi_sigma: standard devitaion of the phi distribution
    :return: (x,y,z) cartesian coordinates of random point on the surface of 
            a sphere
    """

    if (radius < 0 or phi_sigma < 0):
        raise ValueError("Cannot have negative radius or sigma values!")

    theta = math.radians(random.uniform(0.0, 360.0))
    phi = math.radians(sample_trunc_norm(90.0, phi_sigma, 0.0, 180.0))
    x = radius * np.cos(theta) * np.sin(phi)
    y = radius * np.sin(theta) * np.sin(phi)
    z = radius * np.cos(phi)
    return x, y, z

def check_required_kwargs(kwarg_dict, kw_list):
    """
    Checks that any argument given in kw_list has an corresponding entry
    in the kwarg_dict
    :param kwarg_dict: Dictionary which entries are the only allowed values
    :param kw_list: A list of arguments to check
    :return void: If problem, raise KeyError(), otherwise return void
    """
    for kw in kw_list:
        if not kw in kwarg_dict.keys():
            raise KeyError()

class Distribution(object):
    """
    Base class for distribution classes. This provides a required interface:
    A sample_param() must be provided based on the sampling algorithm of the
    distribution. log_param can be called to log sampled values.
    """
    def __init__(self, **kwargs):
        self.log = []
        pass

    def sample_param(self):
        return NotImplementedError

    def log_param(self, val):
        self.log.append(val)

    def clear_log(self):
        self.log = []

    def give_param(self):
        return NotImplementedError

    def change_param(self):
        return NotImplementedError

class TruncNormDist(Distribution):
    """
    The class represents the Truncated Normal distribution. The distribution of
    x is normal conditional on a<=x<=b. a = None means a = -inf, b = None means
    b = inf
    """
    def __init__(self, mu, sigmu, l=None, r=None, **kwargs):
        """
        :param mu: Mean of truncated normal
        :param sigmu: Ratio of standard deviation over mean
        :param l: lower bound of distribution l=None means l=-Inf
        :param r: upper bound of distribution r=None means r=Inf
        :param kwargs: other kwargs to be passed on to parent class
        """
        self.mu = mu
        self.sigmu= sigmu
        self.l = l
        self.r = r

        if not(self.l is None or self.r is None) and (self.l > self.r):
            raise ValueError('Lower bound greater than upper bound!')
        if mu < 0:
            raise ValueError('TruncNormDist accepts only non-negative means!')
        if sigmu < 0:
            raise ValueError('TruncNormDist accepts only non-negative sigmus!')
        super(TruncNormDist, self).__init__(**kwargs)


    def give_param(self):
        return {"dist": "TruncNormDist", "mu": self.mu, "sigmu": self.sigmu, "l": self.l, "r": self.r}
        
    def sample_param(self):
        """
        Implementation of abstract method sample_param
        :return: sample from this specified distribution
        """
        y = sample_trunc_norm(self.mu, self.sigmu*self.mu, self.l, self.r)
        self.log_param(y)
        return y
    
    def change_param(self, param_name, param_val):
        """
        Function to update the value of a parameter.
        :param param_name: name of parameter to be updated
        :param param_val: value to be updated
        :return void: If invalid input, raises Error.
        """
        self_dict = vars(self)
        if param_name not in self_dict.keys():
            raise KeyError('Cannot find specified attribute!')
        if param_name=='mu' and param_val<0:
            raise ValueError('TruncNormDist accepts only non-negative means!')
        if param_name=='sigmu' and param_val<0:
            raise ValueError('TruncNormDist accepts only non-negative sigmus!')
        self_dict[param_name] = param_val
        

class NormDist(Distribution):
    """
    Regular normal distribution
    """
    def __init__(self, mu, sigma, **kwargs):
        """
        :param mu: mean
        :param sigma: standard deviation
        :param kwargs: other kwargs to be passed on to parent class
        """
        if sigma < 0:
            raise ValueError('NormDist accepts only non-negative sigmas!')
        self.mu = mu
        self.sigma = sigma
        super(NormDist, self).__init__(**kwargs)

    def sample_param(self):
        """
        Implementation of abstract method sample_param
        :return: sample from this specified distribution
        """
        y = random.gauss(self.mu, self.sigma)
        self.log_param(y)
        return y

    def give_param(self):
        return {"dist": "NormDist","mu": self.mu, "sigma": self.sigma}

    def change_param(self, param_name, param_val):
        """
        Function to update the value of a parameter.
        :param param_name: name of parameter to be updated
        :param param_val: value to be updated
        :return void: If invalid input, raises Error.
        """
        self_dict = vars(self)
        if param_name not in self_dict.keys():
            raise KeyError('Cannot find specified attribute!')
        if param_name=='sigma' and param_val<0:
            raise ValueError('NormDist accepts only non-negative sigmas!')

        self_dict[param_name] = param_val
        

class UniformCDist(Distribution):
    """
    Continuous uniform distribution on an interval
    """
    def __init__(self, l, r, **kwargs):
        """
        :param l: Lower bound of distribution
        :param r: Upper bound of distribution
        :param kwargs: other kwargs to be passed on to parent class
        """
        self.l = l
        self.r = r
        if self.l > self.r:
            raise ValueError('Lower bound greater than upper bound!')
        super(UniformCDist, self).__init__(**kwargs)

    def sample_param(self):
        """
        Implementation of abstract method sample_param
        :return: sample from this specified distribution
        """
        if self.l > self.r:
            raise ValueError('Lower bound greater than upper bound!')
        y = random.uniform(self.l, self.r)
        self.log_param(y)
        return y

    def give_param(self):
        return {"dist": "UniformCDist", "l": self.l, "r": self.r}

    def change_param(self, param_name, param_val):
        """
        Function to update the value of a parameter.
        :param param_name: name of parameter to be updated
        :param param_val: value to be updated
        :return void: If invalid input, raises Error.
        """
        self_dict = vars(self)
        if param_name not in self_dict.keys():
            raise KeyError('Cannot find specified attribute!')
        self_dict[param_name] = param_val

class UniformDDist(Distribution):
    """
    Uniform discrete distribution on the interval of integers
    """
    def __init__(self, l, r, **kwargs):
        """
        :param l: Lower bound of distribution
        :param r: Upper bound of distribution
        :param kwargs: other kwargs to be passed on to parent class
        """
        self.l = l
        self.r = r
        if self.l > self.r:
            raise ValueError('Lower bound greater than upper bound!')
        super(UniformDDist, self).__init__(**kwargs)

    def sample_param(self):
        """
        Implementation of abstract method sample_param
        :return: sample from this specified distribution
        """
        if self.l > self.r:
            raise ValueError('Lower bound greater than upper bound!')
        y = random.randint(self.l, self.r)
        self.log_param(y)
        return y

    def give_param(self):
        return {"dist": "UniformDDist", "l": self.l, "r": self.r}

    def change_param(self, param_name, param_val):
        """
        Function to update the value of a parameter.
        :param param_name: name of parameter to be updated
        :param param_val: value to be updated
        :return void: If invalid input, raises Error.
        """        
        self_dict = vars(self)
        if param_name not in self_dict.keys():
            raise KeyError('Cannot find specified attribute!')
        self_dict[param_name] = param_val

class PScaledUniformDDist(Distribution):
    """
    Uniform discrete distribution on the natural numbers (non-negative integers),
    specifiable by a midpoint and a scaled range of the midpoint
    """
    def __init__(self, mid, scale, **kwargs):
        """
        :param mid: midpoint of the distribution
        :param scale: proportion of the midpoint to be used as half-range
        :param kwargs: bla
        """
        if scale > 1.0 or scale < 0.0:
            raise ValueError('Scale not in [0,1]')
        if mid < 0.0:
            raise ValueError('Midpoint negative!')
        self.mid = mid
        self.scale = scale
        self.l = int(np.round(mid - (mid * scale)))
        self.r = int(np.round(mid + (mid * scale)))
        super(PScaledUniformDDist, self).__init__(**kwargs)

    def sample_param(self):
        """
        Implementation of abstract method sample_param
        :return: sample from this specified distribution
        """
        if self.l > self.r:
            raise ValueError('Lower bound greater than upper bound!')
        y = random.randint(np.round(self.l), np.round(self.r))
        self.log_param(y)
        return y

    def give_param(self):
        return {"dist": "PScaledUniformDDist", "mid": self.mid, "scale": self.scale}

    def change_param(self, param_name, param_val):
        """
        Function to update the value of a parameter. It also update
        any parameter dependend on the changed parameter
        :param param_name: name of parameter to be updated
        :param param_val: value to be updated
        :return void: If invalid input, raises Error.
        """        
        self_dict = vars(self)

        if param_name=='scale':
            if param_val > 1.0 or param_val < 0.0:
                raise ValueError('Scale greater than 1.0!')

        if param_name == 'mid':
            if param_val < 0.0:
                raise ValueError('Midpoint negative!')

        if param_name in ['scale', 'mid']:
            self_dict[param_name] = param_val
            self.l = int(np.round(self.mid - (self.mid * self.scale) ))
            self.r = int(np.round(self.mid + (self.mid * self.scale) ))
            return

        raise KeyError('Cannot find specified attribute!')


class ShellRingCoordinateDist(Distribution):
    """
    Distribution of 3-D coordinates (x,y,z). Sampling from this distribution
    will give x,y,z distributed about a  spherical ring in the plane with an
    axis normal. The width of the ring is distributed according to the parameter
    phi_sigma. Normal is one of 'X', 'Y' or 'Z'. In the limit of phi_sigma
    goes towards infinity, this will look like phi is sampled unifromly
    """
    def __init__(self, phi_sigma, normal, **kwargs):
        """
        :param phi_sigma: 'width' of spherical ring
        :param normal: 'X', 'Y' or 'Z". dictates the normal of the ring
        :param kwargs: kwargs to be passed on to parent class
        """
        self.normal = normal
        self.phi_sigma = phi_sigma
        super(ShellRingCoordinateDist, self).__init__(**kwargs)
        if self.normal not in ['X','Y','Z']:
            raise ValueError('Normal must be one of X, Y , or Z!')
        self.theta = UniformCDist(l=0.0, r=360.0)
        self.phi = TruncNormDist(mu=90.0,sigmu=self.phi_sigma/90.0,l=0.0,r=180.0)

    def sample_param(self):
        """
        Implementation of abstract method sample_param
        :return: sample from this specified distribution (a triple)
        """        
        # sample phi and theta
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

    def give_param(self):
        return {"dist": "ShellRingCoordinateDist", "phi_sigma": self.phi_sigma, "normal": self.normal}

    def change_param(self, param_name, param_val):
        """
        Function to update the value of a parameter. If other parameter
        depends on the changed one, it will update as well.
        :param param_name: name of parameter to be updated
        :param param_val: value to be updated
        :return void: If invalid input, raises Error.
        """
        self_dict = vars(self)
        if param_name=='normal':
            if param_val not in ['X','Y','Z']:
                raise ValueError('Normal must be one of X, Y , or Z!')
            self_dict[param_name] = param_val
            return
        
        if param_name=='phi_sigma':
            if param_val<0:
                raise ValueError('Phi sigma must be non-negative!')
            self.phi.change_param('sigmu', param_val/90.0)
            self_dict[param_name] = param_val
            return
        raise KeyError('Cannot find specified attribute!')

class CompositeShellRingDist(Distribution):
    """
    x,y,z here are distributed in a space of between 1 and 3 rings, will
    equal probability over the different rings. These rings can be
    specified as 'X', 'Y', 'Z', or any lexical combination of 2 or 3 of
    those, e.g. 'YZ', 'XZ' or 'XYZ'
    """
    def __init__(self, phi_sigma, normals, **kwargs):
        """
        :param phi_sigma: the same phi_sigma for every ring
        :param normals: combination of 'X', 'Y' and 'Z'
        :param kwargs: kwargs to be passed on to parent class
        """
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
        """
        Implementation of abstract method sample_param
        :return: sample from this specified distribution (a triple)
        """
        selection = self.distribution_select.sample_param()
        selected_distribution = self.distributions[selection]
        coords = selected_distribution.sample_param()
        self.log_param(coords)
        return coords

    def give_param(self):
        return {"dist": "CompositeShellRingDist", "phi_sigma": self.phi_sigma, "normals": self.normals}

    def change_param(self, param_name, param_val):
        """
        Function to update the value of a parameter. It also changes
        any dependent parameter in any of the associated distributions.
        :param param_name: name of parameter to be updated
        :param param_val: value to be updated
        :return void: If invalid input, raises Error.
        """

        if param_name=='phi_sigma':
            self.phi_sigma = param_val
            for distribution in self.distributions:
                distribution.change_param('phi_sigma', param_val)
            return

        if param_name=='normals':
            self.normals = param_val
            if self.normals not in ['X','Y','Z','XY','XZ','YZ','XYZ']:
                raise ValueError('Normals must be one of ["X","Y","Z","XY","XZ","YZ","XYZ"]!')
            self.distributions = []
            for normal in self.normals:
                self.distributions.append(ShellRingCoordinateDist(phi_sigma=self.phi_sigma, normal=normal))
            self.distribution_select = UniformDDist(l=0,r=len(self.distributions)-1)
            return

        raise KeyError('Cannot find specified attribute!')


class UniformShellCoordinateDist(Distribution):
    """
    (x,y,z) is distributed according to a uniform shell distribution. This
    is different from specifying phi to come from a uniform dist. A sigma of
    about 30.0 gives an approxiamtely radially uniform distribution about
    the sphere
    """
    def __init__(self, **kwargs):
        """
        :param kwargs: kwargs to be passed on to parent class
        """
        self.theta = UniformCDist(l=0.0, r=360.0)
        self.phi = TruncNormDist(mu=90.0,sigmu=30.0/90.0,l=0.0,r=180.0)
        super(UniformShellCoordinateDist, self).__init__(**kwargs)
        
    def sample_param(self):
        """
        Implementation of abstract method sample_param
        :return: sample from this specified distribution (a triple)
        """
        theta = math.radians(self.theta.sample_param())
        phi = math.radians(self.phi.sample_param())

        x = np.cos(theta) * np.sin(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(phi)
        coords = (x,y,z)
        self.log_param(coords)
        return coords
    
    def give_param(self):
        return {"dist": "UniformShellCoordinateDist"}

def DistributionFactory(**params):
    check_required_kwargs(params, ['dist'])
    return {
        'TruncNorm': TruncNormDist,
        'Norm': TruncNormDist,
        'UniformC': UniformCDist,
        'UniformD': UniformDDist,
        'PScaledUniformDDist': PScaledUniformDDist,
        'ShellRingCoordinate': ShellRingCoordinateDist,
        'CompositeShellRing': CompositeShellRingDist,
        'UniformShellCoordinate': UniformShellCoordinateDist,
    }[params['dist']](**params)

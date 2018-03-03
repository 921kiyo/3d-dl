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
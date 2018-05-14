"""
Logic to generate random colour mesh background using Metaballs.
Using several layers of metaballs and random colour canvas, a final mesh 
is created where random overlaps of the elements create the final image
"""

import numpy as np
from scipy.interpolate import interp2d
#import matplotlib.pyplot as plt

def generate_noise(L):
    """
    Generate an array of L*L size with random values between 0 and 1
    
    Arguments:
        L (Int): One side of the array size
        
    Return:
        L*L array: Of values between 0 and 1 (exclusive 1)
    """
    return np.random.uniform(size=[L,L])


def smoothNoise(noise, scale):
    """
    Given an 2D array of random values, it creates and array of
    same size. The values of the new arrays have lower variance
    between its neighbourghs. This is done by taking a subset of the array
    of size noise.size()/scale and extrapolating it to the original size
    
    Arguments:
        noise (array of float): A 2D array of floats to be smoothened
        scale (int): non negative. An extrapolation factor.
            e.g. scale = 2 will take quarter of the original image and 
            extrapolate it to the original size
        
    Returns:
        smoothed (array of float): A 2D array of same size as noise,
                                    with lower variance between negihbourghs
    
    """

    x = np.linspace(0,scale,noise.shape[1])
    y = np.linspace(0,scale,noise.shape[0])

    noise_scaled = noise[:len(x),:len(y)]

    X = np.linspace(0,1,noise.shape[1])
    Y = np.linspace(0,1,noise.shape[0])

    N = interp2d(x,y,noise_scaled)
    smoothed = N(X,Y)

    return smoothed


def turbulence(N,D,initial_size=2):
    """
    Function that creates a 2D array of values, representing a pixel values
    of an image. This is done by creating and overlapping several noise layers.
    
    Arguments:
        N (int): The number of pixels in each dimension of the array
        D (int): The number of layers to stack on top of each other
        initial_size (int): extrapolation factor for noise smoothing.
            
    Returns:
        Turb (array of float): An N*N array of pixel values
    """
    size = initial_size
    Noise = generate_noise(N)
    Noise = smoothNoise(Noise,initial_size)
    Turb = Noise/(D)
    for i in range(1,D):
        # s += (s / 2^i) where s is the average brightness per layer
        Turb += smoothNoise(Noise,size)/(np.power(2,i))
        size *= 2

    # 2^D * (s + s/2 + s/4 + .. s/2^D) / (2^(D+1)-1) = s, recover nominal average brightness
    Turb = Turb*(np.power(2,D))/(np.power(2,D+1) - 1)
    return Turb


def turbulence_rgb(N):
    """
    Function to create a RGB random mesh image. Creates a 3D array
    of size [N,N,3], where each of the 2D N*N layers represent a single 
    colour channel. Allows a direct conversion to PIL Image format or other 
    image type variables.
    
    Argumens:
        N (int): size of each side of the 2D array.
        
    Return:
        img (array[N,N,3]): An array of floats representing an RGB image
        
    """
    min_depth = 3;
    max_depth = 8;
    img = np.zeros([N,N,3])
    for i in range(3):
        img[:,:,i] = turbulence(N,np.random.randint(min_depth,max_depth), np.random.randint(1,4))
    return img


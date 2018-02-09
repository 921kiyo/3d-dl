"""
metballs!
"""

import numpy as np
from scipy.interpolate import interp2d


def generate_noise(L):
    return np.random.uniform(size=[L,L])


def smoothNoise(noise, scale):

    x = np.linspace(0,scale,noise.shape[1])
    y = np.linspace(0,scale,noise.shape[0])

    noise_scaled = noise[:len(x),:len(y)]

    X = np.linspace(0,1,noise.shape[1])
    Y = np.linspace(0,1,noise.shape[0])

    N = interp2d(x,y,noise_scaled)
    smoothed = N(X,Y)

    return smoothed


def turbulence(N,D,initial_size=1):
    size = 2
    Noise = generate_noise(N)
    Noise = smoothNoise(Noise,initial_size)
    Turb = Noise/(D)
    for i in range(1,D):
        Turb += smoothNoise(Noise,size)/float(D-i)
        size *= 2

    Turb = Turb/D
    return Turb


def turbulence_rgb(N):
    min_depth = 3;
    max_depth = 8;
    img = np.zeros([N,N,3])
    for i in range(3):
        img[:,:,i] = turbulence(N,np.random.randint(min_depth,max_depth), np.random.randint(1,4))
    return img

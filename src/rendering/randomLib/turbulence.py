"""
metballs!
"""

import numpy as np
from scipy.interpolate import interp2d
import matplotlib.pyplot as plt

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


def turbulence(N,D,initial_size=2):
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
    min_depth = 3;
    max_depth = 8;
    img = np.zeros([N,N,3])
    for i in range(3):
        img[:,:,i] = turbulence(N,np.random.randint(min_depth,max_depth), np.random.randint(1,4))
    return img

result = turbulence_rgb(300)
plt.imshow(result)
plt.show()
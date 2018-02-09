"""
metballs!
"""

import numpy as np
from scipy.interpolate import interp2d
from scipy.misc import imresize
import turbulence
import metaballs
import matplotlib.pyplot as plt


def random_color(L):
    img = np.ones([L,L,3])
    for i in range(3):
        img[:,:,i] = np.random.uniform()*img[:,:,i]
    return img

def mix(img1, img2, size):
    mask = np.zeros([size, size, 3])
    ball_size = np.random.uniform(0.1,0.5)

    small_mask = metaballs.random_metaball(150,150,4,ball_size)
    mask[:,:,0] = imresize(small_mask,[size,size])/255.
    mask[:,:,1] = mask[:,:,0]
    mask[:,:,2] = mask[:,:,0]

    return img1*(1-mask) + img2*mask

def random_image(size):
    r = np.random.uniform()
    if r>0.5:
        return random_color(size)
    return turbulence.turbulence_rgb(size)*np.random.uniform(0,2.0)

def rand_background(N, size):
    T = random_image(size)
    for i in range(N):
        T2 = random_image(size)
        T = mix(T,T2,size)
    return T

import time

start = time.time()
for i in range(100):
    print('generated image: ', i)
    img = rand_background(np.random.randint(2,4),300)
    plt.imshow(img)
    plt.show()
end = time.time()
print('time per img = ', (end-start)/100)
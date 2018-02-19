"""
metballs!
"""


import numpy as np
from scipy.interpolate import interp2d
from scipy.misc import imresize
import turbulence 
import metaballs 
import matplotlib.pyplot as plt
from PIL import Image

def random_color(L):
    """
    Creates a L*L*3 array of random values between 0 and 1
    Arguments:
        L (int): the size of the arra
        
    Returns:
        L*L*3 array of values in range (0,1)
    """
    img = np.ones([L,L,3])
    for i in range(3):
        img[:,:,i] = np.random.uniform()*img[:,:,i]
    return img

def mix(img1, img2, size):
    mask = np.zeros([size, size, 3])
    ball_size = np.random.uniform(0.1,0.5)

    mask[:,:,0] = metaballs.random_metaball(size,size,4,ball_size)
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

#start = time.time()
def generate_background(n_of_images, ofset =0):
    for i in range(ofset, n_of_images+ofset):
        #print('generated image: ', i)
        img = rand_background(np.random.randint(2,4),300)
        scaled = img*256
        true_img = Image.fromarray(scaled.astype('uint8'), mode = "RGB")
        #true_img.save('D:\\old_files\\aaaaa\\Anglie\\imperial\\2017-2018\\group_project\\OcadoLobster\\data\\resized_background\\random_back\\background%d.png'%i)
        plt.imshow(true_img)
        plt.show()
    #end = time.time()
    #print('time per img = ', (end-start)/10)
    
generate_background(1,0)
"""
metballs!
"""

import os
import numpy as np
#from scipy.interpolate import interp2d
#from scipy.misc import imresize
import RandomLib.turbulence as turbulence
import RandomLib.metaballs as metaballs
#import matplotlib.pyplot as plt
from PIL import Image

base_path = 'D:\\old_files\\aaaaa\\Anglie\\imperial\\2017-2018\\group_project\\OcadoLobster\\data\\resized_background\\random_back\\'

def random_color(L):
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

def random_brightness(img):
    """
    randomly adjust mean brightness of an image, capping all values
    between 0 and 1
    :param img: image array
    :return: image array
    """
    brightness = np.random.uniform(0,1.0)
    img_bright = np.mean(img)
    mul = brightness/img_bright
    img *= img*mul
    img[img>1.0] = 1.0
    return img

def random_image(size):
    r = np.random.uniform()
    if r>0.5:
        return random_color(size)
    return random_brightness(turbulence.turbulence_rgb(size))

def rand_background(N, size):
    T = random_image(size)
    for i in range(N):
        T2 = random_image(size)
        T = mix(T,T2,size)
    return T

def generate_images( save_as,pixels=300, range_min=0, range_max=10,):
    for i in range(range_min, range_max):
        #print('generated image: ', i)
        img = rand_background(np.random.randint(2,4),pixels)
        scaled = img*256
        true_img = Image.fromarray(scaled.astype('uint8'), mode = "RGB")
        filename = 'background%d.png'%i
        true_img.save(os.path.join(save_as, filename))
        #plt.imshow(img)
        #plt.show()

#generate_images(base_path,300,0,2)

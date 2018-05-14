"""
Functions to create a random colour mesh backgrounds and save it 
or output in another way. Heavy use of the metaballs and turbulence library
for helper functions.
"""

import os
import numpy as np
#from scipy.interpolate import interp2d
#from scipy.misc import imresize
import rendering.RandomLib.turbulence as turbulence
import rendering.RandomLib.metaballs as metaballs
#import matplotlib.pyplot as plt
from PIL import Image

base_path = 'D:\\old_files\\aaaaa\\Anglie\\imperial\\2017-2018\\group_project\\OcadoLobster\\data\\resized_background\\random_back\\'

def random_color(L):
    """
    Creates a 3D array of [L,L,3] of single colour
    :param L: size of 2D sqaure image in pixels.
    """
    img = np.ones([L,L,3])
    for i in range(3):
        img[:,:,i] = np.random.uniform()*img[:,:,i]
    return img

def mix(img1, img2, size):
    """
    Given two images and desired size, it will merge the images together
    by masking metaball shaped parts of one image with metaball shaped sections
    of the other image.
    :param img1: 3D array[size,size,3] of pixel values
    :param img2: 3D array[size,size,3] of pixel values
    :param size: size of the input images and the output image [size, size,3]
    """
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
    """
    Returns a 3D array [size,size,3] of random colour, created either
    as a uniform colour sheet or random mesh. The decision which image to
    create is made randomly.
    :param size: size of the 2D square image in pixels
    :return: [size,size,3] array of floats, easily convertible to image format
    """
    r = np.random.uniform()
    if r>0.5:
        return random_color(size)
    return random_brightness(turbulence.turbulence_rgb(size))

def rand_background(N, size):
    """
    Function that inforporates all the above functions to create a background
    image that has random metaball variations but overall neighbour to
    neighbour variance of pixels is small.
    :param N: number of mixing stages. The higher, the more random the image
    :param size: size of the 2D square image
    :return T: a [size,size,3] array representing a complete image
    """
    T = random_image(size)
    for i in range(N):
        T2 = random_image(size)
        T = mix(T,T2,size)
    return T

def generate_images( save_as,pixels=300, range_min=0, range_max=10,):
    """
    Function for generation of multiple and images. It also allows the images
    to be saved or displayed. In case of saving the image, the images
    are named with index, which value can be adjusted. Useful to split 
    generation of many images into several smaller runs, need to be able
    to set the index so that new generations do not rewrite old.
    Total number of images generated is range_max-range_min-1.
    :param save_as: path to folder in which to save the generated images
    :param pixels: size of the square image in pixels
    :param range_min: lower index used for the naming
    :param range_max: max index used for the naming
    :return: void
    """
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

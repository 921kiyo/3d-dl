import os
import numpy as np
import matplotlib.pyplot as plt

from skimage import data, img_as_float, io
from skimage.transform import rotate

src_folder = '/vol/project/2017/530/g1753002/ong/test_images_raw/phone_cam'
dest_folder = '/vol/project/2017/530/g1753002/ong/test_images_proc/phone_cam'

def random_rot(image):
    angles = [0, 90, 180, 270]
    i = np.random.randint(0,3)
    angle = angles[i]
    return rotate(image, angle)
    

for (dirpath,_,filenames) in os.walk(src_folder):

    src_rel = os.path.relpath(dirpath, src_folder)
    dest_dir = os.path.join(dest_folder, src_rel)

    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)

    for filename in filenames:
        if filename.lower().endswith('.jpg'):
            img = io.imread(os.path.join(dirpath,filename))

            shape = np.array([np.ceil(img.shape[0]/2.), np.ceil(img.shape[1]/2.)])
            length_idx = np.argmax(shape)
            width_idx = np.argmin(shape)
            l = shape[length_idx]
            w = shape[width_idx]

            # random pert of offset
            for i in range(3):

                off_sigma = 0.5*(l-w)
                off_mean = 0
                off = np.random.normal(off_mean, off_sigma)
            
                c = (np.floor(img.shape[0]/2.), np.floor(img.shape[1]/2.))

                x0l  = int(min(max(c[length_idx] - w + off, 0), 2*(l-w)))
                x1l  = x0l + img.shape[width_idx] - 1

                x0w = 0
                x1w = img.shape[width_idx] - 1

                x0 = [0,0]
                x0[length_idx] = x0l
                x0[width_idx] = x0w
                x1 = [0,0]
                x1[length_idx] = x1l
                x1[width_idx] = x1w

                img_new = img[x0[0]:x1[0],x0[1]:x1[1]]
                img_new = random_rot(img_new)

                assert img_new.shape[0] == img_new.shape[1], "shapes {} and {} don't agree!".format(img_new.shape[0], img_new.shape[1]) 
            
                dest_filename = os.path.join(dest_dir, filename)

                base = os.path.splitext(dest_filename)[0]
                dest_filename = base + str(i) + '.jpg'
                print(dest_filename)
                
                io.imsave(dest_filename, img_new)




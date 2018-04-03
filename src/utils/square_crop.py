import os
import numpy as np
import matplotlib.pyplot as plt

from skimage import data, img_as_float, io
from skimage.restoration import denoise_nl_means, estimate_sigma
from skimage.measure import compare_psnr

src_folder = 'D:\\PycharmProjects\\test_data\\ocado_webcam'
dest_folder = 'D:\\PycharmProjects\\test_data\\ocado_webcam_test'

for (dirpath,_,filenames) in os.walk(src_folder):

    src_rel = os.path.relpath(dirpath, src_folder)
    dest_dir = os.path.join(dest_folder, src_rel)

    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)

    for filename in filenames:
        if filename.lower().endswith('.png'):
            img = io.imread(os.path.join(dirpath,filename))
            w = min(np.ceil(img.shape[0]/2.), np.ceil(img.shape[1]/2.))
            c = (np.floor(img.shape[0]/2.), np.floor(img.shape[1]/2.))
            x00 = int(np.floor(c[0]-w))
            x01 = int((c[0]+w-1))
            x10 = int(np.floor(c[1]-w))
            x11 = int((c[1]+w-1))
            img_new = img[x00:x01,x10:x11]

            dest_filename = os.path.join(dest_dir, filename)

            base = os.path.splitext(dest_filename)[0]
            dest_filename = base + '.jpg'
            print(dest_filename)

            io.imsave(dest_filename, img_new)



plt.show()
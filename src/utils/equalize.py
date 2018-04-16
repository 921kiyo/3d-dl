import os

from skimage import data, img_as_float, io
from skimage import exposure

src_folder = 'D:\\PycharmProjects\\manhattan_test_data\\warehouse_test\\Anchor'
dest_folder = 'D:\\PycharmProjects\\manhattan_test_data\\warehouse_test_adap_eq2\\Anchor'

for (dirpath,_,filenames) in os.walk(src_folder):

    src_rel = os.path.relpath(dirpath, src_folder)
    dest_dir = os.path.join(dest_folder, src_rel)

    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)

    for filename in filenames:

        if filename.lower().endswith('.jpg'):

            img = io.imread(os.path.join(dirpath,filename))
            img_eq = exposure.equalize_adapthist(img, clip_limit=0.05)

            dest_filename = os.path.join(dest_dir, filename)

            base = os.path.splitext(dest_filename)[0]
            dest_filename = base + '.jpg'
            print(dest_filename)

            io.imsave(dest_filename, img_eq)




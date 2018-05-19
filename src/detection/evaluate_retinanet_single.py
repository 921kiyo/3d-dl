import keras

from keras_retinanet import models
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color
from keras_retinanet.utils.image import (
    read_image_bgr,
    preprocess_image,
    resize_image,
)

# import miscellaneous modules
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
from detection import train_keras_retinanet as ret

# set tf backend to allow memory to grow, instead of claiming everything
import tensorflow as tf

def get_session():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.Session(config=config)

# use this environment flag to change which GPU to use
# os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# set the modified tf session as backend in keras
keras.backend.tensorflow_backend.set_session(get_session())

# path to the saved model
model_path = 'D:\\PycharmProjects\\Lobster\\data\\logs\\retinanet_debug_logs\\second_attempt\\resnet50_csv_150_inf.h5'
# folder containing the test set
image_path = 'D:\\PycharmProjects\\manhattan_test_data\\phone_2_test\\phone_2_test\\StrawberryYogurt\\20180404_2247560.jpg'
# load label to names mapping for visualization purposes
labels_to_names = {0:'Anchor', 1:'Coconut', 2:'CottageCheese', 3:'Halloumi', 4:'Liberte', 5:'MangoYogurt', 6:'Soup', 7:'SoyMilk', 8:'Squashums', 9:'StrawberryYogurt'}

# load retinanet model
model = models.load_model(model_path, backbone_name='resnet50')

# read in the image
image = read_image_bgr(image_path)

# copy image to draw on
draw = image.copy()
draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)

# preprocess image for network
image = preprocess_image(image)
image, scale = resize_image(image, min_side=224, max_side=224)

# run prediction with threshold score 0.3
threshold = 0.3
detections = ret.predict_with_threshold(model, image, threshold)
'''
detections is a 3-tuple with:
detections[0] = list of scores
detections[1] = list of labels
detections[2] = list of boxes, each box is a 4-tuple, (cmin, rmin, cmax, rmax)
'''
scores, labels, boxes = detections

# draw annotation for every detection
for score, label, box in zip(scores, labels, boxes):
    # correct for image scale
    box /= scale

    # get the correct color
    color = label_color(label)

    # draw box on annotated image
    b = box.astype(int)
    draw_box(draw, b, color=color, thickness=4)

    caption = "{} {:.3f}".format(labels_to_names[label], score)
    draw_caption(draw, b, caption)
    # break # alternatively, show only one detection

plt.figure(figsize=(15, 15))
plt.axis('off')
plt.imshow(draw)
plt.show()


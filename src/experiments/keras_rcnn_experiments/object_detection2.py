import argparse
import functools
import os
import sys
import warnings
import csv
from pathlib import Path
import datetime

import keras
import keras.preprocessing.image
from keras.utils import multi_gpu_model
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import Callback

import tensorflow as tf
import numpy as np

# Change these to absolute imports if you copy this script outside the keras_retinanet package.
from keras_retinanet import layers
from keras_retinanet import losses
from keras_retinanet import models
from keras_retinanet.callbacks import RedirectModel
from keras_retinanet.callbacks.eval import Evaluate
from keras_retinanet.models.retinanet import retinanet_bbox
from keras_retinanet.preprocessing.csv_generator import CSVGenerator
from keras_retinanet.preprocessing.kitti import KittiGenerator
from keras_retinanet.preprocessing.open_images import OpenImagesGenerator
from keras_retinanet.preprocessing.pascal_voc import PascalVocGenerator
from keras_retinanet.utils.anchors import make_shapes_callback, anchor_targets_bbox
from keras_retinanet.utils.keras_version import check_keras_version
from keras_retinanet.utils.model import freeze as freeze_model
from keras_retinanet.utils.transform import random_transform_generator

from keras_retinanet.bin import train
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image

score_threshold = 0.05

def filter(scores, labels, threshold):

    hi = []
    lo = []
    
    for i in range(scores.shape[0]):

        hi_idx = np.nonzero(scores[i,:]>threshold)
        lo_idx = np.nonzero(scores[i,:]<=threshold)

        hi_scores = scores[i,:][hi_idx]
        hi_labels = labels[i,:][hi_idx]
        sorted_idx = np.argsort(hi_scores)
        
        hi.append((hi_scores[sorted_idx], hi_labels[sorted_idx]))

    return hi

def evaluate(detections, gts, top=3):

    assert top > 0, 'number of top selections must be greater than 0!'
    
    tp = 0
    fp = 0

    for detection, gt_label in zip(detections, gts):
        
        labels = detection[1][0:top]
        if labels.shape[0] == 0:
            continue # no detection

        gt_label = np.argwhere(gt_label>0.)[0]
        
        correct = np.argwhere(labels.astype(int) == gt_label)
        
        if correct.shape[0] > 0:
            tp += 1
            fp += labels.shape[0] - 1
        else:
            fp += labels.shape[0]

    return tp, fp
            

def dir2csv(directory):

    filenames_csv = os.path.join(directory, os.path.basename(directory) + '.csv')
    if os.path.exists(filenames_csv):
        os.remove(filenames_csv)
    classnames = []
    
    with open(filenames_csv, 'w') as csvfile:

        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        for (dirpath, dirnames, filenames) in os.walk(directory):
            if dirpath==directory:
                continue
            classname = os.path.basename(dirpath)
            classnames.append(classname)
            for filename in filenames:
                abs_filename = os.path.join(dirpath, filename)
                writer.writerow((abs_filename, 0, 0, 1, 1, classname))

    classnames.sort()
    classnames_csv = os.path.join(directory, os.path.basename(directory) + '_classes.csv')
    if os.path.exists(classnames_csv):
        os.remove(classnames_csv)
    i = 0
    with open(classnames_csv, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for classname in classnames:
            writer.writerow((classname,i))
            i += 1

    return filenames_csv, classnames_csv
        

def rgb2bgr(X):
    Y = np.zeros(X.shape)
    Y[:,:,:,0] = X[:,:,:,2]
    Y[:,:,:,1] = X[:,:,:,1]
    Y[:,:,:,2] = X[:,:,:,0]
    return Y

def detection_as_classification(model, test_generator):

    i = 0
    TP = 0
    FP = 0
    
    for X,Y in test_generator:
        if i >= len(test_generator):
            break # otherwise will run indefinitely
        X = preprocess_image(X)
        X = rgb2bgr(X)
        boxes, scores, labels = model.predict_on_batch(X)
        tp, fp = evaluate(filter(scores, labels, score_threshold), Y)
        i += 1
        TP += tp
        FP += fp

    return TP, FP

class ClassificationCallback(Callback):
    def __init__(self, args, log_filename, test_data_dir, prediction_model, batch_size=50):

        super(ClassificationCallback, self).__init__()
        self.log_filename = log_filename
        self.batch_size = batch_size
        self.model = prediction_model
        self.test_data_dir = test_data_dir
        self.snapshot_data = {'path':args.snapshot_path,'backbone': args.backbone, 'dataset_type': args.dataset_type}
        self.num_epochs = args.epochs
        
        self.test_datagen = ImageDataGenerator(rescale=1.)
        
        self.test_generator = self.test_datagen.flow_from_directory(
            self.test_data_dir,
            target_size=(224, 224),
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=False)

    def on_epoch_end(self, epoch, logs={}):
        model_path = '{backbone}_{dataset_type}_{epoch:02d}.h5'.format(
            backbone=self.snapshot_data['backbone'], dataset_type=self.snapshot_data['dataset_type'], epoch=(epoch+1))
        model_path = os.path.join(self.snapshot_data['path'], model_path)
        print('loading model {}, this may take a while ... '.format(model_path))
        self.model = models.load_model(model_path, convert=True, backbone_name=self.snapshot_data['backbone'], nms=False)
        TP, FP = detection_as_classification(self.model, self.test_generator)
        precision = float(TP)/(len(self.test_generator)*self.batch_size)
        if TP+FP == 0:
            recall = -1
        else:
            recall = float(TP)/(TP+FP)

        my_file = Path(self.log_filename)

        # write header if this is the first run
        if not my_file.is_file():
            print("writing head")
            with open(self.log_filename, "w") as log:
                log.write("datetime,epoch,precision,recall\n")

        # append parameters
        with open(self.log_filename, "a") as log:
            log.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
            log.write(',')
            log.write(str(epoch))
            log.write(',')
            log.write(str(precision))
            log.write(',')
            log.write(str(recall))
            log.write('\n')

        print('\nValidation set at {}% :'.format(self.test_data_dir))
        print('Precision: {}% , Recall: {}%'.format(precision*100, recall*100))

        # remove snapshots, but save the last one
        if not epoch >= self.num_epochs-1:
            os.remove(model_path)

        
def add_classification_callbacks(args, callbacks):
    logs = os.path.join(args.tensorboard_dir, 'second_validation_logs.csv')
    callbacks.append(ClassificationCallback(args, logs, args.second_val_data, None))
    return callbacks

                                                                                            
def train_main(args=None):
    # parse arguments
    if args is None:
        args = sys.argv[1:]
    args = train.parse_args(args)

    args.batch_size = 50
    args.steps = 5000/args.batch_size
    args.epochs = 30
    args.image_max_side = 224
    args.image_min_side = 224
    args.random_transform = False
    args.dataset_type = 'csv'
    args.annotations = './shapes.csv'
    args.classes = './classes.csv'
    args.val_annotations = './shapes.csv'
    args.second_val_data = '/vol/project/2017/530/g1753002/ThirdPartyRepos/keras-rcnn/keras_rcnn/data/shape/images_classify/'

    # create object that stores backbone information
    backbone = models.backbone(args.backbone)

    # make sure keras is the minimum required version
    train.check_keras_version()

    # optionally choose specific GPU
    if args.gpu:
        os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu
    keras.backend.tensorflow_backend.set_session(train.get_session())

    # create the generators
    train_generator, validation_generator = train.create_generators(args)

    # create the model
    if args.snapshot is not None:
        print('Loading model, this may take a second...')
        model            = models.load_model(args.snapshot, backbone_name=args.backbone)
        training_model   = model
        prediction_model = retinanet_bbox(model=model)
    else:
        weights = args.weights
        # default to imagenet if nothing else is specified
        if weights is None and args.imagenet_weights:
            weights = backbone.download_imagenet()

        print('Creating model, this may take a second...')
        model, training_model, prediction_model = train.create_models(
            backbone_retinanet=backbone.retinanet,
            num_classes=train_generator.num_classes(),
            weights=weights,
            multi_gpu=args.multi_gpu,
            freeze_backbone=args.freeze_backbone
        )

    # print model summary
    print(model.summary())

    # this lets the generator compute backbone layer shapes using the actual backbone model
    if 'vgg' in args.backbone or 'densenet' in args.backbone:
        compute_anchor_targets = functools.partial(anchor_targets_bbox, shapes_callback=make_shapes_callback(model))
        train_generator.compute_anchor_targets = compute_anchor_targets
        if validation_generator is not None:
            validation_generator.compute_anchor_targets = compute_anchor_targets

    # create the callbacks
    callbacks = train.create_callbacks(
        model,
        training_model,
        prediction_model,
        validation_generator,
        args,
    )

    callbacks = add_classification_callbacks(args, callbacks)

    # start training
    training_model.fit_generator(
        generator=train_generator,
        steps_per_epoch=args.steps,
        epochs=args.epochs,
        verbose=1,
        callbacks=callbacks,
    )

def test(saved_model_path, test_data_dir):
    model = models.load_model(saved_model_path, backbone_name='resnet50')
    detection_as_classification(model, test_data_dir)
    
if __name__ == '__main__':

    train_main()
    #shapes = '/vol/project/2017/530/g1753002/ThirdPartyRepos/keras-rcnn/keras_rcnn/data/shape/images_classify/'
    #ocado = '/data/g1753002_ocado/manhattan_project/test_data/extended_test_set_ambient/'
    #test('./snapshots_inference/resnet50_csv_10.h5', shapes)

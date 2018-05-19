import functools
import os
import sys
import csv
from pathlib import Path
import datetime

import keras
import keras.preprocessing.image
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import Callback
from keras import backend as K

import numpy as np
import gc

from keras_retinanet import models
from keras_retinanet.models.retinanet import retinanet_bbox
from keras_retinanet.preprocessing import csv_generator
from keras_retinanet.bin import train
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image

score_threshold = 0.05

def read_class_csv(csv_class_file):
    """
    function that reads in a class csv file that is used as an input to the retinanet training routine, and outputs
    a list of class names which is the format required by Keras ImageGenerator
    :param csv_class_file: the filename of the csv containing class names and indices
    :return: list of classnames
    """
    try:
        with csv_generator._open_for_csv(csv_class_file) as file:
            classes = csv_generator._read_classes(csv.reader(file, delimiter=','))
            class_list = list(classes.keys())
            for c in classes:
                class_idx = classes[c]
                class_list[class_idx] = c
            return class_list
    except ValueError as e:
        raise_from(ValueError('invalid CSV class file: {}: {}'.format(csv_class_file, e)), None)
        
def filter(scores, labels, threshold, boxes=None):

    """
    Given a threshold, a list of scores (size = (batch, max_detections)), for each sample i, filter scores[i,:] less
    than threshold, and get corresponding labels.
    :param scores: array of scores of size (batch, max_detections)
    :param labels: array of labels of size (batch, max_detections)
    :param threshold: min score to be considered
    :return: tuples of filtered (scores, labels)
    """
    hi = []

    for i in range(scores.shape[0]):

        hi_idx = np.nonzero(scores[i,:]>threshold)

        hi_scores = scores[i,:][hi_idx]
        hi_labels = labels[i,:][hi_idx]
        sorted_idx = np.argsort(hi_scores)

        if boxes is not None:
            hi_boxes = boxes[i,:][hi_idx]
            hi.append((hi_scores[sorted_idx], hi_labels[sorted_idx], hi_boxes[sorted_idx]))
        else:
            hi.append((hi_scores[sorted_idx], hi_labels[sorted_idx]))

    return hi

def evaluate(detections, gts, top=3):
    """
    Evaluates the top N detection as classification (DAC) accuracy for a batch of detections
    :param detections: given a tuple of filtered detections (scores, labels), determine if the top N labels (ranked by
    scores) contain the ground truth gt, and if so, add one to tp. All other detections are fp's
    :param gts: ground truth labels
    :param top: number of top detections to consider
    :return: the number of true positive and false positive detections
    """

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
    """
    utility function to convert a directory structure to retinanet csv format for a detection as classification task
    since there is not bbox information, this will all be fixed.
    :param directory:
    :return:
    """

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
    """
    RGB format to BGR format
    :param X: images (assuming color channel last, and batch first)
    :return: converted images
    """
    Y = np.zeros(X.shape)
    Y[:,:,:,0] = X[:,:,:,2]
    Y[:,:,:,1] = X[:,:,:,1]
    Y[:,:,:,2] = X[:,:,:,0]
    return Y

def detection_as_classification(model, test_generator):
    """
    Given a test_generator that is a regular Keras image generator (for classification tasks), run a DAC evaluate using
    the given model, and return the toal number of TP's and FP's
    :param model: model to run predictions
    :param test_generator: Keras ImageGenerator iterator
    :return: true positive number, and false positive number (detections)
    """
    i = 0
    TP = 0
    FP = 0
    
    for X,Y in test_generator:
        if i >= len(test_generator):
            break # otherwise will run indefinitely
        X = rgb2bgr(X)
        X = preprocess_image(X)
        boxes, scores, labels = model.predict_on_batch(X)
        tp, fp = evaluate(filter(scores, labels, score_threshold), Y)
        i += 1
        TP += tp
        FP += fp

    return TP, FP

class ClassificationCallback(Callback):
    """
    Callback to run DAC task on a directory, inside a retinanet training routine.
    Works by fetching the snapshot from snapshot_path, and running detection as classification on the images in
    test_data_dir.
    Writes results into log_filename
    """
    def __init__(self, args, log_filename, test_data_dir, prediction_model, delete_model=False, batch_size=50):

        super(ClassificationCallback, self).__init__()
        self.class_list = read_class_csv(args.classes)
        self.log_filename = log_filename
        self.batch_size = batch_size
        self.model = prediction_model
        self.test_data_dir = test_data_dir
        self.snapshot_data = {'path':args.snapshot_path,'backbone': args.backbone, 'dataset_type': args.dataset_type}
        self.num_epochs = args.epochs

        self.delete_model = delete_model
        
        self.test_datagen = ImageDataGenerator(rescale=1.)
        
        self.test_generator = self.test_datagen.flow_from_directory(
            self.test_data_dir,
            target_size=(224, 224),
            batch_size=self.batch_size,
            classes = self.class_list,
            class_mode='categorical',
            shuffle=False)

    def on_epoch_end(self, epoch):
        # load this epoch's saved snapshot
        model_path = '{backbone}_{dataset_type}_{epoch:02d}.h5'.format(
            backbone=self.snapshot_data['backbone'], dataset_type=self.snapshot_data['dataset_type'], epoch=(epoch+1))
        model_path = os.path.join(self.snapshot_data['path'], model_path)
        print('loading model {}, this may take a while ... '.format(model_path))
        self.model = models.load_model(model_path, convert=True, backbone_name=self.snapshot_data['backbone'], nms=False)
        
        # run a detection as classification on the model and our test dataset
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

        print('\nValidation set at {}:'.format(self.test_data_dir))
        print('Precision: {}% , Recall: {}% \n'.format(precision*100, recall*100))

        # remove snapshots, but save the last one
        if (not epoch >= self.num_epochs-1) and self.delete_model:
            os.remove(model_path)
        # make sure we don't run out of memory!
        del self.model
        gc.collect()

        
def add_classification_callbacks(args, callbacks, prediction_model):
    """
    self - explanatory
    :param args: the command line arguments given to the scrip
    :param callbacks: the list of callbacks to add the classification to
    :param prediction_model:
    :return: the callbacks list with the classification callbacks
    """
    logs = os.path.join(args.tensorboard_dir, 'rendered_validation_logs.csv')
    callbacks.append(ClassificationCallback(args, logs, args.rendered_val_data, prediction_model))
    logs = os.path.join(args.tensorboard_dir, 'real_validation_logs.csv')
    callbacks.append(ClassificationCallback(args, logs, args.real_val_data, prediction_model, delete_model = True))
    return callbacks

                                                                                            
def train_main(args=None):
    # parse arguments
    if args is None:
        args = sys.argv[1:]
        args = train.parse_args(args)

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
    # print(model.summary())

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

    callbacks = add_classification_callbacks(args, callbacks, None)

    # start training
    training_model.fit_generator(
        generator=train_generator,
        steps_per_epoch=args.steps,
        epochs=args.epochs,
        verbose=1,
        callbacks=callbacks,
        initial_epoch=args.initial_epoch
    )

    # cleanup at the end of every epoch since we keep loading prediction models
    del training_model
    del model
    del prediction_model
    K.clear_session()

def predict_with_threshold(model, X, threshold):
    single = False
    if X.ndim == 3:
        single = True
        X = np.expand_dims(X, axis=0)
    boxes, scores, labels = model.predict_on_batch(X)
    detections = filter(scores, labels, threshold, boxes)
    if single:
        return detections[0]
    return detections
    
if __name__ == '__main__':
    
    args = sys.argv[1:]
    args = train.parse_args(args)

    """
    Fixed training constants
    """
    args.batch_size = 50
    args.steps = 10000/args.batch_size
    args.epochs = 1
    args.image_max_side = 224
    args.image_min_side = 224
    args.random_transform = True
    args.dataset_type = 'csv'

    """
    The required data files
    """
    manhattan_root = '/data/g1753002_ocado/manhattan_project/'
    images_root = os.path.join(manhattan_root,
                               'training_data/ten_set_model_official_SUN_back_2018-05-11_08_03_02/images')
    args.annotations = os.path.join(images_root, 'train','annotations.csv')
    args.classes = os.path.join(images_root,'classes.csv')
    args.val_annotations = os.path.join(images_root, 'validation','annotations.csv')
    args.snapshot_path = os.path.join(manhattan_root, 'trained_models', 'retinanet_second_attempt')
    args.tensorboard_dir = os.path.join(args.snapshot_path, 'logs')
    args.rendered_val_data = os.path.join(images_root, 'validation')
    args.real_val_data = os.path.join(manhattan_root, 'test_data', 'extended_test_set_ambient')

    """
    Option to start from arbitrary epoch, as long as a snapshot of the correct last epoch exists in args.snapshot_path
    """
    args.initial_epoch = 1
    args.freeze_backbone = False
    epochs = 150

    """
    Training strategy:
    Run train_main() for a single epoch. This allows train_main() to run to completion, and clear GPU memory.
    Update the epoch number everytime we start a new run, so train main runs for exactly one more epoch
    """
    for e in range(args.initial_epoch, epochs, 1):
        args.initial_epoch = e
        args.epochs = e+1
        if e > 0:
            model_path = '{backbone}_{dataset_type}_{epoch:02d}.h5'.format(
            backbone='resnet50', dataset_type=args.dataset_type, epoch=(e))
            model_path = os.path.join(args.snapshot_path, model_path)
            args.snapshot = model_path
        train_main(args=args)
        # remove
        if e > 0:
            os.remove(model_path)

    #shapes = '/vol/project/2017/530/g1753002/ThirdPartyRepos/keras-rcnn/keras_rcnn/data/shape/images_classify/'
    #ocado = '/data/g1753002_ocado/manhattan_project/test_data/extended_test_set_ambient/'
    #test('./snapshots_inference/resnet50_csv_10.h5', shapes)

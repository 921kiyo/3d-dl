#from keras.applications.inception_v3 import InceptionV3
#from keras.applications.resnet50 import ResNet50
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K

from keras.preprocessing.image import ImageDataGenerator

from keras.callbacks import TensorBoard

from keras.optimizers import SGD

from keras.callbacks import TensorBoard, Callback
from pathlib import Path
import os
import datetime

batch_size = 64

"""source dirs"""
project_dir = '/data/g1753002_ocado/manhattan_project'
train_data_dir = os.path.join(project_dir, 'training_data/split_ten_set_model_official_SUN_back_2018-04-07_13_19_16/train/')
validation_data_dir = os.path.join(project_dir, 'training_data/split_ten_set_model_official_SUN_back_2018-04-07_13_19_16/validation')
test_data_dir = os.path.join(project_dir, 'test_data/extended_test_set_ambient/')
train_output = os.path.join(project_dir, 'trained_models/vgg16_unfrozen')
log_filename = os.path.join(train_output, 'training_logs.csv')
model_filename = os.path.join(train_output, 'model.h5')

"""configure generators"""
train_datagen = ImageDataGenerator(
        rescale=1./255,
        zoom_range=0.2)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        train_data_dir,  # this is the target directory
        target_size=(224, 224),  # all images will be resized to 150x150
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=True)

validation_generator = test_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=True)

class ExtraValidationCallback(Callback):
    def __init__(self, log_filename, test_data_dir):
        super(ExtraValidationCallback, self).__init__()
        self.test_generator = test_datagen.flow_from_directory(
            test_data_dir,
            target_size=(224, 224),
            batch_size=batch_size,
            class_mode='categorical',
            shuffle=True)
        self.log_filename = log_filename

    def on_train_begin(self, logs={}):
        self.val1_accs = []
        self.val1_loss = []
        self.val2_accs = []
        self.val2_loss = []
        self.train_accs = []
        self.train_loss = []

    def on_epoch_end(self, epoch, logs={}):
        self.val1_accs.append(logs.get('val_acc'))
        self.val1_loss.append(logs.get('val_loss'))

        # generator for test data
        # similar to above but based on different augmentation function (above)
        loss, acc = self.model.evaluate_generator(self.test_generator)

        self.val2_accs.append(acc)
        self.val2_loss.append(loss)

        self.train_accs.append(logs.get('acc'))
        self.train_loss.append(logs.get('loss'))

        logging = True

        if logging:
            print("logging now...")
            my_file = Path(self.log_filename)

            # write header if this is the first run
            if not my_file.is_file():
                print("writing head")
                with open(self.log_filename, "w") as log:
                    log.write("datetime,epoch,val1_acc,val1_loss,val2_acc,val2_loss,train_acc,train_loss\n")

            # append parameters
            with open(self.log_filename, "a") as log:
                log.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                log.write(',')
                log.write(str(epoch))
                log.write(',')
                log.write(str(logs.get('val_acc'))),
                log.write(',')
                log.write(str(logs.get('val_loss'))),
                log.write(',')
                log.write(str(acc)),
                log.write(',')
                log.write(str(loss)),
                log.write(',')
                log.write(str(logs.get('acc'))),
                log.write(',')
                log.write(str(logs.get('loss')))
                log.write('\n')

        print('\Second Validation Set, loss: {}, acc: {}\n'.format(loss, acc))

"""start construction of CNN"""
# create the base pre-trained model
#base_model = InceptionV3(weights='imagenet', include_top=False)
#base_model = ResNet50(weights='imagenet', include_top=False)
base_model = VGG16(weights='imagenet', include_top=False)
# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
x = Dense(1024, activation='relu')(x)
# and a logistic layer -- let's say we have 200 classes
predictions = Dense(10, activation='softmax')(x)

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers
for layer in base_model.layers:
    layer.trainable = True

"""train the CNN"""
# compile the model (should be done *after* setting layers to non-trainable)
model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy', metrics=['accuracy'])

extraval = ExtraValidationCallback(log_filename, test_data_dir)
# train the model on the new data for a few epochs
model.fit_generator(
        train_generator,
        steps_per_epoch=12000 // batch_size,
        epochs=100,
        validation_data=validation_generator,
        validation_steps=1600 // batch_size,
        callbacks = [extraval])

model.save(model_filename)

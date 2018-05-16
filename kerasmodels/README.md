## Training
For an example how to use the wrapper, see retrain_main.py
Class:

  KerasInception(self,input_dim=150,batch_size=16,dense_layers=1,dropout=None,
            lr=0.0031622777, dense_dim=1024)

Methods:

    def train(self,train_dir,validation_dir,epochs=0,fine_tune=False, unfrozen_layers=0,
            salt_pepper=False,augmentation_params={},classes_txt_dir=None,save_model=False,
            validation_dir_2=None,steps_per_epoch=12000):
        """
        initializes the keras model object and trains the model
        train_dir: directory of training data
        validation_dir: directory of validation data
        epochs: number of epochs to train
        fine_tune: whether to fine-tune the model at the end of normal epochs
        unfrozen_layers: how many layers of the 311 inceptionV3 conv layers
                        should be retrained, has to be between 0 and 311
        salt_pepper: whether to add salt & pepper noise to the training images
        augmentation_params: list of augmentation parameters for keras
        classes_txt_dir: if provided a path, it will save a file named
            "classes.txt" containing the labels of all classes we train for,
            if None, it will not save such a file
        save_model: whether to save the model at the end of training
            name will default to model.h5 in the working directory
        validation_dir_2: if provided a path, this will calculate additional
            validation metrics for a second set of data and log everything
            in a csv in the current working directory
        steps_per_epoch: the number of images that should be processed between
            each validation (= the number of images per epoch)
        returns validation accuracy history
        """

    def evaluate(self,test_dir):
        """
        input = path to directory with test images, expects directory to
        be structured as follows: folders with names of classes, images in each
        of these folders
        output = loss, accuracy of the model
        """

    def load_model(self,file_path):
        """
        input = path to a model in h5 format (a model, not weights!)
        model will be as when saving (i.e. compiled), can then call predict etc
        """

    def save_model(self,path):
        """
        saves the current model to a specified path
        path has to contain the name of the file itself, i.e. end in ".h5"
        """

Utilities:

    def get_augmentation_params(augmentation_mode):
        """
        returns a list of augmentation parameters for training
        0 = no augmentation, 1 = rotation only, 2 = rotation & zoom
        """

    def unzip_and_return_path_to_folder(path_to_zip_file):
        """
        utility to unzip files containing training images
        input = path to a zip file
        unzips the file to a folder with the same name
        returns path to this folder
        """

## Keras Evaluation

All evaluation script can be found in `keras_eval.py`.

`keras()` function will execute all the evaluation and export them into Tensorboard. You need to supply the following paths as arguments.

    def eval(self, output_folder, test_folder, test_result_file, test_result_path, notify_interval, input_dim):
        """
        Starting point of evaluation and run all other functions above
        :param output_folder: folder path to where the trained model is.
        :param test_result_path: path to the test dataset
        :param test_result_file: path to the pre-supplied test result file
        :param notify_interval: frequency of printing the progress of the evaluation
        :return: N/A
        """

## Call Tensorboard:
```tensorboard --logdir=[logdirectory]```

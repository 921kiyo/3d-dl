## Training


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

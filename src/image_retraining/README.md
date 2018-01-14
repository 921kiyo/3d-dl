## About the Retraining Script
`retrain.py` is an example script that shows how one can adapt a pretrained
network for other classification problems. A detailed overview of this script
can be found at:
https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/#0

The script also shows how one can train layers
with quantized weights and activations instead of taking a pre-trained floating
point model and then quantizing weights and activations.
The output graphdef produced by this script is compatible with the TensorFlow
Lite Optimizing Converter and can be converted to TFLite format.


## About the Test Script
`retrain_test.py` is written for this project specifically. this script should only
be run after retrain.py has been run, and the relevant outputs generated (namely
the retrained CNN graph and identified output labels).

* `model_source_dir` is the directory containing the retrained CNN graph, while
* `label_path` should be the path to the list of labels in a list separated by returns. This assumes that the model was
trained on labels of the **product code** not the **barcode**
* `test_file_dir` contains the test images and these have the **barcode numbers** as its labels (as was given to us by
Ocado)
* `json_path` contains the json files holding the product info, which maps the **product code** to **barcodes**
* `test_result_path` is the given path to a pickle filename tell the script where to save test results to.

## About the visualize script
`testresult_visualize.py` loads the test results for plotting

## What remains to be done
`retrain.py` and `retrain_test.py` are quite basic scripts, and there are a number of things that need to be improved on:
* Everything is still being done via simple functions. It would be much appreciated if an OOP approach could be taken,
and all the lower level stuff hidden away. (start with trying to make the CNN graph an object, draw a UML first!)
* Concurrency would definitely help with speeding up the training. Currently, all the bottlenecks are calculated before 
training, and this is a wise decision if no live augmentations are applied (since we will be re-using images). However, 
if live augmentations are going to be applied, we need concurrent processing.
* Support GPU-based training! 
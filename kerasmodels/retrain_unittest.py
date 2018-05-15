import unittest
import retrain as rt
import numpy as np

import os

class TestKerasRetrain(unittest.TestCase):

    # assert that when calling fit on the model, the last layers change
    # (= are not the same as initial values)
    def test_training_last_layers(self):
        # TODO: Can be generalized: take an argument "number of top layers", include
        # them in a for loop and store weights in list

        train_dir = 'unit_test_images/'
        validation_dir = 'unit_test_images/'
        test_dir = 'unit_test_images/'

        # create model
        model = rt.KerasInception(dense_layers=1,
                                dropout=0,
                                dense_dim=1024)

        # initialize model (size of dense layer), 0 epochs
        model.train(train_dir=train_dir,
                    validation_dir=validation_dir,
                    epochs=0,
                    )

        # store weights before
        before_softmax = model.model.layers[-1].get_weights()
        before_dense = model.model.layers[-2].get_weights()

        # train
        model.train(train_dir=train_dir,
                    validation_dir=validation_dir,
                    fine_tune=True,
                    epochs=1,
                    salt_pepper=True,
                    classes_txt_dir=os.getcwd(),
                    unfrozen_layers=311,
                    steps_per_epoch=1000,
                    validation_dir_2=validation_dir
                    # save_model=True
                    )


        # store weights after
        after_softmax = model.model.layers[-1].get_weights()
        after_dense = model.model.layers[-2].get_weights()

        # check that something has changed
        self.assertFalse( np.array_equal(before_softmax,after_softmax) )
        self.assertFalse( np.array_equal(before_dense,after_dense) )
        # self.assertTrue( (before_softmax != after_softmax).any() )
        # self.assertTrue( (before_dense != after_dense).any() )

    # tests if the model stays stable for the layers we want it to be stable
    def test_base_model_stable(self):
        # dummy directories with black/white images
        train_dir = 'unit_test_images/'
        validation_dir = 'unit_test_images/'
        test_dir = 'unit_test_images/'

        # TODO delete
        count = 0

        # initialize two lists for weights
        before_transferred_weights = []
        after_transferred_weights = []

        # store all weights before
        base_model = rt.InceptionV3(weights='imagenet', include_top=False)

        # create model
        model = rt.KerasInception(dense_layers=1,
                                dropout=0,
                                dense_dim=1024)

        # initialize model (size of dense layer), 0 epochs
        model.train(train_dir=train_dir,
                    validation_dir=validation_dir,
                    epochs=0,
                    )

        for layer_bm, layer_fm in zip(base_model.layers,model.model.layers):
            before_transferred_weights.append(layer_fm.get_weights())
            count += 1

        # TODO delete
        # print(count)

        # train
        model.train(train_dir=train_dir,
                    validation_dir=validation_dir,
                    epochs=1,
                    salt_pepper=True,
                    classes_txt_dir=os.getcwd(),
                    unfrozen_layers=0,
                    steps_per_epoch=1000
                    # save_model=True
                    )

        # store all weights after
        for layer_bm, layer_fm in zip(base_model.layers,model.model.layers):
            after_transferred_weights.append(layer_fm.get_weights())

        # check that nothing changed for any of the layers
        for b, a in zip(before_transferred_weights,after_transferred_weights):
            # self.assertFalse( np.array_equal(b,a) )
            self.assertTrue( np.array_equal(b,a) )
            # self.assertTrue( (b == a).all() )


    # tests if model can be trained on two classes and perform significantly
    # better than random on a test set after 15 minutes of training
    def test_full_training(self):
        path_of_zip = 'unit_test_images_zipped.zip'
        train_dir = rt.unzip_and_return_path_to_folder(path_of_zip)

        # dummy directories with black/white images
        # train_dir = 'unit_test_images/'
        validation_dir = 'unit_test_images/'
        test_dir = 'unit_test_images/'

        # train
        model = rt.KerasInception(dense_layers=1,
                                dropout=0,
                                dense_dim=1024)

        model.train(train_dir=train_dir,
                    validation_dir=validation_dir,
                    fine_tune=True,
                    epochs=2,
                    salt_pepper=True,
                    classes_txt_dir=os.getcwd(),
                    unfrozen_layers=311,
                    steps_per_epoch=1000
                    # save_model=True
                    )

        # evaluate
        # TODO: how many images does this generate
        score = model.evaluate(test_dir=test_dir)

        print("accuracy on test images")
        print(score[1])
        # check if significantly better than random
        self.assertTrue( score[1] > 0.6 )

    def test_layers_connected(self):
        train_dir = 'unit_test_images/'
        validation_dir = 'unit_test_images/'
        test_dir = 'unit_test_images/'

        model = rt.KerasInception(dense_layers=1,
                                dropout=0,
                                dense_dim=1024)

        # initialize model (size of dense layer), 0 epochs
        model.train(train_dir=train_dir,
                    validation_dir=validation_dir,
                    epochs=0,
                    )

        self.assertTrue(np.array_equal(model.model.get_layer('base_output').output,model.model.get_layer('pooling').input))
        self.assertTrue(np.array_equal(model.model.get_layer('pooling').output,model.model.get_layer('dense0').input))
        self.assertTrue(np.array_equal(model.model.get_layer('dense0').output,model.model.get_layer('softmax').input))

    # TODO: write test that loss is never zero


if __name__ == '__main__':
    unittest.main()

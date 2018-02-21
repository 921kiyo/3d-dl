import unittest
import retrain as rt
import numpy as np

class TestKerasRetrain(unittest.TestCase):

    # assert that if i call fit on the model, the last layers change
    # (= are not the same as initial values)
    def test_training_last_layers(self):
        # TODO: Can be generalized: take an argument "number of top layers", include
        # them in a for loop and store weights in list

        train_dir = 'unit_test_images/'
        validation_dir = 'unit_test_images/'
        test_dir = 'unit_test_images/'

        model = rt.assemble_model()

        # store weights before
        before_softmax = model.layers[-1].get_weights()
        before_dense = model.layers[-2].get_weights()

        # train
        rt.train_model(model,epochs=1,train_dir=train_dir,validation_dir=validation_dir)

        # store weights after
        after_softmax = model.layers[-1].get_weights()
        after_dense = model.layers[-2].get_weights()

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
        model = rt.assemble_model()

        for layer_bm, layer_fm in zip(base_model.layers,model.layers):
            before_transferred_weights.append(layer_fm.get_weights())
            count += 1

        # TODO delete
        print(count)

        # train
        rt.train_model(model,epochs=1,train_dir=train_dir,validation_dir=validation_dir)

        # store all weights after
        for layer_bm, layer_fm in zip(base_model.layers,model.layers):
            after_transferred_weights.append(layer_fm.get_weights())

        # check that nothing changed for any of the layers
        for b, a in zip(before_transferred_weights,after_transferred_weights):
            self.assertTrue( np.array_equal(b,a) )
            # self.assertTrue( (b == a).all() )


    # tests if model can be trained on two classes and perform significantly
    # better than random on a test set after 15 minutes of training
    def test_full_training(self):
        # dummy directories with black/white images
        train_dir = 'unit_test_images/'
        validation_dir = 'unit_test_images/'
        test_dir = 'unit_test_images/'

        # train
        model = rt.assemble_model()
        rt.train_model(model,epochs=5)

        # evaluate
        # TODO: how many images does this generate
        score = rt.evaluate(model)

        print("accuracy on b/w images")
        print(score[1])
        # check if significantly better than random
        self.assertTrue( score[1] > 0.6 )

    def test_layers_connected(self):
        model = rt.assemble_model()

        self.assertTrue(np.array_equal(model.get_layer('base_output').output,model.get_layer('pooling').input))
        self.assertTrue(np.array_equal(model.get_layer('pooling').output,model.get_layer('dense').input))
        self.assertTrue(np.array_equal(model.get_layer('dense').output,model.get_layer('softmax').input))

    # TODO: write test that loss is never zero


if __name__ == '__main__':
    unittest.main()

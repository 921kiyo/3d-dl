import retrain as rt

def main():
    # train_dir = '/data/g1753002_ocado/manhattan_project/training_data/split_ten_set_model_official_SUN_back_2018-04-07_13_19_16/train'
    train_dir = '/data/g1753002_ocado/manhattan_project/training_data/ten_set_model_official_SUN_back_2018-05-11_08_03_02/images/train'
    # validation_dir = '/data/g1753002_ocado/manhattan_project/training_data/split_ten_set_model_official_SUN_back_2018-04-07_13_19_16/validation'
    validation_dir = '/data/g1753002_ocado/manhattan_project/training_data/ten_set_model_official_SUN_back_2018-05-11_08_03_02/images/validation'
    # test_dir = '/data/g1753002_ocado/manhattan_project/test_data/extended_test_set_ambient'
    test_dir = '/data/g1753002_ocado/manhattan_project/test_data/official_test_set_factory'

    # can add second dir if need two validation sets
    extra_validation_dir = None

    dense_layers = 1
    input_dim = 224
    batch_size = 64
    fine_tune = False # if true, some of the inceptionV3 layers will be trained for 1 epoch at the end of training
    add_salt_pepper_noise = False # if True, it adds SP noise
    augmentation_mode = 0
    epochs = 11
    # has to be a number between 0 and 311
    unfrozen_layers = 311
    learning_rate = 0.0031622777

    model = rt.KerasInception(input_dim=input_dim,
                            batch_size=batch_size,
                            dense_layers=dense_layers)


    model.train(train_dir=train_dir,
                validation_dir=validation_dir,
                fine_tune=fine_tune,
                epochs=epochs,
                unfrozen_layers=unfrozen_layers,
                salt_pepper=add_salt_pepper_noise,
                augmentation_params=rt.get_augmentation_params(augmentation_mode),
                validation_dir_2=extra_validation_dir)

    model.evaluate(test_dir=test_dir)

    model.save_model('occlusion_model.h5')

if __name__== "__main__":
  main()

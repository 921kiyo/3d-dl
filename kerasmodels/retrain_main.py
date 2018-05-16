import retrain as rt

def main():
    train_dir = 'PATH/TO/DIRECTORY'
    validation_dir = 'PATH/TO/DIRECTORY'
    test_dir = 'PATH/TO/DIRECTORY'

    # can add second dir if need two validation sets
    extra_validation_dir = None

    dense_layers = 1
    input_dim = 224
    batch_size = 64
    # if true, 2 inception layers will be trained for 1 epoch at end of training
    fine_tune = False
    # if True, it adds SP noise
    add_salt_pepper_noise = False
    augmentation_mode = 0
    epochs = 10
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

    model.save_model('model.h5')

if __name__== "__main__":
  main()

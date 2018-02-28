## KerasInception API

Class:
* KerasInception(self,input_dim=150,batch_size=16,dense_layers=1)

Methods:
* model.train(self,train_dir,validation_dir,epochs=5,fine_tune=False,salt_pepper=False,augmentation_params={}):
* model.evaluate(self,test_dir)
* model.save_model(self,name)

Helper Function:
* get_augmentation_params(augmentation_mode)

Example how you could use the API:
```
  train_dir = '/vol/project/2017/530/g1753002/keras_test_data/train'
  validation_dir = '/vol/project/2017/530/g1753002/keras_test_data/validation'
  test_dir = '/vol/project/2017/530/g1753002/keras_test_data/test'
  dense_layers = 1
  input_dim = 150
  batch_size = 16
  fine_tune = False # if true, some of the inceptionV3 layers will be trained for 5 epochs at the end of training
  add_salt_pepper_noise = False # if True, it adds SP noise
  augmentation_mode = 0 # 0 = no augmentation, 1 = rotation only, 2 = rotation & zoom
  epochs = 5

  model = KerasInception(input_dim=input_dim,
                          batch_size=batch_size,
                          dense_layers=dense_layers)

  model.train(train_dir=train_dir,
              validation_dir=validation_dir,
              fine_tune=fine_tune,
              epochs=epochs,
              salt_pepper=add_salt_pepper_noise,
              augmentation_params=get_augmentation_params(augmentation_mode))

  model.evaluate(test_dir=test_dir)
```

## Call Tensorboard:
```tensorboard --logdir=[logdirectory]```

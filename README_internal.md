# Machine Learning for Object Recognition at Ocado

### ensure correct read/write permissions on Group Directory

As per emails of Fidelis/Duncan, add
```
umask 002
```

to the end of .bashrc file on your home directory

### How to Generate training data

Get the correct files by pulling the branch pavel/pipeline 
(Once merged this will be changed)

ssh into the GPU: ssh <username>@gpu04.doc.ic.ac.uk

navigate into src/rendering run:

python render_pipeline.py

The generated zip files are in:
/vol/project/2017/530/g1753002/render_workspace/final_zip

The render_workspace contains all the necessary data for generation.
Once your generation is complete, please copy the zip files out of the folder
If somebody tries to generate another set with same name, it will override your
files. So please keep the folder ideally completely empty.



### How to Train

## activate correct CUDA version to link TF to GPU
create a file in your home directory called .bash_profile

with content and save:

```
if [ -f /vol/cuda/8.0.61-cudnn.7.0.2/setup.sh ]
then
   . /vol/cuda/8.0.61-cudnn.7.0.2/setup.sh
fi
```

then log out and log in again or restart bash

## activating shared ocado venv from anywhere
venv is installed in group folder, run this line in bash
```
. /vol/project/2017/530/g1753002/ocadovenv/ocadovenv/bin/activate
```

## run
go to Lobster/src/image_retraining/
```
$ bash run_retrain.bat
```
this automatically directs retrain.py to the folder
```
/vol/project/2017/530/g1753002/product-image-dataset
```

If you want to redirect the training script to a different image folder, run retrain.py as follows:
```
$ python ./retrain.py --image_dir [some path]

```

## exit venv
```
$ deactivate
```

### Linter

Run Pep 8 (TDB)

[Online version](http://pep8online.com/)

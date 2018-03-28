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

### 1. Installing Anaconda

[What is Anaconda?](https://www.anaconda.com/what-is-anaconda/)

I choose Anaconda for 2 reasons.

1. Anaconda is one of the most popular open source distribution for data science project.

2. We will have to use Anaconda for Lab PC.

Once Anaconda (for Python3) is installed, got to the project directory, and run

`conda env create -f environment.yaml`

to create an virtualenv with all dependencies specified in environment.yaml, so everyone gets the same envrionment.

To get into the vertual environment, run

`source activate venv`

(This command could be different depending on your OS)

This environment is different from your local computer.

Make sure you are using python3 (not python2) in this environment by running

`python --version `

If not, try

`conda create -n py3 python=3.5 `


## Git workflow

Our branching workflow is as follow.

- `master` Fully working program.

    E.g if this project was a E-commerce website, this codebase is live-working website, and what users interact with.

- `product` Fully working program, but not live.


- `features/XXX` features branches, where everyone does real development here

### Branching and pull requests rules

1. When you are assigned a issue, create a new branch from `product` branch (never from `master`), and do your work.
    - When you make a branch from `product`, make sure to start the name with `features/XXX` where XXX is the name of the issue you are working with (e.g `features/image_argumentation` )

2. When you have finished your task/issue, make a pull request to `product`.
    - When you do it, make sure to always refer to which issue you've done on the pull request comment (e.g "Resolve #11 Update a final layer ", where #11 is the issue No.).

3. Usually Ong and Kiyo have to do reviews for all pull requests. If the pull request looks okay, Kiyo or Ong merge it into `product`.
    - Make sure to delete the branch and close the issue/update the issue board after the merging.

### Warning

- Usually no one does any direct changes on any code on `master` and `product` branches. These two branches will be updated only by merging by Kiyo or Ong.

- In case we've found a bug on `product` (which means Kiyo or Ong's mistakes), we can fix the bug on `product` branch.

- `master` has to be always error-free and we can show our project to anyone at anytime.

## Coding Style Guide

TBD

This is too obvious, but please make your code readable (leave comments, better variables names), because other people will read your code.

### Linter

Run Pep 8 (TDB)

[Online version](http://pep8online.com/)

## Folder Structures

I took the idea from [this post](https://www.kaggle.com/general/4815#25562). We might adjust it slightly as we make progress.

`/analysis`

- All quick analysis/initial experiments are done, and this directory is sparated from our project codebase.


`/download`

- downloaded data only (No augumented/manipulated data).

`/features`

- features fed to classifier.

`/logs`

- Keep all the loggings in here (logging is what you see on your command line when you are executing the program/training the model)

- We might not do this, but we will experiment

`/src`

- All the working files

## Technology used

Python 3.6.4

Tensorflow version XXX

TODO

## Project Description (FYI)

Ocado is an online supermarket delivering groceries to customers within a one hour time slot. This involves using highly automated warehouses to fulfil 250,000+ orders a week from a range of 50,000+ products. However, there are still parts of the warehouse which require manual labour and barcode scanners to recognise products. Hence Ocado is interested in any new techniques which might speed up this process.

Engineers at Ocado Technology are automatically collecting a large number of labelled images from the warehouse (so far of over 100 different products with an average of 5000 images each). Preliminary investigations on using DNNs on these datasets have shown great promise. Ocado Technology is excited to support one or more groups of students to see what can be achieved. A prize for the best project will be awarded. Interested groups can also get a tour of one of Ocado’s automated warehouses.

The project will involve the following steps:

1. Make a project plan and do background reading,

2. training data organisation

3. implement a state-of-the art deep learning network to do image classification

4. develop deployment strategy for chosen approach

5. evaluate prediction performance and investigate failure cases trough network introspection methods

6. reporting and documentation

The available data allows for more than one group. Each group will pick a different approach and focus on different aspects of the given problem statement (data augmentation, OCR, transfer learning to out of warehouse environments, error investigation, automatic captioning of products, etc.)

You will get exclusive access to as many training resources as necessary in our student lab for this project (high-end GPU accelerated machines).

## Lastly...

I am also learning project management, so any feedback is always welcome;)

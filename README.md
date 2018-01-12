# Machine Learning for Object Recognition at Ocado


## Installation

### 1. Installing Anaconda 

[What is Anaconda?](https://www.anaconda.com/what-is-anaconda/)

I choose Anaconda for 2 reasons. 

1. Anaconda is one of the most popular open source distribution for data science project, 

2. Everybody uses different OS (2 Mac users, 3 Windows, 1 Ubuntu), which, from my experience, can cause troubles, especially installing packages etc when use normal vertualenv (especially for Windows). Anaconda supports all three OS.

Once installed, run

```conda env create -f environment.yaml``` 

where "venv" is the name of your vertual environment (you could call it whatever you like). 

To get into the vertual environment, run 

```source activate venv``` 

(This command could be different depending on your OS)

This environment is different from your local computer. 

Make sure you are using python3 (not python2) in this environment by running

```python --version ```

If not, try 

```conda create -n py3 python=3 ```


## Git workflow

Our branching workflow is as follow.

- ```master``` Fully working model. 
    
    E.g if this project was a E-commerce website, this codebase is live-working website, and what users interact with.

- ```product``` Fully working model, but not live. 


- ```features/XXX``` features branches, where everyone does real development here 

### Branching and pull requests rules

1. When you are assigned a issue, create a new branch from ```product``` branch (never from ```master```), and do your work.

    - When you make a branch from ```product```, make sure to start the name with ```features/XXX``` where XXX is the name of the issue you are working with (e.g ```features/image_argumentation``` )

2. When you have finished your task/issue, make a pull request to ```product```. 
    - When you do it, make sure to always refer to which issue you've done on the pull request comment (e.g "Resolve #11 Update a final layer ", where #11 is the issue No.).

3. Usually Ong and Kiyo have to do reviews for all pull requests. If the pull request looks okay, Kiyo or Ong merge it into ```product```. 
    - Make sure to delete the branch and close the issue/update the issue board after the merging.

### Warning 

- Usually no one does any direct changes on any code on ```master``` and ```product``` branches. These two branches will be updated only by merging by Kiyo or Ong.

- In case we've found a bug on ```product``` (which means Kiyo or Ong's mistakes), we can fix the bug on ```product``` branch.

- ```master``` has to be always error-free and we can show our project to anyone at anytime.

## Coding Style Guide

TBD

This is too obvious, but please make your code readable (leave comments, better variables names), because other people will read your code. 

### Linter

Run Pep 8

[Online version](http://pep8online.com/)

## Folder Structures

I took the idea from [this post](https://www.kaggle.com/general/4815#25562). We might adjust it slightly as we make progress.

```/analysis``` 

    - All quick analysis/initial experiments are done, and this directory is sparated from our project codebase.

```/download``` 

    - downloaded data only (No augumented/manipulated data).

```/features``` 

    - features fed to classifier.


```/logs``` 

    - Keep all the loggings in here (logging is what you see on your command line when you are executing the program/training the model)

    - We might not do this, but we will experiment

```/src``` 

    - Do we need this???



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
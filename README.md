# Deep Learning using Synthetic Data for Product Recognition

## About the project

[Ocado](https://www.ocado.com) is an online supermarket delivering groceries to customers across the UK. Their warehouses are heavily automated to fulfill more than 250,000 orders a week from a range of over 50,000 products. However, not all parts of the warehouse are automated, and still requires manual labour and barcode scanners to recognise the products, and Ocado is interested in any new methods to speed up this process. 
The goal of the project is to deliver a machine learning system that can classify images of Ocado products in a range of environments.

Our approach is to generate 3D training images using the pipeline we developed, which consists of the following main components.

- Rendering API 
- Training pipeline
- Evaluation
- Flask server
- iPhone App

**The full report of the project can be found [here](https://www.imperial.ac.uk/media/imperial-college/faculty-of-engineering/computing/public/1718-pg-projects/Group2-Machine-Learning-for-Product-Recognition.pdf)**

**The short demo video can be found [here](https://vimeo.com/277194444)**

This project was conducted for  [Software Engineering Practice and Group project (CO 530)](http://www.imperial.ac.uk/computing/current-students/courses/530/), MSc in Computing Science at [Imperial College London](http://www.imperial.ac.uk/computing/), and was awarded for ["Corporate Partnership Programme Commendation for Group Project"](http://www.imperial.ac.uk/computing/prospective-students/distinguished-projects/pg-prizes/?fbclid=IwAR16XMDbC5tJ3HAAf6oe8k35TJ1aPFmWRJLwyLLnDBMYJ0lbBTR8qp60WRs).
### Production Recognition (Classification)
![](/demo_images/classification.gif)

### Production Recognition (Detection)
![](/demo_images/detection.gif)

## Design Choices

### Standard Pipeline Design vs Custom Pipeline Design
Under the standard design that is applied to most deep learning projects, a pre-existing data set would be used to train a neural network, which would then be evaluated and optimised.

![](/demo_images/standard_pipeline.png)

While the standard pipeline works well when a high-quality data set is available, given the challenges described above inherent in the data set we were provided with, the standard pipeline designed was not considered to be a viable option.

Specifically, instead of training a neural network on a pre-existing data set, we decided to generate our own data and to curate our own data set using 3D modelling and Image Rendering techniques.

![](/demo_images/custom_pipeline.png)

### Image Rendering
An interface between the generated 3D models and the input to the neural network was also necessary, using 3D models as the direct input to a classifier is is highly complex and would not achieve our goal of producing a scalable system for classifying 2D images. 
<p align="center">
  <img src="/demo_images/rendering_diagram.png">
</p>

We developed an image rendering system that would take a 3D model as its input and produce a set of training images as its output, given a number of rendering parameters θ as shown in the figure above. The system would use the 3D model to produce multiple images showcasing the modelled product from all possible viewpoints, at different scale, under various lighting conditions, with different amounts of occlusion and with varying backgrounds.

A classifier trained on such generated data is expected to be robust to varying backgrounds, light conditions, occlusion, scale and pose. Furthermore, it allows the user to tailor the training set to a particular environment for which the image classifier will be deployed.

### Final System Design
Our final system design shown in the figure below incorporated the key design choices describe above. These resulted in a custom neural network pipeline which goes from generation of 3D models to a customised evaluation suite used to optimise classification accuracy.

<p align="center">
  <img src="/demo_images/system_design.png">
</p>

The individual component functionality is outlined as follows.

- **Data Generation**: provides 3D models of 10 products in .obj format. These models include textures and colour representations of the product and have to be of high enough quality to produce realistic product images in the next stage.
- **Data Processing (Image Rendering)**: produces a specified number of training images for each product which vary product pose, lighting, background and occlusions. The type of background can be specified by the user. Both the rendered product and a background from a database are combined to create a unique training image in .jpeg format.
- **Neural Network**: the produced images are fed into a pre-trained convolutional neural network. The resulting retrained classifier should be able to classify real product images. 
- **Evaluation and Optimisation**: the outlined approach to training data generation means that the training data can be tailored based on results. Therefore, a custom evaluation and optimization suite is required that is not provided in sufficient in detail in off-the-shelf solutions.

## Installation & Dependencies

### Activate correct CUDA version to link TF to GPU
create a file in your home directory called .bash_profile with content and save:

```
if [ -f /vol/cuda/8.0.61-cudnn.7.0.2/setup.sh ]
then
   . /vol/cuda/8.0.61-cudnn.7.0.2/setup.sh
fi
```
(The above code is for Imperial Collge London Lab PC environment)


then log out and log in again or restart bash.

### Create Virtual Environment

The first step is to install *virtualenv*.

```pip install virtualenv```

The next is to initialise the virtual environment with 

```virtualenv -p python3 venv```

Get into the virtualenv

```source venv/bin/activate```

Install all the dependencies within the virtual environment.

```pip install -r requirements.txt```

### How to run each program

### Integrated Pipeline: main.py

provide paths to validation and test set, currently pointing to the example
folders provided with this repository.

provide the path to your blender installation in 
```bl_path = 'PATH/TO/BLENDER/INSTALLATION'```

Choose all parameters in main.py for rendering and neural network training,
save and run
```
$python main.py
```

### Rendering API

README can be found in  `/src/rendering`.

### Training and Evaluation

README can be found in  `/kerasmodels`.

### iPhone App

README can be found in  `/iPhone_app`.

### Flask

README can be found in  `/flask_webserver`.


## Project Team Members <a name="project-team-members"></a>

Should you have any questions regarding how to run the above, please contact one of the project team members.

* [kk3317](https://gitlab.doc.ic.ac.uk/kk3317) -
**Kiyohito Kunii** &lt;kk3317@imperial.ac.uk&gt;
* [mzw17](https://gitlab.doc.ic.ac.uk/mzw17) -
**Max Baylis** &lt;mzw17@imperial.ac.uk&gt;
* [mgb17](https://gitlab.doc.ic.ac.uk/mgb17) -
**Matthew Wong** &lt;mgb@imperial.ac.uk&gt;
* [who11](https://gitlab.doc.ic.ac.uk/who11) -
**Ong Wai Hong** &lt;who11@imperial.ac.uk&gt;
* [pk3014](https://gitlab.doc.ic.ac.uk/pk3014) -
**Pavel Kroupa** &lt;pk3014@imperial.ac.uk&gt;
* [sk5317](https://gitlab.doc.ic.ac.uk/sk5317) -
**Swen Koller** &lt;sk5317@imperial.ac.uk&gt;


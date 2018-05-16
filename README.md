# Machine Learnig for Product Recognition at Ocado

## Note for the coursework submission
Since .git file was more than 300MB, we excluded it in order to meet the CATE submission limit. We can provide the .git file for the assessment purpose if requested.

## About the project

[Ocado](https://www.ocado.com) is an online supermarket delivering groceries to customers across the UK. Their warehouses are heavily automated to fulfill more than 250,000 orders a week from a range of over 50,000 products. However, not all parts of the warehouse are automated, and still requires manual labour and barcode scanners to recognise the products, and Ocado is interested in any new methods to speed up this process. 

The goal of the project is to deliver a machine learning system that can classify images of Ocado products in a range of environments.

Our approach is to generate 3D training images using the pipeline we developed, which consists of the following main components.

- Rendering API 
- Training pipeline
- Evaluation
- Flask server
- iPhone App

This project is conducted for  [Software Engineering Practice and Group project (CO 530)](http://www.imperial.ac.uk/computing/current-students/courses/530/), MSc in Computing Science at [Imperial College London](http://www.imperial.ac.uk/computing/).

**The full report of the project can be found [here](XX)**


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


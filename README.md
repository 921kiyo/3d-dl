# Machine Learnig for Product Recognition at Ocado

# Table of Contents

TODO Links to each section 
* [About the project](#about)
* [Installation & Dependencies](#release-types)
* [How to run](#building-nodejs)
* [Project Team Members](#project-team-members)

<!-- ## Another paragraph <a name="about"></a> -->

## About the project <a name="paragraph2"></a>

[Ocado](https://www.ocado.com) is an online supermarket delivering groceries to customers across the UK. Their warehouses are heavily automated to fulfill more than 250,000 orders a week from a range of over 50,000 products. However, not all parts of the warehouse are automated, and still requires manual labour and barcode scanners to recognise the products, and Ocado is interested in any new methods to speed up this process. 

The goal of the project is to deliver a machine learning system that can classify images of Ocado products in a range of environments.

Our approach is to generate 3D training images using the pipeline we developed, which consists of the following main components.

- 
- 
- 
- 


This project is conducted for  [Software Engineering Practice and Group project (CO 530)](http://www.imperial.ac.uk/computing/current-students/courses/530/), MSc in Computing Science at [Imperial College London](http://www.imperial.ac.uk/computing/).

**The full report of the project can be found [here](XX)**

## Folder Structures


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

```virtualenv venv (name of virtualenv)```

Get into the virtualenv

```source venv/bin/activate```

Install all the dependencies within the virtual environment.

```pip install -r requirements.txt```

### How to run each program

### Rendering 

Refer to PAVEl README

### Training pipeline

Refer to SWEN README

### iPhone App

Refer to MATTHEW README

### Flask

Refer to MATTHEW README

### Evaluation

Refer to KIYO README

## Technology used

- The code is tested with Python 3.5
- Blender API 
- Agisoft


## Project Team Members <a name="project-team-members"></a>


<!-- * [watilde](https://github.com/watilde) -
**Daijiro Wachi** &lt;daijiro.wachi@gmail.com&gt; (he/him) -->
* [xxx](https://github.com/XXX) -
**Kiyohito Kunii** &lt;XX@imperial.ac.uk&gt;
* [xxx](https://github.com/XXX) -
**Max Baylis** &lt;XX@imperial.ac.uk&gt;
* [xxx](https://github.com/XXX) -
**Matthew Wong** &lt;XX@imperial.ac.uk&gt;
* [xxx](https://github.com/XXX) -
**Ong Wai Hong** &lt;XX@imperial.ac.uk&gt;
* [xxx](https://github.com/XXX) -
**Pavel Kroupa** &lt;XX@imperial.ac.uk&gt;
* [xxx](https://github.com/XXX) -
**Swen Koller** &lt;XX@imperial.ac.uk&gt;
<!-- 
## Contributing to Node.js

* [Contributing to the project][]
* [Working Groups][]
* [Strategic Initiatives][]

[Code of Conduct]: https://github.com/nodejs/admin/blob/master/CODE_OF_CONDUCT.md
[Contributing to the project]: CONTRIBUTING.md
[Node.js Help]: https://github.com/nodejs/help
[Node.js Website]: https://nodejs.org/en/
[Questions tagged 'node.js' on StackOverflow]: https://stackoverflow.com/questions/tagged/node.js
[Working Groups]: https://github.com/nodejs/TSC/blob/master/WORKING_GROUPS.md
[Strategic Initiatives]: https://github.com/nodejs/TSC/blob/master/Strategic-Initiatives.md
[#node.js channel on chat.freenode.net]: https://webchat.freenode.net?channels=node.js&uio=d4 -->
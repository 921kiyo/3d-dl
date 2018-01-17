# Intro
- need to setup a virtualenv, then install all tools within the venv
- cannot install anaconda

# Setting up Venv

Create a virtual environment for a project:
```
$ cd [Project Folder]
$ virtualenv ocadovenv
```

Switch to Python 3.5 in venv
```
$ virtualenv -p /usr/bin/python3.5 ocadovenv
```

begin using the virtual environment:
```
$ source ocadovenv/bin/activate
```

Install all packages:
(done manually, tensorflow-gpu, matplotlib)

exit venv:
```
$ deactivate
```

# use created venv
```
$ cd /vol/project/2017/530/g1753002
$ virtualenv ocadovenv
```

# product dataset link
```
/vol/project/2017/530/g1753002/product-image-dataset
```

# activating ocado venv
venv is installed in group folder
```
. /vol/project/2017/530/g1753002/ocado/ocadovenv/bin/activate
```

(to be tested)

# Introduction to Rendering

Rendering module contains all necessary libraries for the rendering of training images. It was designed to be operatable
froms single script render_pipeline.py. All rendering parameters can be specified through a parameter dictionary that 
is defined in the render_pipeline.py. See the script for more details.

# Dependencies
Blender (and its python interface) 
- Free and Open source 3D creation software https://www.blender.org/
- Install Blender and add the path to the blender executable to the environmental variables.
    - e.g. EV: blender
    - path: D:\Blender_Foundation\Blender\blender.exe 
- Also necessary to set the blender path in the render_pipeline.py
    - bl_path needs to point to  D:\Blender_Foundation\Blender\blender (notice the missing .exe)
Slack (For sending rendering logs to Slack for longer jobs )
- Currently disabled so not necessary
- Enable by going to SlackReporter.py and changing 
    - self.disable = True into self.disable = disable
- This will allow the rendering process to report any termination (both error and succesfull) into a Slack channel
- Need to set envirovnmental variable SLACK_WEBHOOK_URL to an url linked to your channel
    - see https://api.slack.com/incoming-webhooks for further details






# Libraries
There are more details in each library readme.

## BlenderAPI

A wrapper around the Blender native bp interface for easier manipulation. 
Provides a way of adding and manipulating objects in a Blender scene.

## RandomLib

Provides all functions providing some higher level randomisation. Source of random parameters for BlenderAPI.
The random colour mesh backgrounds are generated through metaballs implemented in this library.

## SceneLib

Contains functionality necessary for creation of the final scene.
Functions that prepare a database of valid background images by rescaling them to requested size.
Functions to merge RGBA poses with background image from the database. 

## Testpackages

Contains UT for all the other packages.




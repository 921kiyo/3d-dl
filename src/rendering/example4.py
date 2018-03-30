"""
This example script shows how to use the RenderInterface to control
rendering parameters and produce rendering results
"""

import RenderInterface as Render
num_images = 100
""" ************* User specified stuff here ************* """
# required file paths for the script to run
obj_path = '/vol/project/2017/530/g1753002/3DModels/Halloumi/Halloumi.obj'
texture_path = '/vol/project/2017/530/g1753002/3DModels/Halloumi/Halloumi.jpg'
render_folder = '/vol/project/2017/530/g1753002/3DModels/Halloumi/render'

"""
Rendering with default parameters
RenderInterface has a BlenderRandomScene obejct that controls
random variables responsible for the scene. These random variables
have distributions associated with them. Here we show how to render
with the default distributions
"""
RI = Render.RenderInterface(num_images=num_images)
RI.load_subject(obj_path, texture_path, render_folder)
#RI.render_all(dump_logs = True)

"""
Setting distribution parameters.
One can change the distribution parameters of certain attributes
in the rendering engine. This involves specifying the attribute
that needs to be adjusted (as long as the attribute exists) and
then specifying the parameter to tune.

For instance num_lamps is varied according to the continuous
uniform distribution U[l,r]. This makes l and r (the upper and lower
bount of the U-distibution) tunable parameters
For lamp energy, this is a truncated normal with parameters:
{mu: mean, sigmu: sigma/mu, l: lower bound, r: upper bound}
amd any of these can be tuned.
"""
RI.set_attribute_distribution_params('num_lamps','l',5)
RI.set_attribute_distribution_params('num_lamps','r',8)
RI.set_attribute_distribution_params('lamp_energy','mu',500.0)
RI.set_attribute_distribution_params('lamp_size','mu',5.)
RI.set_attribute_distribution_params('camera_radius','sigmu',0.1)
#RI.render_all()

"""
You could also change the distribution of an attribute entirely, by
giving it a distribution name. This will be one of the distributions
specified in RandomLib/random_render.py
The function signature is as follows:
RI.set_attribute_distribution(attr_name, dist=dist_name, kwargs)
Where kwargs is a keyword argument dict of the required parameters
for each distribution
"""
RI.set_attribute_distribution('lamp_energy',{'dist':'UniformD','l':2000.0,'r':2400.0})
RI.set_attribute_distribution_params('camera_loc','normals','XZ')
RI.set_attribute_distribution_params('camera_loc','phi_sigma',20.0)
RI.render_all(dump_logs=True, visualize=True)

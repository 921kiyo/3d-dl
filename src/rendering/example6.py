"""
This example script demonstrates the use of loading from model files
"""
import RenderInterface as Render
num_images = 10
""" ************* User specified stuff here ************* """

'''
Quick introduction to the .model format:
- it is essentially and archive file of type zip
- needs to contain obj  and jpg files for either one or two models
- for one model, exactly one obj and one jpg file of any name needs
  to be included
- for two models exactly two obj files named "Top.obj" and "Bot.obj"
  as well as two texture files named "Top.jpg" and "Bot.jpg" need to
  be included
'''

RI = Render.RenderInterface(num_images=num_images)

RI.set_attribute_distribution_params('num_lamps','l',5)
RI.set_attribute_distribution_params('num_lamps','r',8)
RI.set_attribute_distribution_params('lamp_energy','mu',500.0)
RI.set_attribute_distribution_params('lamp_size','mu',5.)
RI.set_attribute_distribution_params('camera_radius','sigmu',0.1)

'''
example of a double - view model:
this model file contains a top view and a bottom view obj and jpg files
'''
model_path = '/vol/project/2017/530/g1753002/3DModels/model_format_files/Coconut/Coconut.model'
render_folder = '/vol/project/2017/530/g1753002/3DModels/model_format_files/Coconut/render'
RI.load_from_model(model_path, render_folder)
RI.render_all(dump_logs=True, visualize=False)

'''
example of a single - view model:
this model file contains single view obj and jpg files
'''
model_path = '/vol/project/2017/530/g1753002/3DModels/model_format_files/Liberte/Liberte.model'
render_folder = '/vol/project/2017/530/g1753002/3DModels/model_format_files/Liberte/render'
RI.load_from_model(model_path, render_folder)
RI.render_all(dump_logs=True, visualize=False)

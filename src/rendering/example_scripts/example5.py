"""
This example script shows how to use the RenderInterface with two subject models
"""
import src.rendering.RenderInterface as Render
num_images = 10
""" ************* User specified stuff here ************* """

"""subject top model"""
obj_path = '/vol/project/2017/530/g1753002/3DModels/LiberteTop/LiberteTop.obj'
texture_path = '/vol/project/2017/530/g1753002/3DModels/LiberteTop/LiberteTop.jpg'
"""subject bottom model"""
obj_path_bot = '/vol/project/2017/530/g1753002/3DModels/LiberteBot/LiberteBot.obj'
texture_path_bot = '/vol/project/2017/530/g1753002/3DModels/LiberteBot/LiberteBot.jpg'
render_folder = '/vol/project/2017/530/g1753002/3DModels/Liberte/render'

RI = Render.RenderInterface(num_images=num_images)

RI.set_attribute_distribution_params('num_lamps','l',5)
RI.set_attribute_distribution_params('num_lamps','r',8)
RI.set_attribute_distribution_params('lamp_energy','mu',500.0)
RI.set_attribute_distribution_params('lamp_size','mu',5.)
RI.set_attribute_distribution_params('camera_radius','sigmu',0.1)

RI.load_subjects(obj_path, texture_path, obj_path_bot, texture_path_bot, render_folder)
RI.render_all(dump_logs=True, visualize=True)

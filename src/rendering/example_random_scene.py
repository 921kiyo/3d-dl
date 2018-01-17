"""
This example script creates a box in the middle of a half room
"""

import sys
import random
import math

boop = 'D:/PycharmProjects/Lobster/src/rendering'

if not (boop in sys.path):
	sys.path.append(boop)

import BlenderObjects as bo

radius = 7.0

pl0 = bo.BlenderPlane(location=(-radius,0,0),scale=(radius,radius,radius), orientation=(90,0,1,0))
pl1 = bo.BlenderPlane(location=(0,radius,0),scale=(radius,radius,radius), orientation=(90,1,0,0))
pl2 = bo.BlenderPlane(location=(0,0,-radius),scale=(radius,radius,radius))
pl3 = bo.BlenderPlane(location=(radius,0,0),scale=(radius,radius,radius), orientation=(90,0,1,0))
pl4 = bo.BlenderPlane(location=(0,-radius,0),scale=(radius,radius,radius), orientation=(90,1,0,0))
pl5 = bo.BlenderPlane(location=(0,0,radius),scale=(radius,radius,radius))

pl0.set_diffuse_color(*bo.random_color())
pl1.set_diffuse_color(*bo.random_color())
pl2.set_diffuse_color(*bo.random_color())
pl3.set_diffuse_color(*bo.random_color())
pl4.set_diffuse_color(*bo.random_color())
pl5.set_diffuse_color(*bo.random_color())

cam = bo.BlenderCamera(bpy.data.objects[0])
cube = bo.BlenderCube(bpy.data.objects[1])

theta = math.radians(random.uniform(0.0,360.0))
phi = math.radians(random.uniform(0.0,360.0))
x = radius*math.cos(theta)*math.sin(phi)
y = radius*math.sin(theta)*math.sin(phi)
z = radius*math.cos(phi)

cam.set_location((x,y,z))

x = min(random.gauss(0.0,1.0), 4.0)
y = min(random.gauss(0.0,1.0), 4.0)
z = min(random.gauss(0.0,1.0), 4.0)

cube.set_location((x,y,z))

cam.face_towards(x,y,z)
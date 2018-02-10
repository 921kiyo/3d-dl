"""
This example script creates a box in the middle of a half room
"""


import sys
boop = 'D:\\PycharmProjects\\Lobster\\src\\rendering\\BlenderAPI'

bpy.context.scene.render.engine = 'CYCLES'

if not (boop in sys.path):
	sys.path.append(boop)


import BlenderAPI as bld

cube = bld.BlenderCube(reference=bpy.data.objects['Cube'])

# add 3 BlenderPlanes at different locations and orientations to get a half room
pl0 = bo.BlenderPlane(location=(-5,0,0),scale=(5,5,5), orientation=(90,0,1,0))
pl1 = bo.BlenderPlane(location=(0,5,0),scale=(5,5,5), orientation=(90,1,0,0))
pl2 = bo.BlenderPlane(location=(0,0,-5),scale=(5,5,5))
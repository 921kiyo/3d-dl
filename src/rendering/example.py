"""
This example script creates a box in the middle of a half room
"""

import sys
boop = 'D:/PycharmProjects/Lobster/src/rendering'

if not (boop in sys.path):
	sys.path.append(boop)

import BlenderObjects as bo

pl0 = bo.BlenderPlane(location=(-3,0,0),scale=(3,3,3), orientation=(90,0,1,0))
pl1 = bo.BlenderPlane(location=(0,3,0),scale=(3,3,3), orientation=(90,1,0,0))
pl2 = bo.BlenderPlane(location=(0,0,-3),scale=(3,3,3))
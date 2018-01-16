import bpy
import math
import mathutils as mathU

class BlenderObject(object):
	def __init__(self, location=(0,0,0), orientation=(0,0,0,0), scale=(1,1,1)):
		self.blender_create_operation(location)
		self.reference = bpy.context.active_object
		self.set_rot(*orientation)
		self.set_scale(scale)
	
	def blender_create_operation(self, location, orientation):
		raise NotImplementedError
	
	def set_location(self, location):
		self.reference.location = location
	
	def set_scale(self, scale):
		self.reference.scale = scale
	
	def set_rot(self, w,x,y,z):
		self.reference.rotation_mode = 'QUATERNION'
		m = math.sqrt(x**2 + y**2 + z**2)
		w = math.pi*w/180.0
		if (m==0):
			q = [0,0,0,0]
		else:
			q = mathU.Quaternion([x/m, y/m, z/m], w)
		self.reference.rotation_quaternion = q
	
	def delete(self):
		self.blender_delete_operation()
	
	def blender_delete_operation(self):
		# deselect all
		bpy.ops.object.select_all(action='DESELECT')
		# selection
		self.reference.select = True
		# remove it
		bpy.ops.object.delete() 

class BlenderCube(BlenderObject):
	def __init__(self, location=(0,0,0), orientation=(0,0,0,0), scale=(1,1,1)):
		super(BlenderCube, self).__init__(location, orientation,scale)
	
	def blender_create_operation(self,location):
		bpy.ops.mesh.primitive_cube_add(location=location)

class BlenderPlane(BlenderObject):
	def __init__(self, location=(0,0,0), orientation=(0,0,0,0), scale=(1,1,1)):
		super(BlenderPlane, self).__init__(location, orientation, scale)
	
	def blender_create_operation(self,location):
		bpy.ops.mesh.primitive_plane_add(location=location)
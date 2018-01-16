import bpy

class BlenderObject(object):
	def __init__(self, location=(0,0,0), orientation=(0,0,0), scale=(1,1,1)):
		self.blender_create_operation(location, orientation)
		self.reference = bpy.context.active_object
		self.set_scale(scale)
	
	def blender_create_operation(self, location, orientation):
		raise NotImplementedError
	
	def set_location(self, location):
		self.reference.location = location
	
	def set_scale(self, scale):
		self.reference.scale = scale
	
	''' TODO: figure this out! '''
	def set_rot(self, orientation):
		self.reference.rotation_quaternion = orientation
	
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
	def __init__(self, location=(0,0,0), orientation=(0,0,0), scale=(1,1,1)):
		super(BlenderCube, self).__init__(location, orientation,scale)
	
	def blender_create_operation(self,location, orientation):
		bpy.ops.mesh.primitive_cube_add(location=location, rotation=orientation)

class BlenderPlane(BlenderObject):
	def __init__(self, location=(0,0,0), orientation=(0,0,0), scale=(1,1,1)):
		super(BlenderPlane, self).__init__(location, orientation, scale)
	
	def blender_create_operation(self,location, orientation):
		bpy.ops.mesh.primitive_plane_add(location=location, rotation=orientation)
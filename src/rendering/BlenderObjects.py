import bpy
import math
import random
import mathutils as mathU

def random_color():
	return(random.random(), random.random(), random.random())

def rotate(vector, quaternion):
	vecternion = mathU.Quaternion([0,vector[0],vector[1],vector[2]])
	quanjugate = quaternion.copy()
	quanjugate.conjugate()
	return quaternion*vecternion*quanjugate

def to_quaternion(w,x,y,z):
	m = math.sqrt(x**2 + y**2 + z**2)
	w = math.pi*w/180.0
	if (m==0):
		q = [0,0,0,0]
	else:
		q = mathU.Quaternion([x/m, y/m, z/m], w)
	return q
	
class BlenderObject(object):
	def __init__(self, location=(0,0,0), orientation=(0,0,0,0), scale=(1,1,1), reference=None):
		if reference is None:
			self.blender_create_operation(location)
			self.reference = bpy.context.active_object
		else:
			self.reference=reference
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
		q = to_quaternion(w,x,y,z)
		self.reference.rotation_quaternion = q
	
	def rotate(self, w,x,y,z):
		self.reference.rotation_mode = 'QUATERNION'
		q = to_quaternion(w,x,y,z)
		q = q*self.reference.rotation_quaternion
		print(q)
		self.reference.rotation_quaternion = q
	
	def set_diffuse_color(self,r,g,b):
		obj_name = self.reference.name
		if(len(self.reference.data.materials)==0):
			mat = bpy.data.materials.new(name="Mat"+"_"+obj_name) #set new material to variable
			self.reference.data.materials.append(mat) #add the material to the object
		self.reference.data.materials[0].diffuse_color = (r, g, b) #change color
	
	
	def delete(self):
		# deselect all
		bpy.ops.object.select_all(action='DESELECT')
		# selection
		self.reference.select = True
		# remove it
		bpy.ops.object.delete() 

class BlenderCube(BlenderObject):
	def __init__(self, **kwargs):
		super(BlenderCube, self).__init__(**kwargs)
	
	def blender_create_operation(self,location):
		bpy.ops.mesh.primitive_cube_add(location=location)

class BlenderPlane(BlenderObject):
	def __init__(self, **kwargs):
		super(BlenderPlane, self).__init__(**kwargs)
	
	def blender_create_operation(self,location):
		bpy.ops.mesh.primitive_plane_add(location=location)

class BlenderCamera(BlenderObject):
	def __init__(self, reference, **kwargs):
		super(BlenderCamera, self).__init__(reference=reference, **kwargs)
	
	def face_towards(self,x,y,z):
		# vector of target w.r.t camera
		target = mathU.Vector([x,y,z]) - mathU.Vector(self.reference.location)
		target.normalize()
		# rotational origin of camera is (0,0,-1) for some reason
		rot_origin = mathU.Vector([0,0,-1])
		rot_origin.normalize()
		# get the rotational axis and angle by crossing the two vectors
		rot_axis = rot_origin.cross(target)
		rot_angle = math.degrees(math.acos(rot_origin.dot(target)))
		# set rotation quaternion
		self.set_rot(rot_angle, rot_axis[0], rot_axis[1], rot_axis[2])
		
	

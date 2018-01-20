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

def random_shell_coords(radius):
	theta = math.radians(random.uniform(0.0,360.0))
	phi = math.radians(random.uniform(0.0,360.0))
	x = radius*math.cos(theta)*math.sin(phi)
	y = radius*math.sin(theta)*math.sin(phi)
	z = radius*math.cos(phi)
	return x,y,z
	
def random_cartesian_coords(mux, muy, muz, sigma, lim):
	x = min(random.gauss(mux,sigma), lim)
	y = min(random.gauss(muy,sigma), lim)
	z = min(random.gauss(muz,sigma), lim)
	return x,y,z
	
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

class BlenderLamp(BlenderObject):
	def __init__(self, obj_reference, obj_data):
		super(BlenderLamp, self).__init__(reference=obj_reference)
		self.data = obj_data
	
	def set_brightness(self,strength):
		self.data.use_nodes = True
		self.data.node_tree.nodes["Emission"].inputs["Strength"].default_value = strength

class BlenderRoom(object):
	def __init__(self,radius):
		self.walls = []
		self.walls.append(BlenderPlane(location=(-radius,0,0),scale=(radius,radius,radius), orientation=(90,0,1,0)) )
		self.walls.append(BlenderPlane(location=(0,radius,0),scale=(radius,radius,radius), orientation=(90,1,0,0)) )
		self.walls.append(BlenderPlane(location=(0,0,-radius),scale=(radius,radius,radius)) )
		self.walls.append(BlenderPlane(location=(radius,0,0),scale=(radius,radius,radius), orientation=(90,0,1,0)) )
		self.walls.append(BlenderPlane(location=(0,-radius,0),scale=(radius,radius,radius), orientation=(90,1,0,0)) )
		self.walls.append(BlenderPlane(location=(0,0,radius),scale=(radius,radius,radius)) )
		
	def assign_random_colors(self):
		for wall in self.walls:
			wall.set_diffuse_color(*random_color())
	
	def delete(self):
		for wall in self.walls:
			wall.delete()
		self.walls = [] # drop deleted references
	
		
class BlenderScene(object):
	def __init__(self, data):
		self.lamp = None
		self.background = None
		self.objects_fixed = []
		self.objects_unfixed = []
		self.camera = None
		self.subject = None
		self.data = data

	def add_background(self,background):
		self.background = background
	
	def add_camera(self,camera):
		self.camera = camera
		
	def add_subject(self,subject):
		self.subject = subject
	
	def add_object_fixed(self,object):
		self.objects_fixed.append(object)
	
	def add_object_unfixed(self,object):
		self.ojbects_unfixed.append(object)
	
	def add_lamp(self,lamp):
		self.lamp = lamp
	
	def delete_all(self):
		for obj in self.objects_fixed:
			obj.delete()
		for obj in self.objects_unfixed:
			obj.delete()
		self.subject.delete()
		self.objects_fixed = []
		self.objects_unfixed = []
	
	def set_render(self):
		self.data.cycles.max_bounces = 3
		self.data.cycles.min_bounces = 1
		self.data.cycles.transparent_max_bounces = 3
		self.data.cycles.transparent_min_bounces = 1
		self.data.cycles.samples = 64
		self.data.cycles.device = 'GPU'
		self.data.render.tile_x = 512
		self.data.render.tile_y = 512
		self.data.render.resolution_x = 720
		self.data.render.resolution_y = 720
		
import bpy
import math
import random
import mathutils as mathU
import itertools

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

class BlenderNode(object):
	"""
	Generic Node object in Blender, with operations to create node, and reference node inputs and outputs
	via indexing or key name. Node tree must always be given, if reference is given, a BlenderNode
	of that reference type is created
	"""
	def __init__(self, node_tree, type, reference=None):
		"""
		@param node_tree : (Blender Native Object) required, node tree in which this node lives
		@param type : (string) type name of node. ignored if reference provided.
		@param reference : (Blender Native Object) optional, reference to an existing node
		"""
		self.node_tree = node_tree
		self.type=type
		if reference is None:
			self.reference = self.node_tree.nodes.new(type=type)
		else:
			self.reference = reference
	
	def get_input(self,idx):
		if (type(idx) is int) and ( idx > len(self.reference.inputs.keys()) ):
			return None
		if (type(idx) is str) and ( idx not in self.reference.inputs.keys()):
			return None
		return self.reference.inputs[idx]
	
	def get_output(self,idx):
		if (type(idx) is int) and ( idx > len(self.reference.outputs.keys()) ):
			return None
		if (type(idx) is str) and ( idx not in self.reference.outputs.keys()):
			return None
		return self.reference.outputs[idx]
	
	def set_input(self,idx,val):
		input = self.get_input(idx)
		if input is None:
			return False
		input.default_value = val
		return True

class BlenderMixShaderNode(BlenderNode):
	"""
	subclass of BlenderNode object
	Mix Shader nodes take in different shader nodes as inputs and outputs a resulting 
	mixed shader with respect to a mixing factor
	"""
	def __init__(self, node_tree, reference=None):
		super(BlenderMixShaderNode, self).__init__(node_tree,'ShaderNodeMixShader',reference)

	def get_shader1_input(self):
		return self.get_input(1)
	
	def get_shader2_input(self):
		return self.get_input(2)	
	
	def get_shader_output(self):
		return self.get_output('Shader')
	
	def set_fac(self,fac):
		if fac > 1.0:
			fac = 1.0
		self.set_input('Fac',fac)

		
class BlenderMaterialOutputNode(BlenderNode):
	"""
	subclass of BlenderNode object
	Material node takes in a shader node and outputs a surface, used by the rendering
	engine to determine the properties of a material surface
	"""
	def __init__(self, node_tree, reference=None):
		super(BlenderMaterialOutputNode, self).__init__(node_tree,None,reference)

	def get_surface_input(self):
		return self.get_input('Surface')

		
class BlenderDiffuseBSDFNode(BlenderNode):
	"""
	subclass of BlenderNode object
	Describes the diffuse properties of a shading. Can be plugged into a mix shader
	"""
	def __init__(self, node_tree, reference=None):
		super(BlenderDiffuseBSDFNode, self).__init__(node_tree,'ShaderNodeBsdfDiffuse',reference)
	
	def set_color(self,r,g,b,a):
		args = (r,g,b,a)
		for i,arg in enumerate(args):
			if arg > 1.0:
				args[i] = 1.0
		self.set_input('Color',args)
	
	def set_roughness(self, r):
		if r > 1.0:
			r = 1.0
		self.set_input('Roughness',r)
	
	def get_bsdf_output(self):
		return self.get_output('BSDF')
	
	def get_color_input(self):
		return self.get_input('Color')

		
class BlenderGlossyBSDFNode(BlenderNode):
	"""
	subclass of BlenderNode object
	Describes the glossy properties of a shading. Can be plugged into a mix shader
	"""
	def __init__(self, node_tree, reference=None):
		super(BlenderGlossyBSDFNode, self).__init__(node_tree,'ShaderNodeBsdfGlossy',reference)
	
	def set_color(self,r,g,b,a):
		args = (r,g,b,a)
		for i,arg in enumerate(args):
			if arg > 1.0:
				args[i] = 1.0
		self.set_input('Color',args)
	
	def set_roughness(self, r):
		if r > 1.0:
			r = 1.0
		self.set_input('Roughness',r)
	
	def get_bsdf_output(self):
		return self.get_output('BSDF')
	
	def get_color_input(self):
		return self.get_input('Color')

		
class BlenderImageTextureNode(BlenderNode):
	"""
	subclass of BlenderNode
	Outputs a Color based on a Vector mapping for the surface, given an image.
	"""
	def __init__(self, node_tree, reference=None):
		super(BlenderImageTextureNode, self).__init__(node_tree,'ShaderNodeTexImage',reference)
	
	def set_projection(self, projection):
		try:
			self.reference.projection = projection
		except TypeError:
			return False
		return True
		
	def set_image(self, image):
		try:
			self.reference.image = image
		except TypeError:
			return False
		return True
	
	def get_vector_input(self):
		return self.get_input('Vector')
	
	def get_color_output(self):
		return self.get_output('Color')

		
class BlenderTexCoordNode(BlenderNode):
	"""
	subclass of BlenderNode
	Outputs a mapping type (usually 'UV' or 'Generated') to be given to a Texture Node,
	to determine the mapping of the colors onto a surface
	"""
	def __init__(self, node_tree, reference=None):
		super(BlenderTexCoordNode, self).__init__(node_tree,'ShaderNodeTexCoord',reference)
	
	def get_UV_output(self):
		return self.get_output('UV')
		
	def get_Generated_output(self):
		return self.get_output('Generated')

	
class BlenderObject(object):
	"""
	This class is intended as a wrapper for all objects that can be referenced via the
	bpy.data.objects Collection. 
	This includes a number of items like lamps, camera, meshes, assemblies to name a few
	
	This class is an interface to all these objects, and is meant as an abstract class,
	as the blender_create operation is left to the subclass to implement
	
	Also included are concrete implementations of methods that are common to all these
	objects. This mostly include geometric operations like rotation, translation etc.
	
	Also a delete method is implemented
	"""
	def __init__(self, location=(0,0,0), orientation=(0,0,0,0), scale=(1,1,1), reference=None, **kwargs):
		if reference is None:
			bpy.ops.object.select_all(action='DESELECT') # deselect everything
			self.blender_create_operation(location, **kwargs)
			assert len(bpy.context.selected_objects)==1, "more than one selected objects!" 
			# make sure the only selected object is the recently created object
			self.reference = bpy.context.selected_objects[0]
		else:
			self.reference=reference
		self.set_rot(*orientation)
		self.set_scale(scale)
	
	def blender_create_operation(self, location):
		# Attention: for subclass to implement
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
	
	def delete(self):
		# deselect all
		bpy.ops.object.select_all(action='DESELECT')
		# selection
		self.reference.select = True
		# remove it
		bpy.ops.object.delete() 

class BlenderMesh(BlenderObject):
	def __init__(self, **kwargs):
		super(BlenderMesh, self).__init__(**kwargs)
		self.nodes = {}
		self.links = None
		self.node_tree = None
		self.material = None
		self.setup_node_tree()
	
	def setup_node_tree(self):
	
		obj_name = self.reference.name
		if(len(self.reference.data.materials)==0):
			mat = bpy.data.materials.new(name="Mat"+"_"+obj_name) #set new material to variable
			self.reference.data.materials.append(mat) #add the material to the object
		self.material = self.reference.data.materials[0]
		self.reference.data.materials[0].use_nodes = True
		
		self.node_tree = self.material.node_tree
		self.nodes['node_mat'] = BlenderMaterialOutputNode(self.node_tree, reference=self.node_tree.nodes['Material Output'])
		self.nodes['node_diff'] = BlenderDiffuseBSDFNode(self.node_tree, reference=self.node_tree.nodes['Diffuse BSDF'])
		self.nodes['node_gloss'] = BlenderGlossyBSDFNode(self.node_tree)
		self.nodes['node_mix'] = BlenderMixShaderNode(self.node_tree)
		self.links = self.node_tree.links
		self.links.new(self.nodes['node_mix'].get_shader_output(), self.nodes['node_mat'].get_surface_input())
		self.links.new(self.nodes['node_diff'].get_bsdf_output(), self.nodes['node_mix'].get_shader1_input())
		self.links.new(self.nodes['node_gloss'].get_bsdf_output(), self.nodes['node_mix'].get_shader2_input())
	
	def set_diffuse(self,color=(0.5,0.5,0.5,1),rough=0.5):
		self.nodes['node_diff'].set_color(*color)
		self.nodes['node_diff'].set_roughness(rough)
		
	def set_gloss(self,color=(0.5,0.5,0.5,1),rough=0.5):
		self.nodes['node_gloss'].set_color(*color)
		self.nodes['node_gloss'].set_roughness(rough)
	
	def set_mixer(self,factor):
		self.nodes['node_mix'].set_fac(factor)
	
	def add_image_texture(self, image_path, projection='FLAT', mapping ='UV'):
	
		if not 'node_imgtex' in self.nodes.keys():
			self.nodes['node_imgtex'] = BlenderImageTextureNode(self.node_tree)
		if not 'node_texcoord' in self.nodes.keys():
			self.nodes['node_texcoord'] = BlenderTexCoordNode(self.node_tree)
			
		try:
			img = bpy.data.images.load(image_path)
		except:
			return False
		
		success = False
		success = self.nodes['node_imgtex'].set_projection(projection) and self.nodes['node_imgtex'].set_image(img)
		if not success:
			return success
		
		if mapping not in ['UV','Generated']:
			return False
		
		vector = None
		if mapping=='Generated':
			vector = self.nodes['node_texcoord'].get_Generated_output()
		else:
			vector = self.nodes['node_texcoord'].get_UV_output()
		self.links.new(vector, self.nodes['node_imgtex'].get_vector_input())
		self.links.new(self.nodes['node_imgtex'].get_color_output(), self.nodes['node_diff'].get_color_input())
		self.links.new(self.nodes['node_imgtex'].get_color_output(), self.nodes['node_gloss'].get_color_input())
	
	def toggle_smooth(self):
		for poly in self.reference.data.polygons:
			poly.use_smooth = True
		
		
class BlenderCube(BlenderMesh):
	def __init__(self, **kwargs):
		super(BlenderCube, self).__init__(**kwargs)
	
	def blender_create_operation(self,location):
		bpy.ops.mesh.primitive_cube_add(location=location)

class BlenderPlane(BlenderMesh):
	def __init__(self, **kwargs):
		super(BlenderPlane, self).__init__(**kwargs)
	
	def blender_create_operation(self,location):
		bpy.ops.mesh.primitive_plane_add(location=location)

class BlenderImportedShape(BlenderMesh):
	def __init__(self, **kwargs):
		super(BlenderImportedShape, self).__init__(**kwargs)
	
	def blender_create_operation(self,location,obj_path=None):
		assert obj_path is not None, "Required keyword argument for importing shape: obj_path=[filepath]"
		bpy.ops.import_scene.obj(filepath=obj_path)
		
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
	def __init__(self, obj_reference):
		super(BlenderLamp, self).__init__(reference=obj_reference)
		self.data = self.reference.data
	
	def blender_create_operation(self,location):
		bpy.ops.object.lamp_add(location=location)
	
	def set_size(self,size):
		self.data.shadow_soft_size = size
	
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
		self.objects_unfixed.append(object)
	
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
		self.data.cycles.film_transparent = True
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
	
	def render_to_file(self,filepath):
		self.data.render.filepath = filepath
		bpy.ops.render.render( write_still=True )
		
# Introduction to the BlenderAPI

The Blender API is an object-oriented based approach to using the Blender Python Library. In the Blender python library,
Blender is controlled by using the blender python module `bpy`. One does this by importing `bpy` into a python script and
running the script in the Blender environment. This can be done in several ways:
* By launching the Blender GUI, and using the python console. This console already has all the blender runtime libraries
 imported.
* By opening the Blender Editor and running the script in there.
* By running Blender on the console, in the background, and handing it the python script. Note that you will not see the 
graphical interface with this method:
```
    blender --background --python script.py
```

## The bpy module

All of blender can be accssed throught the `bpy` module, by calling `import bpy`.
The most important objects in the `bpy` module are:

* `bpy.data` - this provides an interface to all the data structures that exist in the program. This includes meshes,
cameras, scenes, user settings node trees and many more. The Blender API essentially depends on the `data` API to
manipulate these. For example, if I wanted to change the location of a cube, I would change the cube data structure:

```python
cube = bpy.data.objects['Cube'] # reference the object named 'Cube' in the program
cube.location = (1.0,1.0,1.0) # change location, simple as that
```

* `bpy.ops` - this provides a programmatic way to call Blender operations commonly done via button presses in the GUI. 
 A convenience that's provided is that operations that are associated with certain categories are listed under `bpy.ops.[cat]` 
 , where `[cat]` can be replaced by `object` for object-related operations
```python
bpy.ops.object.select_name('Cube') # select the object named 'Cube' in the program
# by default all operations act on select objects only
bpy.ops.transform.translate((1.0,1.0,1.0)) # perform translation on selected object
```

* `bpy.context` - provides information on data in the current context. It lists only a subset of data such as the 
current scene, the active object etc. This is an easy way to have a script work on whatever object is selected rather 
than having to know it's name beforehand.
```python
# selected is a list of the objects in the current scene that are selected
# any object in this list can be modified via bpy.ops operators
selected = bpy.context.selected_objects
```

This [StackExhange post](https://blender.stackexchange.com/questions/9353/what-is-the-difference-between-items-listed-in-bpy-ops-bpy-data-and-bpy-context)
gives a few more examples of what you can do with the blender python API.

## BlenderAPI

This is what we are building on top of the `bpy` module. Having to reference data in the way Blender constrains users to
do makes it no different from manipulating shapes in the graphical window, except that you can automate tasks more easily.
What BlenderAPI aims to do is to build an OOP layer over the `bpy` module, and make it more pythonic.

One such example is creating a cube. With the BlenderAPI, one could do:
```python
cube = BlenderCube()
cube.set_location((1.0,1.0,1.0))
```

Where `cube` would be a reference to the created object, allowing the user to manipulate in a more natural way.
Compare this with the native approach:
```python
bpy.ops.mesh.primitive_cube_add()
# fetch reference to the first selected object which will always be the created object
cube = bpy.context.selected_objects[0] 
cube.location = (1.0,1.0,1.0) # set cube location
```

Of course, what BlenderAPI really does is call these commands, under the hood.

A quick introduction to the classes available thought BlenderAPI:
### `BlenderObjects`
- Definition:  `BlenderObjects.py`
- Abstract base class to represent all objects that can be referenced via `bpy.data.objects`. These usually includes 
  items in the scene that can be manipulated (meshes, camera, lamps, background etc)
- Classes that subclass this : 
    - `BlenderMesh` -- (`BlenderCube`,  `BlenderPlane`, `BlenderImportedShape`), definition in  `BlenderShapes.py`
    - `BlenderCamera`, definition: `BlenderCamera.py`
    - `BlenderLamp` -- (`BlenderSun`, `BlenderPoint`), definition: `BlenderLamps.py`

### `BlenderNodes`
- Definition : `BlenderNodes.py`
- [This link](https://docs.blender.org/manual/en/dev/render/blender_render/materials/nodes/introduction.html) provides
  an excellent introduction to the idea of material nodes. essentially, it describes it as:      
  _Blender allows you to create a material by routing basic materials through a set of nodes. Each node performs some 
  operation on the material, changing how it will appear when applied to the mesh, and passes it on to the next node._
- Subclasses include nodes that right now are sufficient in capturing most material properties:
    - `BlenderMixShaderNode`, `BlenderDiffuseBSDFNode`, `BlenderGlossyBSDFNode` etc.
  
     
### `BlenderScene`
- Definition: `BlenderScene.py`
- Class to summarize the components within a scene. Right now, it is designed to store information such as, list of
objects in the scene (subjects, objects, lamps and camera(s)), render settings (important), but not much else. 
- This class is still work in progress, but future plans include:
    - Designing the class to manage scene creation (importing all necessary objects to create required scene)
    - Handle background mixing (Important!)
    - Manage random variables that make a scene, right now distributions like camera angles, object scale, material 
    mixing still have to be hand-tweaked in the script. `BlenderScene` should aim to automate this
    - Handle complex operations like managing layers in the scene (optional).

# Introduction to Random Library

The whole rendering process uses a set of non trivial functions which produce
randomized output. All such functions are kept in this library. It also includes
the functionality to generate random colour mesh backgrounds through the use 
of metaballs (which are also product of randomness)

None of these scripts are expected to be run on their own, as they are 
intended and used as helper function for BlenderAPI and SceneLib. For this
reason there is no script provided to run them as so.

## random_render.py
Provides a Class `Distribution` which has a large number of subclasses,
each defining a different distribution.
It provides the following interface
- `sample_param()`: returns one sample sampled from the corresponding distribution
- `give_param()`: returns all the parameters stored for this class instance
- `change_param(param_name, param_value)`: changes parameter of given name to
        given value
        
## metaballs.py random_background.py turbulence.py
Contains all necessary logic to produce a random colour mesh background.
metaballs and turbulence provides helper functions, introducing noise
and metaball coloured patches into the image.

random_background provides an interface which allows generation of final
images. The function `generate_images( save_as,pixels, range_min, range_max)`
provides the main interface. This allows to generate any number 
`(range_max-range_min)` of random background images of given size 
`(pixels*pixels)` and save them into given folder `(save_as)`


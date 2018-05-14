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
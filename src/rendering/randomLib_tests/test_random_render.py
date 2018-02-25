# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 22:19:12 2018

@author: Pavel

Test the functions in file random_render.py
Does not test random_lightning_condition
as that should be tested as part of BlenderAPI
"""


import unittest

import numpy as np
import sys, os
#boop = "D:/old_files/aaaaa/Anglie/imperial/2017-2018/group_project/OcadoLobster/src"

dir_path = os.path.dirname(os.path.realpath(__file__))
parent = os.path.abspath(os.path.join(dir_path, os.pardir))
base_path = os.path.abspath(os.path.join(parent,os.pardir)) # folder /src

if not (base_path in sys.path):
    sys.path.append(base_path)


import rendering.randomLib.random_render as rr

class Testturbulence(unittest.TestCase):
    
    def test_random_color(self):
        """
        Check that random_color returns three values
        Check that the values are between 0 and 1
        """
        rand_color = rr.random_color()

        self.assertEqual(len(rand_color),3)
        for value in rand_color:
            self.assertGreaterEqual(value,0)
            self.assertLessEqual(value,1)
 
    
    def test_random_shell_coord(self):
        """
        Test that for any input radius, the generated points can be found
        on a shell of that radius, centered on (0,0,0)
        Tests for int and float and also for negative radius
        """
        test_values=[2,0,3.5]
        for value in test_values:
            x,y,z = rr.random_shell_coords(value)
            self.assertAlmostEqual(value, np.sqrt(x**2+y**2+z**2))
       
        self.assertRaises(ValueError, rr.random_shell_coords, -5)
        
    def test_random_cartesian_coords_ok(self):
        """
        Tests, the function random_cartesian_coords
        Ensures that the returned coordinates are within the limiting box
        """
        mux = [1.,2.5,-3.,0]
        muy = [3.5,-2,0,15]
        muz = [2.25,-2.0,1.,-0]
        sigma = [2.0,1.1, 0.,15]
        lim = [0.,10,2.3,3]
        i =0
        while i< len(mux):
            x,y,z = rr.random_cartesian_coords(mux[i], muy[i], muz[i], sigma[i], lim[i])
            self.assertLessEqual(x, lim[i]+mux[i])
            self.assertLessEqual(y, lim[i]+muy[i])
            self.assertLessEqual(z, lim[i]+muz[i])
            i+=1
            
            
    def test_random_cartesian_coords_fail(self):
        """
        Tests that an exception is raised when invalid parameters
        are passed in. 
        Invalid parameters are: sigma<0 and lim<0
        """
        
        self.assertRaises(ValueError, rr.random_cartesian_coords, 0,0,1,-5,2)
        self.assertRaises(ValueError, rr.random_cartesian_coords, 0,0,1,5,-2)
        
        
        
if __name__=='__main__':
    unittest.main()

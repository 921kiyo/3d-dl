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


from ..RandomLib import random_render as rr 
from ..RandomLib.random_exceptions import ImprobableError
import itertools as it

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

    def test_random_shell_coords_cons(self):
        """
        Test that for any input radius, the generated points can be found
        on a shell of that radius, centered on (0,0,0)
        Tests for int and float and also for negative radius
        """
        test_radii=[2,0,3.5]
        test_phi_sigma=[10.0, 30.0, 180.0]
        for (r,s) in it.product(test_radii, test_phi_sigma):
            x,y,z = rr.random_shell_coords_cons(r,s)
            self.assertAlmostEqual(r, np.sqrt(x**2+y**2+z**2))

        self.assertRaises(ValueError, rr.random_shell_coords_cons, -5, 30.0)
        self.assertRaises(ValueError, rr.random_shell_coords_cons, 5, -30.0)

    def test_TruncNormDist(self):

        D = rr.TruncNormDist(mu=2.0, sigmu=2.0)

        self.assertEqual(D.mu, 2.0)
        self.assertEqual(D.sigmu, 2.0)

        D = rr.TruncNormDist(mu=3.0, sigmu=5.0)

        self.assertEqual(D.mu, 3.0)
        self.assertEqual(D.sigmu, 5.0)

        self.assertRaises(ValueError, rr.TruncNormDist, mu=-2.0, sigmu=-1.0)
        self.assertRaises(ValueError, rr.TruncNormDist, mu=2.0, sigmu=-1.0)

        D.change_param('mu', 50.0)
        D.change_param('l', 5.0)

        self.assertEqual(D.mu, 50.0)
        self.assertEqual(D.sigmu, 5.0)
        self.assertEqual(D.l, 5.0)
        self.assertEqual(D.r, None)

        D.change_param('mu', 50.0)
        D.change_param('l', 30.0)

        self.assertEqual(D.mu, 50.0)
        self.assertEqual(D.sigmu, 5.0)
        self.assertEqual(D.l, 30.0)
        self.assertEqual(D.r, None)
        
        for i in range(10):
            X = D.sample_param()

        self.assertRaises(ValueError, D.change_param, 'sigmu', -2.0)

        
        # way out of range
        D = rr.TruncNormDist(mu=3.0, sigmu=5.0, l=1e05, r = 5e05)
        self.assertRaises(ImprobableError, D.sample_param)

    def test_NormDist(self):

        D = rr.NormDist(mu=2.0, sigma=2.0)

        self.assertEqual(D.mu, 2.0)
        self.assertEqual(D.sigma, 2.0)

        D = rr.NormDist(mu=-3.0, sigma=5.0)

        self.assertEqual(D.mu, -3.0)
        self.assertEqual(D.sigma, 5.0)

        self.assertRaises(ValueError, rr.NormDist, mu=2.0, sigma=-1.0)

        D.change_param('mu', 50.0)
        D.change_param('sigma', 5.0)

        self.assertEqual(D.mu, 50.0)
        self.assertEqual(D.sigma, 5.0)

        D.change_param('mu', -30.0)
        D.change_param('sigma', 30.0)

        self.assertEqual(D.mu, -30.0)
        self.assertEqual(D.sigma, 30.0)

        for i in range(10):
            X = D.sample_param()

        self.assertRaises(ValueError, D.change_param, 'sigma', -2.0)

        self.assertRaises(KeyError, D.change_param, 'foo','A')

    def test_UniformCDist(self):

        D = rr.UniformCDist(l=2.0, r=3.0)
        self.assertEqual(D.l, 2.0)
        self.assertEqual(D.r, 3.0)

        D = rr.UniformCDist(l=-5.0, r=-3.0)
        self.assertEqual(D.l, -5.0)
        self.assertEqual(D.r, -3.0)

        self.assertRaises(ValueError, rr.UniformCDist, l=2.0, r=1.9)

        D.change_param('l', 5.0)
        D.change_param('r', 6.0)

        self.assertEqual(D.l, 5.0)
        self.assertEqual(D.r, 6.0)

        for i in range(10):
            X = D.sample_param()

        D.change_param('l', 7.0)
        D.change_param('r', 6.9)

        self.assertRaises(ValueError, D.sample_param)

        self.assertRaises(KeyError, D.change_param, 'foo','A')

    def test_UniformDDist(self):

        D = rr.UniformDDist(l=2.0, r=3.0)

        self.assertEqual(D.l, 2.0)
        self.assertEqual(D.r, 3.0)

        D = rr.UniformDDist(l=-5.0, r=-3.0)

        self.assertEqual(D.l, -5.0)
        self.assertEqual(D.r, -3.0)

        self.assertRaises(ValueError, rr.UniformDDist, l=2.0, r=1.9)

        D.change_param('l', 5.0)
        D.change_param('r', 6.0)

        self.assertEqual(D.l, 5.0)
        self.assertEqual(D.r, 6.0)

        for i in range(10):
            X = D.sample_param()

        D.change_param('l', 7.0)
        D.change_param('r', 6.9)

        self.assertRaises(ValueError, D.sample_param)

        self.assertRaises(KeyError, D.change_param, 'foo','A')

    def test_PScaledUniformDDist(self):

        D = rr.PScaledUniformDDist(mid=2.0, scale=1.0)

        self.assertAlmostEqual(D.mid, 2.0)
        self.assertAlmostEqual(D.scale, 1.0)
        self.assertAlmostEqual(D.l, 0.0)
        self.assertAlmostEqual(D.r, 4.0)

        D = rr.PScaledUniformDDist(mid=5.0, scale=0.5)

        self.assertAlmostEqual(D.mid, 5.0)
        self.assertAlmostEqual(D.scale, 0.5)
        self.assertAlmostEqual(D.l, 2)
        self.assertAlmostEqual(D.r, 8)

        self.assertRaises(ValueError, rr.PScaledUniformDDist, mid=-0.1, scale=0.5)
        self.assertRaises(ValueError, rr.PScaledUniformDDist, mid=1.0, scale=1.2)

        D.change_param('mid', 3.0)
        D.change_param('scale', 0.7)

        self.assertAlmostEqual(D.mid, 3.0)
        self.assertAlmostEqual(D.scale, 0.7)
        self.assertAlmostEqual(D.l, 1)
        self.assertAlmostEqual(D.r, 5)

        for i in range(10):
            X = D.sample_param()

        self.assertRaises(ValueError, D.change_param, 'mid', -0.1)
        self.assertRaises(ValueError, D.change_param, 'scale', -0.1)
        self.assertRaises(ValueError, D.change_param, 'scale', 1.1)

        self.assertRaises(KeyError, D.change_param, 'foo','A')

    def test_ShellRingCoordinateDist(self):

        D = rr.ShellRingCoordinateDist(phi_sigma=0.0, normal='X')

        self.assertEqual(D.phi_sigma, 0.0)
        self.assertEqual(D.normal, 'X')
        self.assertEqual(D.phi.sigmu, 0.0)

        D = rr.ShellRingCoordinateDist(phi_sigma=1.0, normal='X')

        self.assertEqual(D.phi_sigma, 1.0)
        self.assertEqual(D.normal, 'X')
        self.assertAlmostEqual(D.phi.sigmu, 1.0/90.0)

        D.change_param('phi_sigma', 3.0)

        self.assertEqual(D.phi_sigma, 3.0)
        self.assertEqual(D.normal, 'X')
        self.assertAlmostEqual(D.phi.sigmu, 3.0/90.0)

        D.change_param('normal', 'Z')

        self.assertEqual(D.phi_sigma, 3.0)
        self.assertEqual(D.normal, 'Z')
        self.assertAlmostEqual(D.phi.sigmu, 3.0/90.0)
        
        for i in range(10):
            X = D.sample_param()

        self.assertRaises(ValueError, D.change_param, 'normal','A')
        self.assertRaises(ValueError, D.change_param, 'phi_sigma',-1.0)

        self.assertRaises(KeyError, D.change_param, 'foo','A')

    def test_CompositeShellRingDist(self):

        D = rr.CompositeShellRingDist(phi_sigma=0.0, normals='XZ')

        self.assertEqual(D.phi_sigma, 0.0)
        self.assertEqual(D.normals, 'XZ')

        X = D.distributions[0]
        Z = D.distributions[1]

        self.assertEqual(X.phi_sigma, 0.0)
        self.assertEqual(X.normal, 'X')
        self.assertEqual(Z.phi_sigma, 0.0)
        self.assertEqual(Z.normal, 'Z')
        self.assertEqual(D.distribution_select.r, 1)
                
        D = rr.CompositeShellRingDist(phi_sigma=1.0, normals='X')
        X = D.distributions[0]

        self.assertEqual(D.phi_sigma, 1.0)
        self.assertEqual(D.normals, 'X')
        self.assertEqual(X.phi_sigma, 1.0)
        self.assertEqual(X.normal, 'X')
        self.assertEqual(D.distribution_select.r, 0)

        D.change_param('phi_sigma', 3.0)

        self.assertEqual(D.phi_sigma, 3.0)
        self.assertEqual(D.normals, 'X')
        self.assertEqual(X.phi_sigma, 3.0)
        self.assertEqual(X.normal, 'X')
        self.assertEqual(D.distribution_select.r, 0)
        
        D.change_param('normals', 'YZ')
        Y = D.distributions[0]
        Z = D.distributions[1]

        self.assertEqual(D.phi_sigma, 3.0)
        self.assertEqual(D.normals, 'YZ')
        self.assertEqual(D.distribution_select.r, 1)
        self.assertEqual(Y.phi_sigma, 3.0)
        self.assertEqual(Y.normal, 'Y')
        self.assertEqual(Z.phi_sigma, 3.0)
        self.assertEqual(Z.normal, 'Z')

        for i in range(10):
            X = D.sample_param()
        
        self.assertRaises(ValueError, D.change_param, 'normals','A')
        self.assertRaises(ValueError, D.change_param, 'phi_sigma',-1.0)

        self.assertRaises(KeyError, D.change_param, 'foo','A')
        
    def test_UniformShellCoordinateDist(self):
        
        D=rr.UniformShellCoordinateDist()
        self.assertEqual(D.theta.l, 0.0)
        self.assertTrue(0.0 <= D.phi.mu <= 180.0)
        self.assertEqual(D.phi.l,0.0)
        x,y,z = D.sample_param()
        self.assertTrue(-1.0<=x<=1.0)
        self.assertTrue(-1.0<=y<=1.0)
        self.assertTrue(-1.0<=z<=1.0)
        
        param = D.give_param()
        self.assertEqual(param,{"dist": "UniformShellCoordinateDist"})        


if __name__=='__main__':
    unittest.main()

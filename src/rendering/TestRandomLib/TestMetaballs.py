# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 19:16:22 2018

@author: Pavel
"""

import unittest

import numpy as np
import os
import sys
#boop = "D:/old_files/aaaaa/Anglie/imperial/2017-2018/group_project/OcadoLobster/src"

dir_path = os.path.dirname(os.path.realpath(__file__))
parent = os.path.abspath(os.path.join(dir_path, os.pardir))
base_path = os.path.abspath(os.path.join(parent,os.pardir)) # folder /src

if not (base_path in sys.path):
    sys.path.append(base_path)


from ..RandomLib import metaballs as mb

class Testturbulence(unittest.TestCase):
    
    def test_norm(self):
        """
        Checking that the norm function works properly for various powers.
        Checked both by
        """
        self.assertAlmostEqual(np.sqrt(41) ,mb.norm(5,4,2))
        self.assertAlmostEqual(np.cbrt(72.248104), mb.norm(2.5,3.84,3))

    def test_ball(self):
        """
        Creates an instance of ball object and tests all of its functions
        Checks that the values are initialised correctly.
        Tests positive and negative ints and floats
        
        Also checks the inverse_distance function, that calculates the
        inverse distance to a given point
        """
        # ball centered at 0,1, with norm 2 with radius 5
        new_ball = mb.ball(5,-1.5,1.,2)
        self.assertEqual(new_ball.radius, 5)
        self.assertEqual(new_ball.x0,-1.5)
        self.assertEqual(new_ball.y0,1.)
        self.assertEqual(new_ball.norm,2)
        inverse = new_ball.inverse_distance(-5,3)
        self.assertAlmostEqual(5./np.sqrt(16.25), inverse)
        
    def test_sum_inverse_ok(self):
        """
        Creates three balls and pass them to sum_inverse
        Also pass an array of values, instead of just one value
        Also tests a negative input as the ball position
        """
        
        x=np.array([1,2])
        y=np.array([3,5])
        all_balls = [mb.ball(3,0,0,2),mb.ball(4,-1,2,2),mb.ball(5,0,1,2)]
        sum_inverse = mb.sum_inverse_distance(x,y,all_balls)
        expected_result=[]
        expected_result.append(3./np.sqrt(10)+4./np.sqrt(5)+5./np.sqrt(5))
        expected_result.append(3/np.sqrt(29)+4./np.sqrt(18)+5./np.sqrt(20))
        self.assertAlmostEqual(sum_inverse[0], expected_result[0])
        self.assertAlmostEqual(sum_inverse[1], expected_result[1])

    def test_sum_inverse_fail(self):
        """
        This function tests that Exception is raised when x and y differ in shape
        
        """
        
        x = np.array([1,2,3])
        y=np.array([1,2])
        all_balls = [mb.ball(2,0,0,2)]
        self.assertRaises(IndexError, mb.sum_inverse_distance,x,y, all_balls)
        
    def test_metaball(self):
        """
        Test function metaball, that creates a single metaball
        As a parameter, the size is used 300*150
        as 300*300 will be the normal use case. 
        However we want to test a more general situation
        
        A metaball should be present so at least one value should be True
        """
        one_ball = mb.ball(4.,-1.,1.,2)
        one_met = mb.metaball(300,150,[one_ball],0.3)
        self.assertEqual(np.shape(one_met)[0],300)
        self.assertEqual(np.shape(one_met)[1],150)
        
        true_count = 0
        for row in one_met:
            for value in row:
                # checks that values are either True or False
                self.assertIn(value,(True, False))
                if(value):
                    true_count +=1
                    
        self.assertGreater(true_count,1)

    def test_random_metaball(self):
        """
        Simillar test to the above, but with passing different parameters
        
        """
        rand_met = mb.random_metaball(100,300,4,0.4)
        self.assertEqual(np.shape(rand_met)[0],100)
        self.assertEqual(np.shape(rand_met)[1],300)
        true_count = 0
        for row in rand_met:
            for value in row:
                # checks that values are either True or False
                self.assertIn(value,(True, False))
                if(value):
                    true_count +=1
        self.assertGreater(true_count,1)

        
 
       
if __name__=='__main__':
    unittest.main()

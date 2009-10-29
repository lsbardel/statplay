import numpy as ny
import rpy2.rinterface as ri
from unittest import TestCase

class Rpy2Test(TestCase):
    
    def setUp(self):
        # Initialized embedded R
        ri.initr()
        
    def testArray(self):
        # Create an array in R domain
        rx = ri.SexpVector([1,2,3,4], ri.INTSXP)
        # Create a local copy in Python domain
        nx = ny.array(rx)
        # Proxy to R vector without coping
        nx_nc = ny.asarray(rx)
        nx[1]    = 9
        nx_nc[1] = 10
        self.assertNotEqual(rx[1],nx[1])
        self.assertNotEqual(nx_nc[1],nx[1])
        self.assertEqual(rx[1],nx_nc[1])
        
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

def check_confidence_tensor(tensor):
    tol = 1e-04
    if (not (np.abs(np.sum(tensor,axis=1)[0]-1.)) < tol) or (np.argmin(tensor, axis=1)[0] < 0):
        return False
    return True

def check_confusion_matrix(cm):
    if (not cm.shape[0]==cm.shape[1]):
        return False
    return True

def check_nonnegative_args(*args):
    for arg in args:
        if arg < 0:
            return False
    return True

class InvalidInputError(Exception):
    def __init__(self, message):
        self.message = message

class InvalidDirectoryStructureError(Exception):
    def __init__(self):
        self.message = "hello world"

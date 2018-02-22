import bpy
import math
import mathutils as mathU
import itertools

def check_is_iter(input, size):
    try:
        input_iter = iter(input)
        return len(input) == size
    except TypeError:
        return False

def check_vector_non_negative(input):
    for item in input:
        if not (item >= 0):
            return False
    return True

def check_scalar_non_negative(input):
    return input >= 0

class InvalidInputError(Exception):
    """
    Error to call when input invalid
    """
    def __init__(self, message):
        self.message = message

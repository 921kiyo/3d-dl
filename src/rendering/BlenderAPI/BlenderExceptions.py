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

def check_vector_elements_normalized(input):
    for item in input:
        if not (check_scalar_normalized(item)):
            return False
    return True

def check_scalar_normalized(input):
    return 1.0 >= input >= 0.0

class InvalidInputError(Exception):
    """
    Error to call when input invalid
    """
    def __init__(self, message):
        self.message = message

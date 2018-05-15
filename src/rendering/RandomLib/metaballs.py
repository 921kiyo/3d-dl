"""
Script to create metaballs structures encoded as arrays.
Metaballs structures used for background generation.  
"""

import numpy as np

def norm(x,y,p):
    """
    Normalise x and y. Raises x and y to power p sum them and then take
    root to the power 1/p.
    Since this value can be used as divisor, a small constant is added
    to ensure it is never zero
    :param x: value to be normalized
    :param y: value to be normalized
    :param p: normalization factor
    :return: sum of normalized values raised to 1/p
    """
    #the constant factor is to ensure that norm is never 0 as it is used 
    # as divisor
    n = np.power(np.power(np.abs(x),p) + np.power(np.abs(y),p), 1./p)+1e-08
    return n

class ball:
    """
    Class representing a 2D ball, with a center, radius and normalization 
    factor. Provides function to calculate inverse distance to a point
    relative to the radius.
    :param radius: radius of the ball
    :param x0: x coordinate of the center
    :param y0: y coordinate of the center
    :param norm: normalisation factor
    """
    def __init__(self, radius, x0, y0, norm):
        self.radius = radius
        self.x0 = x0
        self.y0 = y0
        self.norm = norm

    def inverse_distance(self, x, y):
        """
        Calcutes the inverse distance from a point to the sphere center
        :param x: x coordinate of the point
        :param y: y coordinate of the point
        :return: inverse distance to the point scaled by the radius
        """
        return self.radius/norm(x-self.x0, y-self.y0, self.norm)


def sum_inverse_distance(x,y,balls):
    """
    For a given ball and array of points calculates the inverse distance
    of each point to each ball and sums values for each point together. This
    produce an array of the same size as the input x,y arrays
    :param x: array of x coordinates of individual points
    :param y: array of y coordinates of individual points
    :balls: array of ball class instances
    :return f: array of sums of inverse distances of each point to all balls
        respectively (e.g. f[0] is sum of all inverse distances of 
        point x[0],y[0])
    """
    if(x.shape!=y.shape):
        raise IndexError("The x and y parameters don't have the same shape")
    
    f = np.zeros(x.shape)
    for ball in balls:
        f += ball.inverse_distance(x,y)
    return f


def metaball(rows, cols, balls, thres):
    """
    For a 2D array of given number of rows and collumns, it calculates
    the inverse distance to all balls. Creates a boolean array of same size
    where True, if the points sum of inverse distances is bigger than given
    treshold.
    :param rows: int number of rows
    :param cols: int number of collumns
    :param balls: array of ball class instances
    :param thres: threshold for the inverse distance
    :return filled: boolean array of the specified size with True for entries
        which coordinate representation inverse distance was larger than 
        treshold
    """
    # create arrays of X,Y coordinates
    Y = np.linspace(0,rows-1,rows)
    Y = np.reshape(Y,(rows,1))
    Ystack = []
    for i in range(cols):
        Ystack.append(Y)
    Y = np.hstack(Ystack)

    X = np.linspace(0,cols-1,cols)
    Xstack = []
    for i in range(rows):
        Xstack.append(X)
    X = np.vstack(Xstack)

    # compute the sum_inverse_distance over the coordinates, using numpy matrix operations
    f = sum_inverse_distance(X,Y,balls)
    filled = f > thres
    return filled


def random_metaball(row, col, n_balls, size):
    """
    Returns a metaball images with specified size (row, col), number of 
    balls present. The amount of metaball features present can be controlled
    through the n_balls and size (threshold for pixel being included in the
    metaball)
    :param row: number of rows of returned image
    :param col: number of collumns of returned image
    :param n_balls: number of balls to generate
    :param size: treshold for point being included in a metaball
    :return metaball: returns a row*col array image of metaball features
    """
    centre_x = np.random.randint(0,col)
    centre_y = np.random.randint(0,row)
    sigma_x = np.round(col/10.0)
    sigma_y = np.round(row/10.0)
    min_ball_radius = col/(15*n_balls)
    max_ball_radius = col/(10*n_balls)

    # generate balls
    Balls = []
    for i in range(n_balls):
        x = np.round(np.random.normal(centre_x, sigma_x))
        y = np.round(np.random.normal(centre_y, sigma_y))
        x = min(max(x,0),col-1)
        y = min(max(y,0),row-1)
        radius = np.random.uniform(min_ball_radius, max_ball_radius)

        norm = np.random.randint(1,3)

        Balls.append(ball(radius, x, y, norm))

    return metaball(row, col, Balls, size)

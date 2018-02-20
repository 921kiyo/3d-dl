"""
metballs!
"""

import numpy as np

def norm(x,y,p):
    #the constant factor is to ensure that norm is never 0 as it is used 
    # as divisor
    n = np.power(np.power(np.abs(x),p) + np.power(np.abs(y),p), 1./p)+1e-08
    return n

class ball:
    def __init__(self, radius, x0, y0, norm):
        self.radius = radius
        self.x0 = x0
        self.y0 = y0
        self.norm = norm

    def inverse_distance(self, x, y):
        return self.radius/norm(x-self.x0, y-self.y0, self.norm)


def sum_inverse_distance(x,y,balls):
    if(x.shape!=y.shape):
        raise IndexError("The x and y parameters don't have the same shape")
    
    f = np.zeros(x.shape)
    for ball in balls:
        f += ball.inverse_distance(x,y)
    return f


def metaball(rows, cols, balls, thres):

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
    print("filled is", filled.shape)
    return filled


def random_metaball(row, col, n_balls, size):
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

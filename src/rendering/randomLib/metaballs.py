"""
metballs!
"""

import numpy as np

def norm(x,y,p):
    n = (abs(x)**p + abs(y)**p)**(1./p)
    return n

class ball:
    def __init__(self, radius, x0, y0, norm):
        self.radius = radius
        self.x0 = x0
        self.y0 = y0
        self.norm = norm

    def inverse_distance(self, x, y):
        if (x == self.x0) and (y==self.y0):
            return self.radius
        return self.radius/norm(x-self.x0, y-self.y0, self.norm)


def sum_inverse_distance(x,y,balls):
    f = 0.0
    for ball in balls:
        f += ball.inverse_distance(x,y)

    return f


def metaball(rows, cols, balls, thres):
    filled = np.zeros(shape=[rows,cols])
    for r in range(rows):
        for c in range(cols):
            f = sum_inverse_distance(r,c,balls)
            if f>thres:
                filled[r,c] = 1.0
    return filled


def random_metaball(row, col, n_balls, size):
    centre_x = np.random.randint(0,col)
    centre_y = np.random.randint(0,row)
    sigma_x = np.round(col/10.0)
    sigma_y = np.round(row/10.0)
    min_ball_radius = np.round(col/(15*n_balls))
    max_ball_radius = np.round(col/(10*n_balls))

    # generate balls
    Balls = []
    for i in range(n_balls):
        x = np.round(np.random.normal(centre_x, sigma_x))
        y = np.round(np.random.normal(centre_y, sigma_y))
        x = min(max(x,0),col-1)
        y = min(max(y,0),row-1)
        radius = np.random.randint(min_ball_radius, max_ball_radius)

        norm = np.random.randint(1,3)

        Balls.append(ball(radius, x, y, norm))

    return metaball(row, col, Balls, size)

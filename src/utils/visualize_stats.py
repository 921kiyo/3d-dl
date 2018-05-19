import os
import json
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from ..rendering.RandomLib import random_render as rr

"""
Script to visualize rendering stats in the parameter output logs json generated during rendering
"""

output_folder = 'D:\\PycharmProjects\\Lobster\\data\\logs\\rendering_debug_logs\\spread_cam_radius\\Anchor_stats'
stats_file = os.path.join(output_folder, 'randomvars_dump.json')

def make_ring(samples=100,normal='X'):
    D = rr.CompositeShellRingDist(0, normal)
    C = []
    for sample in range(samples):
        C.append(D.sample_param())
    return C

def plot_stats(stats_file, output_folder):

    with open(stats_file) as json_data:
        logs = json.load(json_data)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    camera_locations = logs['camera_loc']

    X = [loc[0] for loc in camera_locations]
    Y = [loc[1] for loc in camera_locations]
    Z = [loc[2] for loc in camera_locations]

    ax.scatter(X, Y, zs=Z)
    ax.set_zlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_xlim([-1, 1])

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.title('Normalized Camera Locations')
    dump_file = os.path.join(output_folder, 'camera_locations.jpg')
    plt.savefig(dump_file)
    plt.close(fig)

    fig = plt.figure()
    plt.subplot(211)
    camera_radii = logs['camera_radius']
    plt.hist(camera_radii, bins=25)
    plt.ylabel('Number of scenes (images)')
    plt.title('Camera Radius Histogram')

    plt.subplot(212)
    camera_radii = logs['spin_angle']
    plt.hist(camera_radii, bins=25)
    plt.title('Spin angle Histogram')
    plt.ylabel('Number of scenes (images)')
    dump_file = os.path.join(output_folder, 'camera_stats.jpg')
    plt.savefig(dump_file)
    plt.close(fig)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    lamp_locations = logs['lamp_loc']

    X = [loc[0] for loc in lamp_locations]
    Y = [loc[1] for loc in lamp_locations]
    Z = [loc[2] for loc in lamp_locations]

    ax.scatter(X, Y, zs=Z)
    ax.set_zlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_xlim([-1, 1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.title('Normalized Lamp Locations')
    dump_file = os.path.join(output_folder, 'lamp_locations.jpg')
    plt.savefig(dump_file)
    plt.close(fig)

    fig = plt.figure()
    plt.subplot(211)
    lamp_energies = logs['lamp_energy']
    plt.hist(lamp_energies, bins=25)
    plt.ylabel('Number of lamps')
    plt.title('Lamp Energy Histogram')

    plt.subplot(212)
    lamp_energies = logs['lamp_distance']
    plt.hist(lamp_energies, bins=25)
    plt.ylabel('Number of lamps')
    plt.title('Lamp Distance Histogram')

    dump_file = os.path.join(output_folder, 'lamp_stats.jpg')
    plt.savefig(dump_file)
    plt.close(fig)


plot_stats(stats_file, output_folder)

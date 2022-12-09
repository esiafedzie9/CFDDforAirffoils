from matplotlib import pyplot as plt
from control_volume.geometry import Geometry


def PLOT(geometry: Geometry):
    # create the fig and axis
    fig, ax = plt.subplots(1)
    ax.set_aspect('equal')
    ax.scatter(geometry.x, geometry.y)
    plt.show()
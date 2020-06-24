# draw a graph using trilaterate
# https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import trilaterate as tri

def drawCircle(p, r):
    u = np.linspace(0, 2 * np.pi, 20)
    v = np.linspace(0, np.pi, 20)
    x = r * np.outer(np.cos(u), np.sin(v)) + p[0]
    y = r * np.outer(np.sin(u), np.sin(v)) + p[1]
    z = r * np.outer(np.ones(np.size(u)), np.cos(v)) + p[2]
    ax.plot_surface(x, y, z, color='r', alpha=0.1)

if __name__ == "__main__":
    # x y r
    measurement = np.array([[6.6, 5.4, 9.2],
                            [-6.0, -6.8, 10.54],
                            [9.4, -6.7, 8.5]])

    for i, data in enumerate(measurement):
        print(str(i + 1) + ". COORD: {0:<20}  RANGE: {1:<15}".format(str(measurement[i, [0, 1]]), measurement[i, 2])) # new print method
    
    location = tri. trilaterate2D(measurement[:, [0, 1]], measurement[:, 2])
    np.set_printoptions(precision=3, suppress=True)
    print("{0:.3f}, {1:.3f}".format(location[0], location[1]))

    #draw 2D
    fig, ax = plt.subplots()
    plt.plot(location[0], location[1], 'bo')

    for circles in measurement:
        circle = plt.Circle(circles[[0, 1]], circles[2], color='r', fill=False)
        ax.add_artist(circle)
        
    ax.grid(linestyle='--')
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_aspect(1)


    # 3D x y z r
    measurement = np.array([[2.0, 3.0, 10.0, 10.7],
                            [-1.5, -4.0, 4.0, 5.9],
                            [7.0, -8.0, -4.5, 12],
                            [-4.0, 6.0, -7.0, 10.1]])

    for i, data in enumerate(measurement):
        print(str(i + 1) + ". COORD: {0:<20}  RANGE: {1:<15}".format(str(measurement[i, [0, 1, 2]]), measurement[i, -1])) # new print method
    
    location3D = tri.trilaterate3D(measurement[:, [0, 1, 2]], measurement[:, -1])
    print("{0:.3f}, {1:.3f}, {2:.3f}".format(location3D[0], location3D[1], location3D[2]))
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    for data in measurement:
        drawCircle(data[[0, 1, 2]], data[-1])

    ax.scatter(location3D[0], location3D[1], location3D[2], color='b', s=100)
    # show plots
    plt.show()
# https://en.wikipedia.org/wiki/True_range_multilateration
# adapted from https://github.com/akshayb6/trilateration-in-3d/blob/master/trilateration.py

import numpy as np

# 2D trilateration requires 3 circles
def trilaterate2D(coordinates, ranges):
    # the following points
    p = coordinates
    r = ranges

    e_x = (p[1] - p[0]) / np.linalg.norm(p[1] - p[0])
    i = np.dot(e_x, p[2] - p[0])
    e_y = (p[2] - p[0] - i * e_x) / np.linalg.norm(p[2] - p[0] - i * e_x)
    d = np.linalg.norm(p[1] - p[0])
    j = np.dot(e_y, p[2] - p[0])
    x = ((r[0] ** 2) - (r[1] ** 2) + (d ** 2)) / (2 * d)
    y = (((r[0]** 2) - (r[2]** 2) + (i ** 2) + (j ** 2)) / (2 * j)) - ((i * x) / j)
    point = p[0] + x * e_x + y * e_y
    return point

# similar BUT 3D trilateration requires 4 circles
def trilaterate3D(coordinates, ranges):
    p = coordinates
    r = ranges

    e_x = e_x = (p[1] - p[0]) / np.linalg.norm(p[1] - p[0])
    i = np.dot(e_x, p[2] - p[0])
    e_y = (p[2] - p[0] - i * e_x) / np.linalg.norm(p[2] - p[0] - i * e_x)
    e_z = np.cross(e_x, e_y)
    d = np.linalg.norm(p[1] - [0])
    j = np.dot(e_y, (p[2] - p[0]))
    x = ((r[0] ** 2) - (r[1] ** 2) + (d ** 2)) / (2 * d)
    y = (((r[0]** 2) - (r[2]** 2) + (i ** 2) + (j ** 2)) / (2 * j)) - ((i * x) / j)
    z1 = np.sqrt(r[0]**2 - x**2 - y**2)
    z2 = np.sqrt(r[0]**2 - x**2 - y**2) * -1
    a1 = p[0] + x * e_x + y * e_y + z1 * e_z
    a2 = p[0] + x * e_x + y * e_y + z2 * e_z
    d1 = np.linalg.norm(p[3] - a1)
    d2 = np.linalg.norm(p[3] - a2)
    if np.abs(r[3] - d1) < np.abs(r[3] - d2):
        return a1
    else:
        return a2

if __name__ == "__main__":
    # 2D x y r
    measurement = np.array([[6.6, 5.4, 9.2],
                            [-6.0, -6.8, 10.54],
                            [9.4, -6.7, 8.5]])

    for i, data in enumerate(measurement):
        print(str(i + 1) + ". COORD: {0:<20}  RANGE: {1:<15}".format(str(measurement[i, [0, 1]]), measurement[i, 2])) # new print method
    
    location = trilaterate2D(measurement[:, [0, 1]], measurement[:, 2])
    np.set_printoptions(precision=3, suppress=True)
    print("{0:.3f}, {1:.3f}".format(location[0], location[1]))

    # 3D x y z r
    measurement = np.array([[2.0, 3.0, 10.0, 10.7],
                            [-1.5, -4.0, 4.0, 5.9],
                            [7.0, -8.0, -4.5, 12],
                            [-4.0, 6.0, -7.0, 10.1]])
    for i, data in enumerate(measurement):
        print(str(i + 1) + ". COORD: {0:<20}  RANGE: {1:<15}".format(str(measurement[i, [0, 1, 2]]), measurement[i, 2])) # new print method
    
    location3D = trilaterate3D(measurement[:, [0, 1, 2]], measurement[:, -1])
    print("{0:.3f}, {1:.3f}, {2:.3f}".format(location3D[0], location3D[1], location3D[2]))
    
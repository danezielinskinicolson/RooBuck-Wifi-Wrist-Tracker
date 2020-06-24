# https://en.wikipedia.org/wiki/True_range_multilateration

import numpy as np

# 2D trilateration requires 3 points
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

if __name__ == "__main__":
    # x y r
    measurement = np.array([[6.6, 5.4, 9.2],
                            [-6.0, -6.8, 10.54],
                            [9.4, -6.7, 8.5]])

    for i, data in enumerate(measurement):
        print(str(i + 1) + ". COORD: {0:<20}  RANGE: {1:<15}".format(str(measurement[i, [0, 1]]), measurement[i, 2])) # new print method
    
    location = trilaterate2D(measurement[:, [0, 1]], measurement[:, 2])
    np.set_printoptions(precision=3, suppress=True)
    print("{0:.3f}, {1:.3f}".format(location[0], location[1]))
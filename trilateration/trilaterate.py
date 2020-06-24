import numpy as np

# https://en.wikipedia.org/wiki/True_range_multilateration

# 2D trilateration requires 3 points
def trilaterate2D(devices):
    # the following points
    p = {}
    r = {}
    for i, data in enumerate(devices):
        p[i] = data.coordinate
        r[i] = data.range
    
    e_x = (p[1] - p[0]) / np.linalg.norm(p[1] - p[0])
    i = np.dot(e_x, p[2] - p[0])
    e_y = (p[2] - p[0] - i * e_x) / np.linalg.norm(p[2] - p[0] - i * e_x)
    d = np.linalg.norm(p[1] - p[0])
    j = np.dot(e_y, p[2] - p[0])
    x = ((r[0] ** 2) - (r[1] ** 2) + (d ** 2)) / (2 * d)
    y = (((r[0]** 2) - (r[2]** 2) + (i ** 2) + (j ** 2)) / (2 * j)) - ((i * x) / j)
    point = p[0] + x * e_x + y * e_y
    return point

class position():
    def __init__(self, coordinate, range):
        self.coordinate = coordinate
        self.range = range


if __name__ == "__main__":
    Device_List = [position(np.array((3, 44.5)), 5),
                   position(np.array((20, 19.5)), 29),
                   position(np.array((-17, 184.5)), 145)]

    for i, data in enumerate(Device_List):
        # print(str(i + 1) + ". COORD: %-*s  RANGE: %s" % (20, data.coordinate, data.range)) # some old version
        print(str(i + 1) + ". COORD: {0:<20}  RANGE: {1:<15}".format(str(data.coordinate), data.range)) # new print method

    
    location = trilaterate2D(Device_List)
    np.set_printoptions(precision=3, suppress = True)
    print("{0:.3f}, {1:.3f}".format(location[0], location[1]))

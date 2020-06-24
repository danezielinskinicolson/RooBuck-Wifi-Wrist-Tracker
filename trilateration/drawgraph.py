# draw a graph using trilaterate

import numpy as np
import matplotlib.pyplot as plt
import trilaterate as tri


if __name__ == "__main__":

    Device_List = [tri.Position(np.array((6.6, 5.4)), 9.2),
                   tri.Position(np.array((-6.0, -6.8)), 10.54),
                   tri.Position(np.array((9.4, -6.7)), 8.5)]

    for i, data in enumerate(Device_List):
        # print(str(i + 1) + ". COORD: %-*s  RANGE: %s" % (20, data.coordinate, data.range)) # some old version
        print(str(i + 1) + ". COORD: {0:<20}  RANGE: {1:<15}".format(str(data.coordinate), data.range)) # new print method

    location = tri.trilaterate2D(Device_List)
    np.set_printoptions(precision=3, suppress=True)
    print("{0:.3f}, {1:.3f}".format(location[0], location[1]))

#draw

fig, ax = plt.subplots()
plt.plot(location[0], location[1], 'bo')

for circles in Device_List:
    circle = plt.Circle(circles.coordinate, circles.range, color='r', fill=False)
    ax.add_artist(circle)
    
ax.grid(linestyle='--')
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
ax.set_aspect(1)
plt.show()

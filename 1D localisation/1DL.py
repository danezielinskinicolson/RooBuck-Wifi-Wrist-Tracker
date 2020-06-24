# sphere and line intersection
# http://www.ambrsoft.com/TrigoCalc/Sphere/SpherLineIntersection_.htm

import numpy as np
# from dataclasses import dataclass

MARGIN = 0.00001

# sort of struct, why don't i just write this in C or matlab >:-(
class Line:
    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2

class Sphere:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

if __name__ == "__main__":
    # define a line using 2 points
    l = Line(12., 17., 11., -10., -20., -14.)
    s = Sphere(0., 0., 0., 10.)

    a = (l.x2-l.x1)**2 + (l.y2-l.y1)**2 + (l.z2-l.z1)**2
    b = -2 * ((l.x2-l.x1)*(s.x-l.x1) + (l.y2-l.y1)*(s.y-l.y1) + (l.z2-l.z1)*(s.z-l.z1))
    c = (s.x-l.x1)**2 + (s.y-l.y1)**2 + (s.z-l.z1)**2 - s.r**2
    D = (b**2) - (4*a*c)
    if D < -MARGIN:
        print("No intersections found")
        raise SystemExit(0)

    if D > MARGIN:
        print("2 Intersections found")
        t = np.array([(-b + np.sqrt(D)) / (2*a), (-b - np.sqrt(D)) / (2*a)])
    else:
        print("1 Intersection found")
        t = (-b + np.sqrt(D)) / (2*a)

    x = l.x1 + (l.x2-l.x1) * t
    y = l.y1 + (l.y2-l.y1) * t
    z = l.z1 + (l.z2-l.z1) * t

    if D > MARGIN:
        print("Intersection 1: [{0:.3f} {1:.3f} {2:.3f}]".format(x[0], y[0], z[0]), "Intersection 2: [{0:.3f} {1:.3f} {2:.3f}]".format(x[1], y[1], z[1]))
    else:
        print("Intersection 1: [{0:.3f} {1:.3f} {2:.3f}]".format(x, y, z))
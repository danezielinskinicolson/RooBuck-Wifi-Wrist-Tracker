# sphere and line intersection
# http://www.ambrsoft.com/TrigoCalc/Sphere/SpherLineIntersection_.htm

import numpy as np
# from dataclasses import dataclass

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

def detect_intersection(l, s):
    """a*t^2 - b*t + c = 0"""
    a = (l.x2-l.x1)**2 + (l.y2-l.y1)**2 + (l.z2-l.z1)**2
    b = -2 * ((l.x2-l.x1)*(s.x-l.x1) + (l.y2-l.y1)*(s.y-l.y1) + (l.z2-l.z1)*(s.z-l.z1))
    c = (s.x-l.x1)**2 + (s.y-l.y1)**2 + (s.z-l.z1)**2 - s.r**2
    # discriminant
    D = (b**2) - (4*a*c)
    if D < 0:
        return None
    else:
        t = np.array([(-b + np.sqrt(D)) / (2*a), (-b - np.sqrt(D)) / (2*a)])
    # tangent check
    if t[0] == t[1]:
        t = np.delete(t, 0)
    # check only for line segment, not infinite line
    for ct, val in enumerate(t):
        if val < 0 or val > 1:
            if len(t) == 1:
                return None
            t = np.delete(t, ct, axis=0)

    x = l.x1 + (l.x2-l.x1) * t
    y = l.y1 + (l.y2-l.y1) * t
    z = l.z1 + (l.z2-l.z1) * t
    return [x, y, z]


if __name__ == "__main__":
    # define a line using 2 points
    line = Line(12., 17., 11., -10., -20., -14.) # 2 intersections
    # line = Line(0., 0., 0., 10., 0., 10.) # 1 intersection from origin
    # line = Line(10., 0., 10., 10., 0., -10.) # tangential intersection
    # line = Line(1, 1, 1, -1, -2, -3) # no intersection

    sphere = Sphere(0., 0., 0., 10.)

    p = detect_intersection(line, sphere)
    if p is None:
        print("No intersections found")
    elif np.shape(p)[1] == 1:
        print("Intersection 1: [{0:.3f} {1:.3f} {2:.3f}]".format(p[0][0], p[1][0], p[2][0]))
    else:
        print("Intersection 1: [{0:.3f} {1:.3f} {2:.3f}]".format(p[0][0], p[1][0], p[2][0]),
              "Intersection 2: [{0:.3f} {1:.3f} {2:.3f}]".format(p[0][1], p[1][1], p[2][1]))

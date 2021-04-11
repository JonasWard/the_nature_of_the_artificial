from vertex import Vertex

class Line():
    def __init__(self, v0, v1):
        self.v0 = v0
        self.v1 = v1
        self.dir = v1 - v0

    def closest_point(self, v):
        t = self.dir * (v - self.v0) / v.length() ** 2.
        return self.v0 + self.dir * t

    def distance_to(self, v):
        return self.closest_point(v).distance_to(v)

    def point_at(self, t):
        return self.v0 + self.dir * t

    def parallel(self, other):
        return self.dir.parallel(other.dir)

    def normal(self):
        return Vertex(self.dir).unitize().rotate_z(1.5707)

    def intersect(self, ln):
        if self.parallel(ln):
            return None
        else:
            pass

    def bounds(self):
        return Vertex.bounds([self.v0, self.v1])

    def length(self):
        return self.dir.length()

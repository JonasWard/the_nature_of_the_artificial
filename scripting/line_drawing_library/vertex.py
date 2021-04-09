from math import sin, cos, atan2

class Vertex():
    DISTANCE_TOLERANCE = 0.001

    def __init__(self, x, y=0., z=0.):
        if isinstance(x, float):
            self.x = x
            self.y = y
            self.z = z
        elif isinstance(x, Vertex):
            self.x = x.x
            self.y = x.y
            self.z = x.z
        else:
            raise TypeError("Vertex initialization only accept floats or Vertex (not {})".format(type(x)))

    def add(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

        return self

    def subtract(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

        return self

    def pos_angle(self, other):
        x1,x2,y1,y2=self.x, other.x, self.y, other.y
        dot = x1*x2 + y1*y2      # dot product between [x1, y1] and [x2, y2]
        det = x1*y2 - y1*x2      # determinant
        angle = atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)

        return angle

    def cross_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def multiplication(self, other):
        if isinstance(other, float) or isinstance(other, int):
            self.x *= other
            self.y *= other
            self.z *= other

            return self
        elif isinstance(other, Vertex):
            print("(Multiplicating vertex with vertex, returning cross product)")
            return self.cross_product(other)
        
        else:
            raise TypeError("Vertex multiplication not defined for {}".format(type(x)))

    def division(self, other):
        if isinstance(other, float) or isinstance(other, int):
            self.x /= other
            self.y /= other
            self.z /= other

            return self
        
        else:
            raise TypeError("Vertex multiplication not defined for {}".format(type(x)))

    def rotate_z(self, angle):
        s, c = sin(angle), cos(angle)
        self.x, self.y = c * self.x - s * self.y, s * self.x + c * self.y

    def length(self):
        return (self.x ** 2. + self.y ** 2. + self.z ** 2.) ** .5

    def unitize(self):
        self.division(self.length())
        return self

    def clone(self):
        return Vertex(self)

    def distance(self, other):
        return (other - self).length()

    def equal(self, other):
        return self == other

    def parallel(self, other):
        d0, d1 = Vertex(self).unitize(), Vertex(other).unitize()
        if (d0 == d1) or (d0.distance(d1) == 2.):
            return True
        return False

    def __eq__(self, other):
        return self.distance(other) < Vertex.DISTANCE_TOLERANCE

    def __abs__(self, other):
        return Vertex(abs(self.x), abs(self.y), abs(self.z))

    def __add__(self, other):
        return Vertex(self).add(other)

    def __sub__(self, other):
        return Vertex(self).subtract(other)

    def __mul__(self, other):
        return Vertex(self).multiplication(other)

    def __truediv__(self, other):
        return Vertex(self).multiplication(1./other)

    def __repr__(self):
        return "Vertex: {}, {}, {}".format(self.x, self.y, self.z)

if __name__ == "__main__":
    v_a = Vertex(1., 2., 3.)
    v_b = Vertex(2., 1., 1.)

    print(v_a)
    print(v_b)

    print(v_a.cross_product(v_b))
    print(v_a.multiplication(v_b))
    print(v_a.multiplication(20.))

    print(v_a + v_b)
    print(v_a * v_b)
    print(v_a.unitize())

    print(v_a.distance(v_b))
    print(v_a == v_b)
    # print(v_a / v_b)
    
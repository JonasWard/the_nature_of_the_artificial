from math import floor, sin, cos, pi
from line import Line
from vertex import Vertex

class Polyline():
    def __init__(self, vs, closed = False):
        if len(vs) < 2:
            raise ValueError("need at least 2 points for a avlid polyline")

        self.vs = vs
        self.closed = closed
        if vs[0] == vs[-1]:
            self.closed = True
            self.vs.pop(-1)

        # self.ns

    def _normals(self):
        dirs = []
        for i in range(len(self.vs)-1+self.closed):
            dirs.append((self.vs[(i+1)%len(self.vs)-self.vs[i]]).unitize())

        if not(self.closed):
            dirs.append(dirs[-1])

    def bounds(self):
        return Vertex.bounds(self.vs)

    @property
    def count(self):
        return len(self.vs)

    def segments(self):
        segs = []
        for i in range(self.count - 1):
            segs.append(self.segement_at(i))

        if self.closed:
            segs.append(Line(self.vs[-1], self.vs[0]))

        return segs

    def segement_at(self, i):
        if i < 0.:
            return Line(self.vs[0], self.vs[1])
        elif i > self.count:
            return Line(self.vs[-2], self.vs[-1])
        else:
            i_0 = i
            i_1 = i + 1

            return Line(self.vs[i_0], self.vs[i_1])

    def point_at_index(self, i):
        return self.vs[int(i)]

    def point_at(self, t):
        if self.closed:
            t %= self.count()
        
        i = t - t%1

        if i > 0:
            t -= i

        return self.segement_at(int(i)).point_at(t)

    def length(self):
        l = 0.
        for s in segments:
            l += s.length()

        return l

    def __repr__(self):
        start = "Closed" if self.closed else "Open"
            
        return "{} Polyline with {} vertices".format(start, len(self.vs))

    @staticmethod
    def rectangle(x_int, y_int):
        return Polyline(
            vs = [
                Vertex(x_int.min, y_int.min),
                Vertex(x_int.max, y_int.min),
                Vertex(x_int.max, y_int.max),
                Vertex(x_int.min, y_int.max),
            ], closed = True
        )

    @staticmethod
    def polygon(sides = 5, r = 5.):
        d = pi * 2. / sides
        return Polyline([Vertex(cos(d*i)*r, sin(d*i)*r) for i in range(sides)], True)

if __name__ == "__main__":
    from interval import Interval
    vs = [Vertex(i*1.%3.56, i*4.56%7.8, i*.2%.345) for i in range(100)]

    pl = Polyline(vs)
    print(pl)
    print((pl.point_at_index(10)+pl.point_at_index(9))*.5)
    print(pl.point_at(-9.5))
    print(pl.bounds())

    rec = Polyline.rectangle(Interval(0.1, 10.), Interval(-.5, 4.5))
    rec.segments()

    print(rec)

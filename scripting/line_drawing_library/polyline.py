from math import floor
from line import Line

class Polyline():
    def __init__(self, vs, closed = False):
        if len(vs) < 2:
            raise ValueError("need at least 2 points for a avlid polyline")

        self.vs = vs
        self.closed = closed
        if vs[0] == vs[-1]:
            self.closed = True
            self.vs.pop(-1)

        self.ns

    def _normals(self):
        dirs = []
        for i in range(len(self.vs)-1+self.closed):
            dirs.append((self.vs[(i+1)%len(self.vs)-self.vs[i]]).unitize())

        if not(self.closed):
            dirs.append(dirs[-1])

    @property
    def count(self):
        return len(self.vs)

    def segement_at(self, i):
        if i < 0.:
            return Line(self.vs[0], self.vs[1])
        elif i > self.count:
            return Line(self.vs[-2], self.vs[-1])
        else:
            i_0 = i
            i_1 = i + 1

            return Line(self.vs[i_0], self.vs[i_1])

    def point_at(self, t):
        if self.closed:
            t %= self.count()
        
        i = t - t%1

        if i > 0:
            t -= i

        return self.segement_at(i).point_at(t)

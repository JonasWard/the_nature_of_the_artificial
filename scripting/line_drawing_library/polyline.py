class Polyline():
    def __init__(self, vs, closed = False):
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


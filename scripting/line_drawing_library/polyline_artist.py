import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

from vertex import Vertex
from polyline import Polyline

def plot_vertex(v):
    pass

def read_vertex(v):
    return (v.x, v.y)

def read_vertexes(vs):
    return zip(*[(v.x, v.y) for v in vs])

def plot_points(vs):
    x, y = read_vertexes(vs)
    plt.scatter(x, y)

    plt.show()

def plot_polyline(pl):
    verts = []
    codes = []
    
    for i, v in enumerate(pl.vs):
        if i > 0:
            codes.append(Path.LINETO)
        else:
            codes.append(Path.MOVETO)

        verts.append(read_vertex(v))

    if pl.closed:
        verts.append(verts[0])
        codes.append(Path.CLOSEPOLY)

    fig, ax = plt.subplots()

    path = Path(verts, codes)
    if pl.closed:
        patch = patches.PathPatch(path, facecolor='orange', lw=2)
        ax.add_patch(patch)
    else:
        xs, ys = zip(*verts)
        ax.plot(xs, ys, lw=2, color='black')

    x_int,y_int,_ = pl.bounds()
    ax.set_xlim((x_int*1.1).as_tuple())
    ax.set_ylim((y_int*1.1).as_tuple())

    plt.show()

def simple_plot(geos):
    pass

if __name__ == "__main__":
    vs = [Vertex(i*1.%3.56, i*4.56%7.8, i*.2%.345) for i in range(100)]
    pl = Polyline(vs)

    plot_polyline(pl)

    plot_points(vs)
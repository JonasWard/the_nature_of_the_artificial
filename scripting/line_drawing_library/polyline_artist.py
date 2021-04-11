import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

from interval import Interval
from vertex import Vertex
from line import Line
from polyline import Polyline

plt.rcParams['figure.figsize'] = [12, 12]
plt.rcParams['figure.dpi'] = 80 # 200 e.g. is really fine, but slower

def plot_vertex(v):
    pass

def read_vertex(v):
    return (v.x, v.y)

def read_vertexes(vs):
    return zip(*[(v.x, v.y) for v in vs])

def ax_bounding(ax, bounds):
    ax.set_aspect(1.)

    x, y = bounds

    if x < y:
        x.match_delta(y)
    else:
        y.match_delta(x)

    ax.set_xlim((x*1.1).as_tuple())
    ax.set_ylim((y*1.1).as_tuple())

def vertices_to_plot(vs, ax):
    x, y = read_vertexes(vs)
    ax.scatter(x, y)

def line_to_plot(ln, ax):
    verts = [
        (ln.v0.x, ln.v0.y),
        (ln.v1.x, ln.v1.y)
    ]
    
    xs, ys = zip(*verts)
    ax.plot(xs, ys, lw=2, color='black')

def polyline_to_plot(pl, ax):
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

    path = Path(verts, codes)
    if pl.closed:
        patch = patches.PathPatch(path, facecolor='orange', lw=2)
        ax.add_patch(patch)
    else:
        xs, ys = zip(*verts)
        ax.plot(xs, ys, lw=2, color='black')

def plot_points(vs):
    fig, ax = plt.subplots()

    vertices_to_plot(vs, ax)
    x, y, _ = Vertex.bounds(vs)

    ax_bounding(ax, (x, y))

    plt.show()

def plot_line(ln):
    fig, ax = plt.subplots()
    ax.set_aspect(1.)

    line_to_plot(ln, ax)
    x, y, _ = ln.bounds()
    ax_bounding(ax, (x, y))

    plt.show()

def plot_polyline(pl):
    fig, ax = plt.subplots()

    polyline_to_plot(pl, ax)

    x,y,_ = pl.bounds()
    ax_bounding(ax, (x, y))

    plt.show()

def geos_to_plot(ax, geos):
    bounds = []
    vertices = []

    if isinstance(geos, list):
        for geo in geos:
            bnd, vs = geos_to_plot(ax, geo)
            bounds.extend(bnd)
            vertices.extend(vs)
    elif isinstance(geos, Vertex):
        return [], [geos]
    elif isinstance(geos, Line):
        line_to_plot(geos, ax)
        return [geos.bounds()], []
    elif isinstance(geos, Polyline):
        polyline_to_plot(geos, ax)
        return [geos.bounds()], []

    return bounds, vertices

def simple_plot(geos):
    fig, ax = plt.subplots()

    bounds, vertices = geos_to_plot(ax, geos)
    vertices_to_plot(vertices, ax)

    x, y, _ = zip(*bounds)
    x, y = list(x), list(y)
    x_vs, y_vs , _ = Vertex.bounds(vertices)
    x.append(x_vs)
    y.append(y_vs)

    x,y = Interval.bounds(x), Interval.bounds(y)

    ax_bounding(ax, (x, y))

    plt.show()

if __name__ == "__main__":

    vs = [Vertex(i*1.%3.56, i*4.56%7.8, i*.2%.345) for i in range(100)]
    pl = Polyline(vs)

    plot_polyline(pl)

    plot_points(vs)

    ln = Line(
        Vertex(0., 0., 0.),
        Vertex(10., 0., 0.)
    )

    plot_line(ln)

    simple_plot([ln, pl, vs])
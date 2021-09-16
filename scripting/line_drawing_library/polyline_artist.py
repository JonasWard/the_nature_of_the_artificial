import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

from interval import Interval
from edge import Edge
from graph import Graph
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


def line_to_plot(ln, ax, line_color=None):
    verts = [
        (ln.v0.x, ln.v0.y),
        (ln.v1.x, ln.v1.y)
    ]

    line_color = 'black' if None else line_color
    
    xs, ys = zip(*verts)
    ax.plot(xs, ys, lw=2, color=line_color)


def edge_to_plot(edge, ax, spacing=0.1):
    state_cnt = len(edge.states)
    if state_cnt == 0:
        print("edges with no states defined")
        line_to_plot(edge.line_repr(), ax)

    else:
        print("edge with {} states defined".format(state_cnt))
        distance_shift = (state_cnt - 1) * .5
        ln = edge.line_repr()
        for i in range(state_cnt):
            loc_ln = ln.offset( (i - distance_shift) * spacing)
            line_to_plot(loc_ln, ax, edge.states[i].color)


def graph_to_plot(graph, ax, spacing=0.1):
    for edge in graph.edges:
        edge_to_plot(edge, ax, spacing=0.1)


def polyline_to_plot(pl, ax, line_color=None, fill_color=None):
    verts = []
    codes = []

    line_color = 'black' if None else line_color
    fill_color = 'orange' if None else fill_color

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
        patch = patches.PathPatch(path, facecolor=fill_color, lw=2)
        ax.add_patch(patch)
    else:
        xs, ys = zip(*verts)
        ax.plot(xs, ys, lw=2, color=line_color)


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

    elif type(geos) == Edge:
        edge_to_plot(geos, ax)
        return [geos.bounds()], []

    elif isinstance(geos, Line) and not(isinstance(geos, Edge)):
        line_to_plot(geos, ax)
        return [geos.bounds()], []

    elif isinstance(geos, Polyline):
        polyline_to_plot(geos, ax)
        return [geos.bounds()], []

    elif isinstance(geos, Graph):
        graph_to_plot(geos, ax)
        return [geos.bounds()], []

    return bounds, vertices


def simple_plot(geos):
    fig, ax = plt.subplots()
    fig = simple_plot_figax(fig, ax, geos)

    plt.show()


def simple_plot_figax(fig, ax, geos):
    x, y = [], []

    bounds, vertices = geos_to_plot(ax, geos)
    if any(bounds):
        x, y, _ = zip(*bounds)
        x, y = list(x), list(y)

    if any(vertices):
        vertices_to_plot(vertices, ax)
        x_vs, y_vs , _ = Vertex.bounds(vertices)
        x.append(x_vs)
        y.append(y_vs)

    if any(x) and any(y):
        x,y = Interval.bounds(x), Interval.bounds(y)
        ax_bounding(ax, (x, y))

    return fig


if __name__ == "__main__":

    vs = [Vertex(i*1.%3.56, i*4.56%7.8, i*.2%.345) for i in range(100)]
    pl = Polyline(vs)

    plot_polyline(pl)

    plot_points(vs)

    ln = Line(
        Vertex(0., 0., 0.),
        Vertex(10., 0., 0.)
    )

    edge = Edge(
        Vertex(0., 0., 0.),
        Vertex(10., 0., 0.)
    )

    print(edge)
    print(type(edge) == Edge)

    plot_line(ln)

    simple_plot([ln, pl, vs])
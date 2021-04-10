import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

def plot_vertex(v):
    pass

def read_vertex(v):
    return (v.x, v.y)

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

    x0,x1,y0,y1,_,_ = pl.bounds()
    dx = x1 - x0
    dy = y1 - y0
    ax.set_xlim(x0-dx*.1,x1+dx*.1)
    ax.set_ylim(y0-dy*.1,y1+dy*.1)

    plt.show()

def simple_plot(geos):
    pass


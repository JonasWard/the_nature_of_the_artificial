import skgeom as sg
from vertex import Vertex
from line import Line
from polyline import Polyline

def translate_from_skg_objects(geos):
    if isinstance(geos, list):
        geos_2d = []
        for geo in geos:
            geos_2d.extend(translate_from_skg_objects(geo))
        return geos_2d
    elif isinstance(geos, sg._skgeom.Point2):
        return [translate_point_to_vertex(geos)]
    elif isinstance(geos, sg._skgeom.Polygon):
        return [translate_polygon_to_pl2d(geos)]
    elif isinstance(geos, sg._skgeom.Skeleton):
        return translate_skeleton_to_lines(geos)
    else:
        print("tried to convert type: {}".format(type(geos).__name__))

def translate_point_to_vertex(pt):
    return Vertex(float(pt.x()), float(pt.y()))

def translate_polygon_to_pl2d(plg):
    vs = []
    for v in plg.vertices:
        vs.append(translate_point_to_vertex(v))

    return Polyline(vs, True)

def mv_points(pts, x,y):
    n_pts = []
    for pt in pts:
        n_pts.append(sg.Point2(float(pt.x()) + x, float(pt.y())+y))
    return n_pts

def translate_skeleton_to_lines(ske):
    lns = []

    if isinstance(ske, list):
        for skeleton in ske:
            lns.extend(translate_skeleton_to_lines(skeleton))

    elif isinstance(ske, sg._skgeom.Skeleton): 
        for h in ske.halfedges:
            if h.is_bisector:
                p1 = h.vertex.point
                p2 = h.opposite.vertex.point

                lns.append(Line(
                    translate_point_to_vertex(p1),
                    translate_point_to_vertex(p2)
                ))
    else:
        print("tried to convert type: {}".format(type(ske).__name__))

    return lns

if __name__ == "__main__":
    from polyline_artist import simple_plot

    plg_1 = sg.random_polygon(seed=10)
    plg_2 = sg.random_polygon(seed=100)
    plg_3 = sg.random_polygon(seed=1000)

    plg_2 = sg.Polygon(mv_points(plg_2.vertices, 10., 10.))
    # plg_3.transform()
    # pt_2 = Vertex(10., 10.)
    ori_geos = [plg_1, plg_2, plg_3]

    skes = [sg.skeleton.create_interior_straight_skeleton(plg) for plg in ori_geos]

    simple_plot([
        translate_from_skg_objects(ori_geos)]+translate_skeleton_to_lines(skes)
    )
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

def from_number_lists(list_of_list_of_lists):
    plgs = []
    for coordinates in list_of_list_of_lists:
        pts = []
        for x, y in coordinates:
            pts.append(sg.Point2(x, y))
        plgs.append(sg.Polygon(pts))
    
    return plgs

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

    rhino_pt_lists = [[[-2366.0723216185265, -3654.7480689800168], [-2369.9115779035178, -3675.7691360714189], [-2369.6225198685111, -3675.8280156860228], [-2362.9151582245227, -3676.9737245840179], [-2361.7545927645092, -3670.9660970364157], [-2357.2559130175191, -3671.790598652321], [-2356.8122420085106, -3669.2974940406157], [-2352.6084526645113, -3670.0405649347185], [-2350.4297512265307, -3657.6732305921205], [-2359.8515299135156, -3655.8918551392226], [-2365.885632481511, -3654.7684746942205]], [[-2362.8614076356239, -3706.9785942848271], [-2362.8933234696228, -3706.9213633231288], [-2368.3542775176243, -3706.015630776727], [-2370.8593307166079, -3719.2125381022292], [-2366.4214129236129, -3720.0006593313324], [-2366.7798285146196, -3721.8970335598301], [-2361.3537683626123, -3722.9457063408286], [-2360.9737615456174, -3720.8945989838271], [-2360.4430867256083, -3720.9877440220321], [-2360.1491383426251, -3719.6891310747328], [-2360.7150390396196, -3719.6053645470333], [-2358.6434451726159, -3707.8559396269288]], [[-2371.7676607929534, -3754.7570962809223], [-2373.4978816499715, -3762.016251598925], [-2368.3340596199632, -3763.1631639279258], [-2370.2572702539692, -3772.6273987629211], [-2364.952772549972, -3773.8814581771258], [-2361.1312779549698, -3757.1330276014232]], [[-2373.1174749693923, -3815.150099671609], [-2376.8332255413875, -3816.0738484636126], [-2377.2588843413864, -3812.7102226996099], [-2367.6715764373835, -3810.3923690006081], [-2368.483274733389, -3807.0920649845971], [-2365.4984417403934, -3806.3954462935976], [-2356.8740161363853, -3804.3805244135906], [-2355.2974864253952, -3810.7359554816098]], [[-2373.2733252967846, -3849.3179805839868], [-2373.5782167197867, -3848.13599027399], [-2371.5398300687775, -3847.4754534059871], [-2372.1162525267828, -3845.3008994169909], [-2362.5464797827844, -3842.6045705949914], [-2359.9089376047887, -3853.3972853679993], [-2360.8197116187912, -3854.9356141810099], [-2370.8675421977787, -3857.794579490987]], [[-2373.3224867248678, -3901.1203905479833], [-2361.2770863558576, -3903.5503825169781], [-2358.1114563178739, -3889.9995441399715], [-2363.20385810787, -3887.8100004459757], [-2361.7255476408641, -3884.0567037559722], [-2374.8533058458593, -3880.4657519709635], [-2376.2219672538517, -3887.5822935909873], [-2370.9345906318517, -3890.4571581069813]], [[-2363.3742437792457, -3924.5271881665226], [-2354.3028813842607, -3928.4338322145172], [-2358.6356691362375, -3943.2792387815257], [-2364.8727712232426, -3941.728745038517], [-2368.2504060022397, -3948.5533713525342], [-2373.3347951712417, -3946.1305473055231], [-2376.5101741952453, -3953.6407267455193], [-2381.6487270482389, -3952.7845098635421], [-2373.5870832252472, -3934.0300108705246], [-2366.9293039832478, -3936.2736234285235]]]

    plgs = from_number_lists(rhino_pt_lists)

    skes = [sg.skeleton.create_interior_straight_skeleton(plg) for plg in plgs]

    simple_plot([
        translate_from_skg_objects(plgs)]
    )

    for i, ske in enumerate(skes):
        simple_plot(translate_from_skg_objects(plgs[i]) + translate_skeleton_to_lines(ske))
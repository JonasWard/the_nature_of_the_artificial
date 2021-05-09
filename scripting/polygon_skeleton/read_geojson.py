import json
import skgeom as sg
from vertex import Vertex
from line import Line
from polyline import Polyline
from polyline_artist import simple_plot

def read_coords(coord_list):
    vertexes = []

    if isinstance(coord_list[0], list):
        for c in coord_list:
            vertexes.append(read_coords(c))
    elif isinstance(coord_list[0], float) or isinstance(coord_list[0], int):
        x, y, z = 0., 0., 0.
        if len(coord_list) == 3:
            x, y, z = coord_list
        elif len(coord_list) == 2:
            x, y = coord_list
        elif len(coord_list) == 1:
            x = coord_list
        
        return Vertex(x, y, z)

    return vertexes

def reading_polygons(vertex_lists):
    plgs = []
    if isinstance(vertex_lists[0], list):
        for v_list in vertex_lists:
            plgs.extend(reading_polygons(v_list))
    elif isinstance(vertex_lists[0], Vertex):
        # print(vertex_lists)
        plgs = [Polyline(vertex_lists, True)]

    return plgs

def reading_json(data):
    geo_list = []

    for f in data["features"]:
        geo = f["geometry"]
        geo_list.append(read_coords(geo["coordinates"]))

    return geo_list

if __name__ == "__main__":
    example_path = "/Users/jonas/Documents/reps/polygon_to_building/data/almere_houses.geojson"

    with open(example_path) as f:
        data = json.load(f)

    plgs = reading_polygons(reading_json(data))
    # print(plgs)
    simple_plot(plgs)
from edge import Edge
from interval import Interval
from vertex import Vertex


class Graph:
    def __init__(self, vs, edge_pair_indexes, states=[]):
        self.edges = []
        if any(states):
            for i, i_a, i_b in enumerate(edge_pair_indexes):
                state = states[i % len(states)]
                self.edges.append(Edge(vs[i_a], vs[i_a], state))
        else:
            for i_a, i_b in edge_pair_indexes:
                self.edges.append(Edge(vs[i_a], vs[i_a]))

    def bounds(self):

        x_ints, y_ints = [], []
        for edge in self.edges:
            x_int, y_int = edge.bounds()

            x_ints.append(x_int)
            y_ints.append(y_int)

        return Interval.bounds(x_ints), Interval(y_ints)


if __name__ == "__main__":
    from polyline_artist import simple_plot

    vs = [
        Vertex(0),
        Vertex(1),
        Vertex(1, 1),
        Vertex(0, 1)
    ]

    e_is = [
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 3),
        (3, 1),
        (3, 0)
    ]

    g = Graph(vs, e_is)
    simple_plot(g)
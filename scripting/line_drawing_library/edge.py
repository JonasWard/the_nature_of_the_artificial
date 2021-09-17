from line import Line
from vertex import Vertex


class State:

    def __init__(self, name = "default", color = (0, 0, 0)):
        self.name = name
        self.color = color


class Edge:

    def __init__(self, v0, v1, states=[]):
        self.v0 = v0
        self.v1 = v1
        self.states = set(states)

    def line_repr(self):
        return Line.copy(self)

    def add_state(self, state):
        self.states.add(state)

    def bounds(self):
        return Line.bounds(self)


if __name__ == "__main__":
    from polyline_artist import simple_plot

    v0, v1 = Vertex(0.), Vertex(1., 1.)
    v2, v3 = Vertex(0., 1.), Vertex(1., 0.)

    edges = [
        Edge(v0, v1, [State()]),
        Edge(v2, v3, [State()])
    ]

    simple_plot(edges)
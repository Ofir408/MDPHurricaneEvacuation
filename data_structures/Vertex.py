from typing import List


class Vertex:
    def __init__(self, vertex_name: str, evacuees_probability: int, edges: List[str] = [],
                 parent_vertex: 'Vertex' = None,
                 action: str = None, depth: int = 0):
        self.__vertex_name = vertex_name
        self.__evacuees_probability = evacuees_probability
        self.__edges = edges
        self.__parent_vertex = parent_vertex
        self.__action = action
        self.__depth = depth

    def add_edge_name(self, edge_name: str):
        self.__edges.append(edge_name)

    def set_parent_vertex(self, parent_vertex: 'Vertex'):
        self.__parent_vertex = parent_vertex

    def set_action(self, action):
        self.__action = action

    def set_depth(self, depth):
        self.__depth = depth

    def get_vertex_name(self):
        return self.__vertex_name

    def get_evacuees_probability(self):
        return self.__evacuees_probability

    def get_edges(self) -> List[str]:
        return self.__edges

    def get_parent_vertex(self):
        return self.__parent_vertex

    def get_action(self):
        return self.__action

    def get_depth(self):
        return self.__depth

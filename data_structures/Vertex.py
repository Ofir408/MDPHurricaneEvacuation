from typing import List


class Vertex:
    def __init__(self, vertex_name: str, edges=None):
        if edges is None:
            edges = []
        self.__vertex_name = vertex_name
        self.__edges = edges

    def add_edge_name(self, edge_name: str):
        self.__edges.append(edge_name)

    def get_vertex_name(self):
        return self.__vertex_name

    def get_edges(self) -> List[str]:
        return self.__edges

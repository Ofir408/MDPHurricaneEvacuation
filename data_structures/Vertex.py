from typing import List


class Vertex:
    def __init__(self, vertex_name: str, evacuees_probability: int, edges: List[str] = []):
        self.__vertex_name = vertex_name
        self.__evacuees_probability = evacuees_probability
        self.__edges = edges

    def add_edge_name(self, edge_name: str):
        self.__edges.append(edge_name)

    def get_vertex_name(self):
        return self.__vertex_name

    def get_evacuees_probability(self):
        return self.__evacuees_probability

    def get_edges(self) -> List[str]:
        return self.__edges

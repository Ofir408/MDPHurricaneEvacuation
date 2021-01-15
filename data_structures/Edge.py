from typing import Tuple


class Edge:

    def __init__(self, edge_name: str, weight: int, vertex_names: Tuple[str, str], blockages_probability: float):
        self.__edge_name = edge_name
        self.__weight = weight
        self.__vertex_names = vertex_names
        self.__blockages_probability = blockages_probability

    def get_edge_name(self):
        return self.__edge_name

    def get_weight(self):
        return self.__weight

    def get_vertex_names(self):
        return self.__vertex_names

    def get_blockages_probability(self):
        return self.__blockages_probability

    def set_blockages_probability(self, prob: float):
        self.__blockages_probability = prob

    def __str__(self) -> str:
        return "Edge: {0}, Weight: {1}, Vertexes: {2}, blockage prob: {3}".format(self.__edge_name, self.__weight,
                                                                                  self.__vertex_names,
                                                                                  self.__blockages_probability)

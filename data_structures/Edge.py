from typing import Tuple


class Edge:

    def __init__(self, edge_name: str, weight: int, vertex_names: Tuple[str, str], blockages_probability: float):
        self.__edge_name = edge_name
        self.__weight = weight
        self.__vertex_names = vertex_names
        self.__blockages_probability = blockages_probability
        self.__is_blocked_prob = False

    def get_edge_name(self):
        return self.__edge_name

    def get_weight(self):
        return self.__weight

    def get_vertex_names(self):
        return self.__vertex_names

    def get_blockages_probability(self):
        return self.__blockages_probability

    def get_is_blocked_prob_calc(self):
        return self.__is_blocked_prob

    def set_blockages_probability(self, prob: float):
        self.__blockages_probability = prob

    def set_is_blocked_prob(self, is_blocked_prob_calc: bool):
        self.__is_blocked_prob = is_blocked_prob_calc

    def __str__(self) -> str:
        return "Edge: {0}, Vertexes: {1}".format(self.__edge_name, self.__vertex_names)

    def full_str(self) -> str:
        return "Edge: {0}, Vertexes: {1}, blockages_probability: {2}".format(self.__edge_name, self.__vertex_names, self.__blockages_probability)

    def __eq__(self, other: 'Edge'):
        return self.__edge_name == other.__edge_name and self.__weight == other.__weight \
               and self.__vertex_names == other.__vertex_names \
               and self.__blockages_probability == other.__blockages_probability and self.get_is_blocked_prob_calc() == other.get_is_blocked_prob_calc()

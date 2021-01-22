import copy
from typing import List

from data_structures.Edge import Edge


class BeliefState:
    def __init__(self, vertex_name: str, blockages_edges: List[Edge], is_goal: bool = False):
        self.__vertex_name = vertex_name
        self.__blockages_edges = copy.deepcopy(blockages_edges)
        self.__is_goal = is_goal

    def get_vertex_name(self):
        return self.__vertex_name

    def get_blockages_edges(self):
        return self.__blockages_edges

    def get_is_goal(self):
        return self.__is_goal

    def set_is_goal(self, is_goal: bool):
        self.__is_goal = is_goal

    def __str__(self):
        edges_str = ""
        for edge in self.__blockages_edges:
            is_blocked_str = "Unknown"
            if edge.get_blockages_probability() == 0:
                is_blocked_str = "UnBlocked"
            if edge.get_blockages_probability() == 1:
                is_blocked_str = "Blocked"
            edges_str += "edge_name= {0},is_blocked= {1}".format(edge.get_edge_name(), is_blocked_str)

        return "{0}, blockages_edges({1})".format(self.__vertex_name, edges_str)

    def __eq__(self, other: 'BeliefState'):
        same_name = self.__vertex_name == other.__vertex_name
        same_blockages_edges = self.__blockages_edges == other.__blockages_edges
        return same_name and same_blockages_edges

    def __hash__(self):
        edges_strings = [e.full_str() for e in self.__blockages_edges]
        return hash(self.__vertex_name) + hash(str(edges_strings))

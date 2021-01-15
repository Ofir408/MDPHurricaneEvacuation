import copy
from typing import List

from data_structures.Edge import Edge


class BeliefState:
    def __init__(self, vertex_name: str, blockages_edges: List[Edge]):
        self.__vertex_name = vertex_name
        self.__blockages_edges = copy.deepcopy(blockages_edges)

    def get_vertex_name(self):
        return self.__vertex_name

    def get_blockages_edges(self):
        return self.__blockages_edges

    def __str__(self):
        edges_str = ""
        for edge in self.__blockages_edges:
            edges_str += "edge_name= {0}, is_blocked= {1}".format(edge.get_edge_name(),
                                                                  edge.get_blockages_probability())
        return "vertex_name= {0}, blockages_edges= {1}".format(self.__vertex_name, edges_str)

from typing import Dict

from data_structures.Edge import Edge
from data_structures.Vertex import Vertex


class EnvironmentConfiguration:

    def __init__(self, vertices_num: int, persistence: float, vertex: Dict[str, Vertex], edges: Dict[str, Edge]):
        self.__vertices_num = vertices_num
        self.__persistence = persistence
        self.__vertexes = vertex
        self.__edges = edges
        self.__blocked_edges = []

    def get_vertices_num(self):
        return self.__vertices_num

    def get_persistence(self):
        return self.__persistence

    def get_vertexes(self):
        return self.__vertexes

    def get_edges(self):
        return self.__edges

    def get_blocked_edges(self):
        return self.__blocked_edges

    def set_blocked_edge(self, edge_to_block):
        return self.__blocked_edges.append(edge_to_block)

from typing import List

from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.Edge import Edge
from data_structures.Vertex import Vertex


class EnvironmentUtils:
    _EDGE_PREFIX = "#E"
    _VERTEX_PREFIX = "#V"
    _WEIGHT_PREFIX = "W"
    _SPACE_SEPARATOR = " "
    _NUMBER_OF_VERTICES_PREFIX = "#N"
    _PERSONS_NUM_PREFIX = "F"

    @staticmethod
    def print_environment(env_config: EnvironmentConfiguration):
        num_of_vertex = env_config.get_vertices_num()
        edges_dict = env_config.get_edges()
        vertexes_dict = env_config.get_vertexes()

        print(EnvironmentUtils._NUMBER_OF_VERTICES_PREFIX + EnvironmentUtils._SPACE_SEPARATOR + str(
            num_of_vertex))

        for vertex in vertexes_dict.values():
            EnvironmentUtils.__print_vertex(vertex)
        for edge in edges_dict.values():
            EnvironmentUtils.__print_edge(edge)
        print("\n")

    @staticmethod
    def get_possible_moves(current_vertex: Vertex, env_config: EnvironmentConfiguration) -> List[Edge]:
        current_vertex_name = current_vertex.get_vertex_name()
        vertexes_dict = env_config.get_vertexes()
        edges_dict = {k: v for k, v in env_config.get_edges().items() if k not in env_config.get_blocked_edges()}
        current_vertex = vertexes_dict[current_vertex_name]
        names_of_edges = [edge for edge in current_vertex.get_edges() if
                          edge not in env_config.get_blocked_edges()]
        possible_edges = []
        for edge_name in names_of_edges:
            possible_edges.append(edges_dict[edge_name])
        return possible_edges

    @staticmethod
    def get_next_vertex(current_vertex: Vertex, edge_name: str,
                        env_config: EnvironmentConfiguration) -> Vertex:
        """

        :param current_vertex: the current state
        :param edge_name: edge name from current vertex to the next vertex
        :param env_config: environment configuration
        :return: The new vertex
        """
        current_vertex_name = current_vertex.get_vertex_name()
        edges_dict = env_config.get_edges()
        vertexes_dict = env_config.get_vertexes()
        edge = edges_dict[edge_name]
        first_vertex, sec_vertex = edge.get_vertex_names()
        next_vertex_name = first_vertex if sec_vertex == current_vertex_name else sec_vertex
        next_vertex = vertexes_dict[next_vertex_name]
        return next_vertex

    @staticmethod
    def __print_vertex(vertex: Vertex):
        print(vertex.get_vertex_name())

    @staticmethod
    def __print_edge(edge: Edge):
        print(edge)

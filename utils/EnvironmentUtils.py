import copy
from typing import List, Callable

from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.Edge import Edge
from data_structures.Vertex import Vertex


class EnvironmentUtils:
    _EDGE_PREFIX = "#E"
    _VERTEX_PREFIX = "#V"
    _WEIGHT_PREFIX = "W"
    _SPACE_SEPARATOR = " "
    _PERSISTENCE_PREFIX = "#Ppersistence"
    _NUMBER_OF_VERTICES_PREFIX = "#N"
    _PERSONS_NUM_PREFIX = "F"

    @staticmethod
    def print_environment(env_config: EnvironmentConfiguration):
        num_of_vertex = env_config.get_vertices_num()
        persistence = env_config.get_persistence()
        edges_dict = env_config.get_edges()
        vertexes_dict = env_config.get_vertexes()

        print(EnvironmentUtils._NUMBER_OF_VERTICES_PREFIX + EnvironmentUtils._SPACE_SEPARATOR + str(
            num_of_vertex))
        print(EnvironmentUtils._PERSISTENCE_PREFIX + EnvironmentUtils._SPACE_SEPARATOR + str(persistence))

        for vertex in vertexes_dict.values():
            EnvironmentUtils.__print_vertex(vertex)
        for edge in edges_dict.values():
            EnvironmentUtils.__print_edge(edge)
        print("Blocked edges: ", env_config.get_blocked_edges())

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
    def get_next_vertex(current_vertex: Vertex, edge_name: str, step_cost: Callable,
                        env_config: EnvironmentConfiguration, is_max_player: bool = True) -> Vertex:
        """

        :param current_vertex: the current state
        :param edge_name: edge name from current vertex to the next vertex
        :param step_cost: function that receives parent_vertex, action, new_node and returns the step cost.
        :param is_max_player: True if this is the max player, false otherwise
        :param env_config: environment configuration
        :return: The new vertex
        """
        current_state = current_vertex.get_state()
        current_vertex_name = current_vertex.get_vertex_name()
        edges_dict = env_config.get_edges()
        vertexes_dict = env_config.get_vertexes()
        if edge_name not in edges_dict:
            current_vertex.set_state(current_state)
            print("edge_name= ", edge_name)
            print("No operation for this agent")
            current_vertex.set_cost(
                current_vertex.get_cost() + step_cost(current_vertex, Edge("", 0, ("", "")), current_vertex))
            return current_vertex  # No operation

        edge = edges_dict[edge_name]
        first_vertex, sec_vertex = edge.get_vertex_names()
        next_vertex_name = first_vertex if sec_vertex == current_vertex_name else sec_vertex
        next_vertex = vertexes_dict[next_vertex_name]
        return next_vertex

    @staticmethod
    def g(node: Vertex, env_conf: EnvironmentConfiguration) -> int:
        current_node = copy.deepcopy(node)
        edges = env_conf.get_edges()
        edges_of_path = []
        cost = 0
        while current_node is not None:
            edges_of_path.append(current_node.get_action() if current_node.get_action() is not None else "")
            current_node = current_node.get_parent_vertex()
        # calculate the cost to the solution
        for edge_name in filter(None, edges_of_path):
            cost += edges[edge_name].get_weight()
        return cost

    @staticmethod
    def __print_vertex(vertex: Vertex):
        print(
            EnvironmentUtils._VERTEX_PREFIX + vertex.get_vertex_name() + EnvironmentUtils._SPACE_SEPARATOR
            + EnvironmentUtils._PERSONS_NUM_PREFIX + str(vertex.get_evacuees_probability()))

    @staticmethod
    def __print_edge(edge: Edge):
        first_vertex_name, second_vertex_name = edge.get_vertex_names()
        print(
            EnvironmentUtils._EDGE_PREFIX + edge.get_edge_name() + EnvironmentUtils._SPACE_SEPARATOR + first_vertex_name
            + EnvironmentUtils._SPACE_SEPARATOR +
            second_vertex_name + EnvironmentUtils._SPACE_SEPARATOR + EnvironmentUtils._WEIGHT_PREFIX + str(
                edge.get_weight()))

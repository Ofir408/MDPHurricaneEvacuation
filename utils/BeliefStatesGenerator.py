import copy
from typing import List, Tuple, Dict

from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.BeliefState import BeliefState
from data_structures.Edge import Edge


class BeliefStatesGenerator:

    @staticmethod
    def __has_vertex_in_possible_blocked(vertex_name: str, possible_blocked_edges: List[Edge]) -> Tuple[bool, str]:
        for possible_blocked_edge in possible_blocked_edges:
            vertices = possible_blocked_edge.get_vertex_names()
            vertex_name = vertex_name.replace("#V", "")
            if vertex_name in vertices:
                return True, possible_blocked_edge.get_edge_name()
        return False, ""

    @staticmethod
    def __get_unblocked_edges(edges_dict: Dict[str, Edge]) -> Dict[str, Edge]:
        return {k: v for k, v in edges_dict.items() if v.get_blockages_probability() > 0}

    @staticmethod
    def __set_unknown_edges(edges: List[Edge]):
        for edge in edges:
            edge.set_blockages_probability(-1)
        return edges

    @staticmethod
    def generate_states(env_config: EnvironmentConfiguration) -> List[BeliefState]:
        states = []
        possible_blocked_edges = [edge for edge in env_config.get_edges().values() if
                                  edge.get_blockages_probability() > 0]
        names_of_vertices = env_config.get_vertexes().keys()
        unblocked_edges = BeliefStatesGenerator.__get_unblocked_edges(env_config.get_edges())

        for vertex_name in names_of_vertices:
            temp_edges_dict = copy.deepcopy(unblocked_edges)
            has_edge, edge_name = BeliefStatesGenerator.__has_vertex_in_possible_blocked(vertex_name,
                                                                                         possible_blocked_edges)
            if has_edge:
                for possible_value in [0, 1]:
                    temp_edges_dict[edge_name].set_blockages_probability(possible_value)
                    states.append(BeliefState(vertex_name, list(temp_edges_dict.values())))
            else:
                states.append(
                    BeliefState(vertex_name, BeliefStatesGenerator.__set_unknown_edges(list(temp_edges_dict.values()))))
        return states

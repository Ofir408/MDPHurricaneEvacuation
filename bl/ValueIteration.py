import copy
from typing import List, Dict

from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.BeliefState import BeliefState
from data_structures.TransitionProbability import TransitionProbability


class ValueIteration:
    __CONVERGE_DISTANCE = 0.00000001
    __GAMA = 1

    def __init__(self, transition_distributions: List[TransitionProbability], states_dict: Dict[BeliefState, float]):
        self.__transition_distributions = transition_distributions
        self.__states_dict = states_dict

    def value_iteration_algo(self, env_config: EnvironmentConfiguration):
        should_continue = True
        state_to_best_action_dict = {}
        while should_continue:
            prev_utilities = [v for v in self.__states_dict.values()]
            for state in self.__states_dict.keys():
                max_sum = -100000000000
                max_action = None
                for action in self.__get_possible_edges(state, env_config):
                    current_sum = self.__sum_possible_probabilities(state, action)
                    if current_sum > max_sum:
                        max_sum = current_sum
                        max_action = action

                r = self.__get_edge_distance(max_action, env_config) if not state.get_is_goal() else 0
                current_utility = r + ValueIteration.__GAMA * max_sum
                state_to_best_action_dict[state] = max_action
                self.__update_utility(state, current_utility)
            should_continue = not self.__is_converge(list(self.__states_dict.values()), list(prev_utilities))
        return state_to_best_action_dict, self.__states_dict

    def __is_converge(self, current_utilities: List[float], prev_utilities: List[float]) -> bool:
        if current_utilities is None or prev_utilities is None:
            return False
        for a, b in zip(current_utilities, prev_utilities):
            if abs(a - b) >= ValueIteration.__CONVERGE_DISTANCE:
                return False
        return True

    def __get_possible_next_states(self, current_state: BeliefState, edge_name: str) -> List[BeliefState]:
        possible_next_states = []
        for transition_distribution in self.__transition_distributions:
            current_edge_name = transition_distribution.get_action().get_edge_name()
            if current_state == transition_distribution.get_given_belief_state() and edge_name == current_edge_name:
                required_state = transition_distribution.get_required_belief_state()
                possible_next_states.append(copy.deepcopy(required_state))
        return possible_next_states

    def __get_possible_edges(self, current_state: BeliefState, env_config: EnvironmentConfiguration) -> List[str]:
        current_vertex_name = current_state.get_vertex_name()
        vertices_dict = env_config.get_vertexes()
        current_vertex = vertices_dict[current_vertex_name]
        blocked_edges = []
        for edge in current_state.get_blockages_edges():
            if edge.get_blockages_probability() == 1:
                # Blocked edge
                blocked_edges.append(edge)
        blocked_edges_str = [edge.get_edge_name() for edge in blocked_edges]
        diff = [edge_name for edge_name in current_vertex.get_edges() if edge_name not in blocked_edges_str]
        return diff

    def __get_edge_distance(self, action_name: str, env_config: EnvironmentConfiguration) -> float:
        edges_dict = env_config.get_edges()
        return -edges_dict[action_name].get_weight()

    def __get_state_utility(self, state: BeliefState) -> float:
        return self.__states_dict[state]

    def __update_utility(self, state: BeliefState, new_utility: float):
        self.__states_dict[state] = new_utility

    def __get_transition_prob(self, given_state: BeliefState, next_state: BeliefState, action_name: str) -> float:
        for current_transition_distribution in self.__transition_distributions:
            is_same_current_state = current_transition_distribution.get_given_belief_state() == given_state
            is_same_next_state = current_transition_distribution.get_required_belief_state() == next_state
            is_same_action = current_transition_distribution.get_action().get_edge_name() == action_name
            is_given_goal = given_state.get_is_goal()
            if is_same_current_state and is_same_next_state and is_same_action and not is_given_goal:
                return current_transition_distribution.get_prob()

        # Doesn't exists, the prob is 0
        return 0

    def __sum_possible_probabilities(self, state: BeliefState, edge_name: str):
        possible_next_states = self.__get_possible_next_states(state, edge_name)
        total_prob_sum = 0.0
        for next_state in possible_next_states:
            next_state_utility = self.__get_state_utility(next_state)
            transition_utility = self.__get_transition_prob(state, next_state, edge_name)
            current_prob = next_state_utility * transition_utility
            total_prob_sum += current_prob / len(possible_next_states)
        return total_prob_sum

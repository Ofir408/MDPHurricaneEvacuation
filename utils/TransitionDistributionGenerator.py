import copy
from typing import List

from data_structures.BeliefState import BeliefState
from data_structures.Edge import Edge
from data_structures.TransitionProbability import TransitionProbability


class TransitionDistributionGenerator:

    @staticmethod
    def generate_distributions(possible_states: List[BeliefState], possible_edges: List[Edge]) -> List[
        TransitionProbability]:
        transition_probability_list = []
        for given_state in possible_states:
            left_states = [state for state in possible_states if
                           state.get_vertex_name() != given_state.get_vertex_name()]
            # left_states.remove(given_state)
            transition_probability_list += TransitionDistributionGenerator.__generate_distributions(given_state,
                                                                                                    left_states,
                                                                                                    possible_edges)
        return transition_probability_list

    @staticmethod
    def __generate_distributions(given_state: BeliefState, possible_states: List[BeliefState],
                                 possible_edges: List[Edge]) -> List[TransitionProbability]:
        transition_probability_list = []
        for possible_state in possible_states:
            for possible_edge in possible_edges:
                transition_prob = TransitionProbability(possible_state, given_state, possible_edge)
                prob = TransitionDistributionGenerator.__calc_prob(transition_prob, possible_edges)
                if prob != 0:
                    transition_prob.set_prob(prob)
                    transition_probability_list.append(copy.deepcopy(transition_prob))
        return transition_probability_list

    @staticmethod
    def __find_edges_diff(given_state: BeliefState, required_state: BeliefState) -> List[Edge]:
        given_state_edges = given_state.get_blockages_edges()
        required_state_edges = required_state.get_blockages_edges()
        required_vertex_name = required_state.get_vertex_name().replace("#V", "")
        edges_diff_list = [x for x in required_state_edges if
                           x not in given_state_edges]
        # filter states that are unknown although in the given state are known.
        return list(edges_diff_list)

    @staticmethod
    def __is_blocked(state: BeliefState, edge: Edge):
        state_edges = state.get_blockages_edges()
        return edge in state_edges

    @staticmethod
    def __is_valid(given_state: BeliefState, required_state: BeliefState):
        required_state_blockages_edges = required_state.get_blockages_edges()
        given_state_blockages_edges = given_state.get_blockages_edges()
        for required_edge in required_state_blockages_edges:
            for given_state_edge in given_state_blockages_edges:
                if required_edge.get_edge_name() == given_state_edge.get_edge_name():
                    if given_state_edge.get_blockages_probability() == 0 and required_edge.get_blockages_probability() != 0:
                        return False
                    if given_state_edge.get_blockages_probability() == 1 and required_edge.get_blockages_probability() != 1:
                        return False
        return True

    @staticmethod
    def __calc_prob(transition_prob: TransitionProbability, possible_edges: List[Edge]) -> float:
        required_state = transition_prob.get_required_belief_state()
        action = transition_prob.get_action()
        given_state = transition_prob.get_given_belief_state()
        required_vertex_name = required_state.get_vertex_name().replace("#V", "")
        given_vertex_name = given_state.get_vertex_name().replace("#V", "")
        action_vertices = action.get_vertex_names()

        if required_vertex_name not in action_vertices or given_vertex_name not in action_vertices \
                or not TransitionDistributionGenerator.__is_valid(given_state, required_state):
            return 0  # not a possible state given action & current state
        else:
            prob = 1.0
            blockage_prob = 1.0
            edges_diff = TransitionDistributionGenerator.__find_edges_diff(given_state, required_state)
            for edge in edges_diff:
                for possible_edge in possible_edges:
                    if possible_edge.get_edge_name() == edge.get_edge_name():
                        blockage_prob = possible_edge.get_blockages_probability()
                prob *= blockage_prob if edge.get_is_blocked_prob_calc() else 1 - blockage_prob
            return prob

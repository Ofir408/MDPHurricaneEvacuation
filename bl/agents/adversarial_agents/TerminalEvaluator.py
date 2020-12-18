"""
Evaluates the score of an agent given the state
"""
from typing import Tuple, Dict

from data_structures.State import State
from data_structures.Vertex import Vertex


class TerminalEvaluator:

    @staticmethod
    def adversarial_utility_eval(scores: Tuple[int, int], is_agent1_turn: bool) -> Tuple[int, int]:
        first_player_score, second_player_score = scores
        first_player_adversarial_score = first_player_score - second_player_score
        second_player_adversarial_score = second_player_score - first_player_score
        if is_agent1_turn:
            return first_player_adversarial_score, second_player_adversarial_score
        return second_player_adversarial_score, first_player_adversarial_score

    @staticmethod
    def semi_cooperative_utility_eval(scores: Tuple[int, int], is_agent1_turn: bool) -> Tuple[int, int]:
        first_player_score, second_player_score = scores
        if is_agent1_turn:
            return first_player_score, second_player_score
        return second_player_score, first_player_score

    @staticmethod
    def full_cooperative_utility_eval(scores: Tuple[int, int]) -> Tuple[int, int]:
        first_player_score, second_player_score = scores
        common_score = first_player_score + second_player_score
        return common_score, common_score  # the score of each player is common_score

    @staticmethod
    def are_no_more_people(state: State):
        has_unvisited_state = False in state.get_required_vertexes().values()
        return not has_unvisited_state

    @staticmethod
    def was_deadline_passed(state: State, deadline):
        return state.get_cost() > deadline

    @staticmethod
    def cut_off_utility_eval(state: State, is_agent1_player: bool, vertexes_dict: Dict[str, Vertex]) -> Tuple[int, int]:
        left_vertexes_to_visit = [state_name for state_name in state.get_required_vertexes().keys()
                                  if not state.get_required_vertexes()[state_name]]
        left_people_to_visit = 0
        for left_vertex_to_visit in left_vertexes_to_visit:
            left_people_to_visit += vertexes_dict[left_vertex_to_visit].get_people_num()

        agent1_player_score, agent2_player_score = state.get_scores_of_agents()
        if is_agent1_player:
            agent1_player_score += left_people_to_visit
        else:
            agent2_player_score += left_people_to_visit
        print("cut_off= ", str((agent1_player_score, agent2_player_score)))
        if is_agent1_player:
            return agent1_player_score, agent2_player_score
        return agent2_player_score, agent1_player_score

    @staticmethod
    def terminate_eval(state: State, mode: str, is_agent1_turn: bool) -> Tuple[int, int]:
        if mode == 'adversarial':
            return TerminalEvaluator.adversarial_utility_eval(state.get_scores_of_agents(), is_agent1_turn)
        if mode == "semi-cooperative":
            return TerminalEvaluator.semi_cooperative_utility_eval(state.get_scores_of_agents(), is_agent1_turn)
        else:
            # cooperative mode
            return TerminalEvaluator.full_cooperative_utility_eval(state.get_scores_of_agents())

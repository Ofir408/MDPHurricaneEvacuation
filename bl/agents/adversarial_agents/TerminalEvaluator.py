"""
Evaluates the score of an agent given the state
"""
from typing import Tuple, Dict

from data_structures.State import State
from data_structures.Vertex import Vertex


class TerminalEvaluator:

    @staticmethod
    def adversarial_utility_eval(scores: Tuple[int, int]) -> Tuple[int, int]:
        first_player_score, second_player_score = scores
        first_player_adversarial_score = first_player_score - second_player_score
        second_player_adversarial_score = second_player_score - first_player_score
        return first_player_adversarial_score, second_player_adversarial_score

    @staticmethod
    def semi_cooperative_utility_eval(scores: Tuple[int, int]) -> Tuple[int, int]:
        first_player_score, second_player_score = scores
        return first_player_score, second_player_score

    @staticmethod
    def full_cooperative_utility_eval(scores: Tuple[int, int], _: bool) -> Tuple[int, int]:
        first_player_score, second_player_score = scores
        common_score = first_player_score + second_player_score
        return common_score, common_score  # the score of each player is common_score

    @staticmethod
    def should_terminate(state: State):
        has_unvisited_state = False in state.get_required_vertexes().values()
        return not has_unvisited_state

    @staticmethod
    def cut_off_utility_eval(state: State, is_max_player: bool, vertexes_dict: Dict[str, Vertex]) -> Tuple[int, int]:
        left_vertexes_to_visit = [state_name for state_name in state.get_required_vertexes().keys()
                                  if not state.get_required_vertexes()[state_name]]
        left_people_to_visit = 0
        for left_vertex_to_visit in left_vertexes_to_visit:
            left_people_to_visit += vertexes_dict[left_vertex_to_visit].get_people_num()

        max_player_score, min_player_score = state.get_scores_of_agents()
        if is_max_player:
            max_player_score += left_people_to_visit
        else:
            min_player_score += left_people_to_visit
        return max_player_score, min_player_score

    @staticmethod
    def terminate_eval(state: State, mode: str, is_max_player: bool) -> Tuple[int, int]:
        if mode == 'adversarial':
            print("terminated state, utility= ",
                  TerminalEvaluator.adversarial_utility_eval(state.get_scores_of_agents()))
            return TerminalEvaluator.adversarial_utility_eval(state.get_scores_of_agents())
        if mode == "semi_cooperative":
            return TerminalEvaluator.semi_cooperative_utility_eval(state.get_scores_of_agents())
        else:
            # cooperative mode
            return TerminalEvaluator.full_cooperative_utility_eval(state.get_scores_of_agents(), is_max_player)

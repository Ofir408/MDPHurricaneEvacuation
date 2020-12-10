import copy
from typing import Tuple

from bl.agents.IAgent import IAgent
from bl.agents.adversarial_agents.TerminalEvaluator import TerminalEvaluator
from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.Edge import Edge
from data_structures.State import State
from data_structures.Vertex import Vertex
from utils.EnvironmentUtils import EnvironmentUtils


class MiniMaxAgent(IAgent):
    TRAVELLING = "TRAVELLING"
    ADVERSARIAL_MODE = "adversarial"
    SEMI_COOPERATIVE_MODE = "semi-cooperative"
    COOPERATIVE_MODE = "full-cooperative"

    def __init__(self, mode: str, cut_off_depth: int):
        super().__init__()
        self.__mode = mode
        self.__cut_off_depth = cut_off_depth
        self.__is_max_player = True

    def get_action(self, percepts: Tuple[State, EnvironmentConfiguration]) -> str:
        if self.is_travelling():
            self._distance_left_to_travel -= 1  # Travel this step
            return MiniMaxAgent.TRAVELLING

        initial_state, env_config = percepts
        print("initial_state= ", initial_state)
        best_action, best_utility = self.minimax(initial_state, "", self.__cut_off_depth, -10000000, 10000000,
                                                 self.__is_max_player, env_config)
        print("max_player? {0}, best_action={1}, best_utility={2}".format(self.__is_max_player, best_action,
                                                                          best_utility))
        if best_action is None:
            self._was_terminated = True
        else:
            self._distance_left_to_travel = env_config.get_edges()[best_action].get_weight()
        if initial_state.get_cost() + env_config.get_edges()[best_action].get_weight() > env_config.get_deadline():
            self._was_terminated = True
            return None
        return best_action

    def step_cost(self, parent_node: Vertex, action: Edge, new_node: Vertex) -> int:
        return action.get_weight()

    def minimax(self, state: State, action_to_state: str, depth: int, alpha: int, beta: int, is_max_player: bool,
                env_config: EnvironmentConfiguration):
        if TerminalEvaluator.was_deadline_passed(state, env_config.get_deadline()):
            return None, TerminalEvaluator.terminate_eval(state.get_parent_state(), self.__mode, is_max_player)
        if TerminalEvaluator.are_no_more_people(state):
            return action_to_state, TerminalEvaluator.terminate_eval(state, self.__mode, is_max_player)
        if depth == 0:
            return action_to_state, TerminalEvaluator.cut_off_utility_eval(state, is_max_player,
                                                                           env_config.get_vertexes())
        possible_edges = EnvironmentUtils.get_possible_moves(state, env_config)
        possible_actions = [edge.get_edge_name() for edge in possible_edges]
        if is_max_player:
            # Max Player
            best_action = None
            max_utility_value = -10000000
            max_opponent_utility = -10000000
            best_score = None

            for action in possible_actions:
                possible_next_state = self.__result(action, copy.deepcopy(state), is_max_player, env_config)
                is_max_next_player = False if self.__mode == MiniMaxAgent.ADVERSARIAL_MODE else True
                new_action, scores = self.minimax(copy.deepcopy(possible_next_state), action, depth - 1, alpha, beta,
                                                  is_max_next_player, env_config)
                print("cost of possible_next_state = ", possible_next_state.get_cost())
                current_utility, opponent_utility = scores
                if self.__is_better_score(max_utility_value, current_utility, max_opponent_utility, opponent_utility):
                    max_utility_value = current_utility
                    max_opponent_utility = opponent_utility
                    best_score = scores
                    best_action = action
                alpha = max(alpha, current_utility)
                if self.__mode == MiniMaxAgent.ADVERSARIAL_MODE and beta <= alpha:
                    break
            return best_action, best_score

        else:
            # Min Player
            min_utility_value = 10000000
            best_action = None
            best_score = None

            for action in possible_actions:
                possible_next_state = self.__result(action, state, is_max_player, env_config)
                _, scores = self.minimax(copy.deepcopy(possible_next_state), action, depth - 1, alpha, beta, True,
                                         env_config)
                current_utility = scores[1]  # score of the minimum player
                if current_utility < min_utility_value:
                    min_utility_value = current_utility
                    best_score = scores
                    best_action = action
                beta = min(beta, current_utility)
                if self.__mode == MiniMaxAgent.ADVERSARIAL_MODE and beta <= alpha:
                    break
            return best_action, best_score

    def __is_better_score(self, max_utility_value, current_utility, max_opponent_utility, opponent_utility):
        # Checking for semi-cooperative agent
        semi_cooperative_check = self.__mode == MiniMaxAgent.SEMI_COOPERATIVE_MODE and \
                                 max_utility_value == current_utility and max_opponent_utility < opponent_utility
        normal_check = current_utility > max_utility_value
        return semi_cooperative_check or normal_check

    def __result(self, action: str, state: State, is_max: bool, env_config: EnvironmentConfiguration) -> State:
        """

        :param action: edge name
        :param state: current state
        :return: next state after moving on edge action from the given state
        """
        next_vertex = env_config.get_vertexes()[state.get_current_vertex_name()]
        next_vertex.set_state(state)
        return EnvironmentUtils.get_next_vertex(next_vertex, action, self.step_cost, env_config, is_max).get_state()

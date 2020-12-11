import copy
from typing import Tuple

from bl.agents.IAgent import IAgent
from bl.agents.adversarial_agents.GameState import GameState
from bl.agents.adversarial_agents.TerminalEvaluator import TerminalEvaluator
from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.Edge import Edge
from data_structures.State import State
from data_structures.Vertex import Vertex
from utils.EnvironmentUtils import EnvironmentUtils


class MiniMaxAgent(IAgent):
    TRAVELLING = "TRAVELLING"
    DONE = "DONE"
    ADVERSARIAL_MODE = "adversarial"
    SEMI_COOPERATIVE_MODE = "semi-cooperative"
    FULL_COOPERATIVE_MODE = "full-cooperative"

    def __init__(self, mode: str, cut_off_depth: int):
        super().__init__()
        self.__mode = mode
        self.__cut_off_depth = cut_off_depth
        self.__is_max_player = True

    def get_action(self, percepts: Tuple[GameState, EnvironmentConfiguration]) -> str:
        if self.is_travelling():
            self._distance_left_to_travel -= 1  # Travel this step
            if self._distance_left_to_travel == 0:
                return MiniMaxAgent.DONE
            return MiniMaxAgent.TRAVELLING

        game_state, env_config = percepts
        print("initial_game_state= ", game_state)
        best_action, best_utility = self.minimax(game_state, self.__is_max_player, "", self.__cut_off_depth, -10000000,
                                                 10000000, env_config)
        print("is_agent1={0}, best_action={1}, best_utility={2}".format(game_state.get_is_agent1_turn(), best_action,
                                                                        best_utility))
        if best_action is None:
            self._was_terminated = True
        else:
            self._distance_left_to_travel = env_config.get_edges()[best_action].get_weight()
        initial_state = game_state.get_agent1_state() if game_state.get_is_agent1_turn() else game_state.get_agent2_state()
        if initial_state.get_cost() + env_config.get_edges()[best_action].get_weight() > env_config.get_deadline():
            self._was_terminated = True
            return None
        return best_action

    def step_cost(self, parent_node: Vertex, action: Edge, new_node: Vertex) -> int:
        return action.get_weight()

    def minimax(self, game_state: GameState, is_max_player: bool, action_to_state: str, depth: int, alpha: int,
                beta: int, env_config: EnvironmentConfiguration):
        current_agent_state = game_state.get_current_state()
        is_agent1_turn = game_state.get_is_agent1_turn()

        if TerminalEvaluator.was_deadline_passed(current_agent_state, env_config.get_deadline()):
            return None, TerminalEvaluator.terminate_eval(current_agent_state.get_parent_state(), self.__mode,
                                                          is_agent1_turn)
        if TerminalEvaluator.are_no_more_people(current_agent_state):
            return action_to_state, TerminalEvaluator.terminate_eval(current_agent_state, self.__mode, is_agent1_turn)
        if depth == 0:
            return action_to_state, TerminalEvaluator.cut_off_utility_eval(current_agent_state, is_agent1_turn,
                                                                           env_config.get_vertexes())
        possible_edges = EnvironmentUtils.get_possible_moves(current_agent_state, env_config)
        possible_actions = [edge.get_edge_name() for edge in possible_edges]
        if is_max_player:
            # Max Player
            best_action = None
            max_utility_value = -10000000
            max_opponent_utility = -10000000
            best_score = None

            for action in possible_actions:
                possible_next_state = self.__result(action, copy.deepcopy(current_agent_state), is_max_player,
                                                    env_config)
                is_max_next_player = True if self.__mode == MiniMaxAgent.FULL_COOPERATIVE_MODE else False
                new_game_state = self.__get_next_game_state(game_state, possible_next_state)
                new_action, scores = self.minimax(copy.deepcopy(new_game_state), is_max_next_player, action,
                                                  depth - 1, alpha, beta, env_config)
                current_utility, opponent_utility = scores
                print("is_agent1={0}, best_action={1}, best_score={2} ".format(is_agent1_turn, best_action, best_score))
                if self.__is_better_score(max_utility_value, current_utility, max_opponent_utility, opponent_utility, is_max_player):
                    max_utility_value = current_utility
                    max_opponent_utility = opponent_utility
                    best_score = scores
                    best_action = action
                alpha = max(alpha, current_utility)
                if self.__mode == MiniMaxAgent.ADVERSARIAL_MODE and beta <= alpha:
                    break
            #print("is_agent1={0}, best_action={1}, best_score={2} ".format(is_agent1_turn, best_action, best_score))
            return best_action, best_score

        else:
            # Min Player
            min_utility_value = 10000000
            max_opponent_utility = -1000000
            best_action = None
            best_score = None

            for action in possible_actions:
                possible_next_state = self.__result(action, current_agent_state, is_max_player, env_config)
                new_game_state = self.__get_next_game_state(game_state, possible_next_state)
                _, scores = self.minimax(copy.deepcopy(new_game_state), True, action,
                                         depth - 1, alpha, beta, env_config)
                current_utility, opponent_utility = scores
                # TODO: add is better score for semi-cooperative here.
                if self.__is_better_score(min_utility_value, current_utility, max_opponent_utility, opponent_utility, is_max_player):
                    min_utility_value = current_utility
                    max_opponent_utility = opponent_utility
                    best_score = scores
                    best_action = action
                beta = min(beta, current_utility)
                if self.__mode == MiniMaxAgent.ADVERSARIAL_MODE and beta <= alpha:
                    break
            return best_action, best_score

    def __is_better_score(self, max_utility_value, current_utility, max_opponent_utility, opponent_utility, is_max):
        # Checking for semi-cooperative agent
        semi_cooperative_check = self.__mode == MiniMaxAgent.SEMI_COOPERATIVE_MODE and \
                                 max_utility_value == current_utility and max_opponent_utility < opponent_utility
        normal_check = current_utility > max_utility_value if is_max else current_utility < max_utility_value
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

    def __get_next_game_state(self, current_game_state: GameState, current_agent_next_state: State) -> GameState:
        is_agent1_current_turn = current_game_state.get_is_agent1_turn()
        next_agent_turn = not is_agent1_current_turn
        next_game = copy.deepcopy(current_game_state)
        if is_agent1_current_turn:
            next_game.set_agent1_state(current_agent_next_state)
        else:
            next_game.set_agent2_state(current_agent_next_state)
        next_game.set_is_agent1_turn(next_agent_turn)
        return next_game

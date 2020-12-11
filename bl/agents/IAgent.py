from abc import abstractmethod
from typing import Tuple

from bl.agents.ICostCalculator import ICostCalculator
from bl.agents.adversarial_agents.GameState import GameState
from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.State import State


class IAgent(ICostCalculator):

    def __init__(self):
        self._was_terminated = False
        self._distance_left_to_travel = 0

    @abstractmethod
    def get_action(self, percepts: Tuple[GameState, EnvironmentConfiguration]) -> str:
        """
        Should be implemented within each agent.
        :param percepts: percepts about the environment
                         composed from current GameState & EnvironmentConfiguration
        :return: the next edge name
        """
        pass

    def was_terminated(self) -> bool:
        return self._was_terminated

    def is_travelling(self) -> bool:
        if self._distance_left_to_travel == 0:
            return False
        else:
            return True

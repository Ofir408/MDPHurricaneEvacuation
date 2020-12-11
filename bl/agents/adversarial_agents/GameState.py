from data_structures.State import State


class GameState:
    def __init__(self, agent1_state: State, agent2_state: State):
        self.__agent1_state = agent1_state
        self.__agent2_state = agent2_state

    def get_agent1_state(self):
        return self.__agent1_state

    def get_agent2_state(self):
        return self.__agent2_state

    def set_agent1_state(self, new_state):
        self.__agent1_state = new_state

    def set_agent2_state(self, new_state):
        self.__agent2_state = new_state

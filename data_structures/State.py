from typing import Dict, Tuple


class State:
    """
    Represents a state, contains:
     1) names of vertexes with people that the agent has to go through them, with binary
    flag (did we reach everyone or not)
     2) scores_of_agents the scores of the agents in that state.
     3) current vertex name.
    """

    def __init__(self, current_vertex_name: str, scores_of_agents: Tuple[int, int],
                 required_vertexes: Dict[str, bool] = None, cost: int = 0, parent_state=None, distance: int = 0):
        self.__current_vertex = current_vertex_name
        self.__scores_of_agents = scores_of_agents
        self.__required_vertexes = required_vertexes
        self.__cost = cost
        self.__parent_state = parent_state
        self.__distance = distance

    def set_visited_vertex(self, vertex_name: str):
        if vertex_name in self.__required_vertexes:
            self.__required_vertexes[vertex_name] = True

    def set_required_vertexes(self, require_vertexes):
        self.__required_vertexes = require_vertexes

    def set_scores_of_agents(self, new_score: Tuple[int, int]):
        self.__scores_of_agents = new_score

    def set_cost(self, cost):
        self.__cost = cost

    def set_parent_state(self, parent_state):
        self.__parent_state = parent_state

    def set_distance(self, distance):
        self.__distance = distance

    def decrease_distance_by_one(self):
        self.__distance -= 1

    def get_required_vertexes(self):
        return self.__required_vertexes

    def get_current_vertex_name(self):
        return self.__current_vertex

    def get_scores_of_agents(self):
        return self.__scores_of_agents

    def get_cost(self):
        return self.__cost

    def get_parent_state(self):
        return self.__parent_state

    def get_distance(self):
        return self.__distance

    def __eq__(self, other):
        if other is None:
            return False
        return self.__current_vertex == other.get_current_vertex_name()

    def __str__(self) -> str:
        return "State={0}, Required State={1}, scores:{2}".format(self.__current_vertex, self.__required_vertexes,
                                                                  self.__scores_of_agents)

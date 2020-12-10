from typing import List

from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.State import State


class StateUtils:

    @staticmethod
    def get_saved_people_num(state: State, current_traveled_states, env_conf: EnvironmentConfiguration) -> int:
        score = 0
        new_traveled_vertexes = [vertex_name for vertex_name in StateUtils.get_state_traveled_vertexes(state) if
                                 vertex_name not in current_traveled_states]
        for x in StateUtils.get_state_traveled_vertexes(state):
            current_traveled_states.append(x)
        vertexes_dict = env_conf.get_vertexes()
        for vertex in new_traveled_vertexes:
            score += vertexes_dict[vertex].get_people_num()
        return score

    @staticmethod
    def get_state_traveled_vertexes(state: State) -> List[str]:
        required_vertexes_dict = state.get_required_vertexes()
        return [vertex_name for vertex_name in required_vertexes_dict.keys()
                if required_vertexes_dict[vertex_name]]

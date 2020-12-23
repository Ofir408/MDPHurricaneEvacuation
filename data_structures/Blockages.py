from typing import List

from data_structures.Evacuees import Evacuees


class Blockages:
    def __init__(self, name: str, time: int, evacuees_dependencies: List[Evacuees],
                 blockages_dependencies: List['Blockages'], is_blocked_prob_calc,
                 probability: float = None):
        self.__name = name
        self.__time = time
        self.__evacuees_dependencies = evacuees_dependencies
        self.__blockages_dependencies = blockages_dependencies
        self.__is_blocked_prob_calc = is_blocked_prob_calc
        self.__probability = probability

    def get_name(self):
        return self.__name

    def get_time(self):
        return self.__time

    def get_evacuees_dependencies(self):
        return self.__evacuees_dependencies

    def get_blockages_dependencies(self):
        return self.__blockages_dependencies

    def get_is_blocked_prob_calc(self):
        return self.__is_blocked_prob_calc

    def get_probability(self):
        return self.__probability

    def has_probability(self):
        return self.__probability is not None

    def set_probability(self, probability: float):
        self.__probability = probability

    def set_is_blocked_prob_calc(self, is_blocked_prob_calc: bool):
        self.__is_blocked_prob_calc = is_blocked_prob_calc

    def __eq__(self, other: 'Blockages'):
        same_name = self.__name == other.__name
        same_time = self.__time == other.__time
        same_evacuees_dependencies = self.__evacuees_dependencies == other.__evacuees_dependencies
        same_blockages_dependencies = self.__blockages_dependencies == other.__blockages_dependencies
        return same_name and same_time and same_evacuees_dependencies and same_blockages_dependencies

    # example format: P(Blockage 1 | not Evacuees 1, not Evacuees 2) = 0.001 or P(Blockage 1,1 | Blockage 1,0) = 0.001
    def __str__(self):
        if len(self.__evacuees_dependencies) > 0:
            s = "P(Blockage {0} | {1}Evacuees {2}, {3}Evacuees {4}) = {5}".format(
                self.__name + "," + str(self.__time),
                "" if self.__evacuees_dependencies[0].get_is_evacuees() else "NOT ",
                self.__evacuees_dependencies[0].get_vertex_name(),
                "" if self.__evacuees_dependencies[1].get_is_evacuees() else "NOT ",
                self.__evacuees_dependencies[1].get_vertex_name(),
                round(self.__probability, 3)
            )
        else:
            s = "P(Blockage {0} | {1}Blockage {2}) = {3}".format(
                self.__name + "," + str(self.__time),
                "" if self.__blockages_dependencies[-1].__is_blocked_prob_calc else "NOT ",
                self.__blockages_dependencies[-1].get_name() + "," + str(self.__time - 1), round(self.__probability, 3)
            )
        return s

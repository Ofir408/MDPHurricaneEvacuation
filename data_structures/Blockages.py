from typing import List

from data_structures.Evacuees import Evacuees


class Blockages:
    # TODO: is_blocked should be without a default value?
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
        return self.__name == other.__name and self.__time == other.__time \
               and self.__is_blocked_prob_calc == other.__is_blocked_prob_calc \
               and self.__evacuees_dependencies == other.__evacuees_dependencies \
               and self.__blockages_dependencies == other.__blockages_dependencies

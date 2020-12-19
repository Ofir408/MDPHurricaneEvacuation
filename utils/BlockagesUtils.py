import copy
from typing import List

from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.Blockages import Blockages
from data_structures.Evacuees import Evacuees


class BlockagesUtils:
    SPONTANEOUS_PROBABILITY = 0.001
    LEAKAGE_PROBABILITY = 0.001

    @staticmethod
    def persistence_probability_calc(blockages: Blockages, env_config: EnvironmentConfiguration) -> float:
        # leakage probability of 0.001, when all the causes are inactive
        if BlockagesUtils.__is_spontaneous_blockage(blockages.get_blockages_dependencies()):
            return BlockagesUtils.SPONTANEOUS_PROBABILITY
        return env_config.get_persistence()

    @staticmethod
    def noisy_or_probability_calc(blockages: Blockages, env_config: EnvironmentConfiguration) -> float:
        probability = 1.0
        evacuees = blockages.get_evacuees_dependencies()
        names_of_evacuees = [evacuee.get_vertex_name() for evacuee in evacuees]
        previous_blockage_prob = []
        BlockagesUtils.__add_noisy_or_base_cases(blockages.get_name(), previous_blockage_prob, evacuees, env_config)
        truth_evacuees = [evacuee for evacuee in evacuees if evacuee.get_is_evacuees()]

        if blockages in previous_blockage_prob:
            inx = previous_blockage_prob.index(blockages)
            return previous_blockage_prob[inx].get_probability()

        for truth_evacuee in truth_evacuees:
            current_blockages = BlockagesUtils.__build_blockages_for_noisy_or(blockages.get_name(), names_of_evacuees,
                                                                              truth_evacuee.get_vertex_name(), 0)
            current_probability = BlockagesUtils.__get_probability_from_previous_blockage(current_blockages,
                                                                                          previous_blockage_prob)
            probability = probability * (1 - current_probability)
        truth_probability = 1 - probability
        return truth_probability

    @staticmethod
    def __add_noisy_or_base_cases(blockage_name, previous_blockage_prob: List[Blockages], evacuees: List[Evacuees],
                                  env_config: EnvironmentConfiguration):
        names_of_evacuees = []
        for evacuee in evacuees:
            names_of_evacuees.append(evacuee.get_vertex_name())

        # add leakage case
        false_evacuees = []
        for evacuee_name in names_of_evacuees:
            false_evacuees.append(Evacuees(False, evacuee_name))
        blockages = Blockages(blockage_name, 0, false_evacuees, [], False, 1 - BlockagesUtils.LEAKAGE_PROBABILITY)
        previous_blockage_prob.append(copy.deepcopy(blockages))

        for evacuee_name in names_of_evacuees:
            blockages = BlockagesUtils.__build_blockages_for_noisy_or(blockage_name, names_of_evacuees, evacuee_name, 0)
            # calculate the probability
            edge_name = blockages.get_name()
            edge_weight = env_config.get_edges()[edge_name].get_weight()
            probability = BlockagesUtils.__pi(edge_weight)
            blockages.set_probability(probability)
            blockages.set_is_blocked_prob_calc(False)
            previous_blockage_prob.append(copy.deepcopy(blockages))

    @staticmethod
    def __get_probability_from_previous_blockage(required_blockage: Blockages, previous_blockage_prob: List[Blockages]):
        for current_blockages in previous_blockage_prob:
            if required_blockage.__eq__(current_blockages):
                return current_blockages.get_probability()
        print("Not found!!!")
        return None

    @staticmethod
    def __is_spontaneous_blockage(blockages: List[Blockages]):
        blockage = blockages[-1]
        return not blockage.get_is_blocked_prob_calc()

    @staticmethod
    def __is_incident(evacuees: List[Evacuees]):
        return len([True for x in evacuees if x.get_is_evacuees()]) == 1

    @staticmethod
    def __is_leakage(evacuees: List[Evacuees]):
        for evacuee in evacuees:
            if evacuee.get_is_evacuees():
                return False
        return True

    @staticmethod
    def __pi(edge_weight: float) -> float:
        return 0.6 * 1 / edge_weight

    @staticmethod
    def __build_blockages_for_noisy_or(blockage_name: str, names_of_evacuees: List[str], truth_evacuee_name: str,
                                       time: int) -> Blockages:
        evacuees = []
        temp = copy.deepcopy(names_of_evacuees)
        truth_evacuee = Evacuees(True, truth_evacuee_name)
        evacuees.append(truth_evacuee)
        temp.remove(truth_evacuee_name)
        for evacuee_name in temp:
            evacuees.append(Evacuees(False, evacuee_name))
        blockage = Blockages(blockage_name, time, evacuees, [], False)
        return blockage

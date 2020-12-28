import copy
from typing import List

from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.Blockages import Blockages
from data_structures.Evacuees import Evacuees
from data_structures.Var import Var
from utils.BlockagesUtils import BlockagesUtils


class BayesianNetworkBL:
    def __init__(self, env_config: EnvironmentConfiguration):
        self.__env_config = env_config
        self.__blockages = []
        self.__evacuees = []
        self.__time = 0

    def build_bayes_network(self, time_limit: int):
        self.__build_evacuees()
        while self.__time < time_limit:
            self.__build_blockages()
            self.__time += 1
            print("\n------------------- TIME={0} Ended -----------------------\n".format(self.__time - 1))

    def get_from_bn(self, var: Var, evidence_list: List[Var]) -> float:
        name = var.get_name()
        is_true = var.is_true()
        # TODO: calc by the evidence list - find the bug here... & simplify.
        for evidence in evidence_list:
            if evidence.get_is_user_evidence() and evidence.get_name() == name:
                if evidence.is_true() == is_true:
                    return 1.0
                else:
                    return 0.0

        for evacuee in self.__evacuees:
            if evacuee.get_name() == name:
                if evacuee.is_true() and is_true:
                    return evacuee.get_probability()
                if not evacuee.is_true() and not is_true:
                    return evacuee.get_probability()
                return 1 - evacuee.get_probability()
        for blockage in self.get_blockages():
            if blockage.get_name() == name and self.__is_same_blockages_dependencies(evidence_list, blockage):
                if blockage.is_true() and is_true:
                    return blockage.get_probability()
                if not blockage.is_true() and not is_true:
                    return blockage.get_probability()
                return 1 - blockage.get_probability()
        return 0.001

    def __is_same_blockages_dependencies(self, evidence_list: List[Var], blockage: Blockages):
        blockage_dependencies = blockage.get_blockages_dependencies()
        evacuees_dependencies = blockage.get_evacuees_dependencies()
        for current_blockage in blockage_dependencies:
            current_name = current_blockage.get_name()
            current_is_true = current_blockage.is_true()
            temp = Var(current_name)
            temp.set_value(current_is_true)
            if not self.check_if_exist(temp, evidence_list):
                return False

        for current_evacuee in evacuees_dependencies:
            current_name = "#V" + current_evacuee.get_name()
            current_is_true = current_evacuee.is_true()
            temp = Var(current_name)
            temp.set_value(current_is_true)
            if not self.check_if_exist(temp, evidence_list):
                return False
        return True

    def check_if_exist(self, var: Var, evidence_list: List[Var]):
        name = var.get_name()
        is_true = var.is_true()
        for evidence in evidence_list:
            current_evidence_name = evidence.get_name()
            current_evidence_is_true = evidence.is_true()
            if current_evidence_name == name and current_evidence_is_true == is_true:
                return True
        return False

    def get_y_value_from_e(self, var: Var, evidence_list: List[Var]):
        name = var.get_name()
        for evidence in evidence_list:
            current_evidence_name = evidence.get_name()
            if not evidence.get_is_user_evidence() and current_evidence_name == name:
                return evidence.is_true()
        return None

    def topological_sorter(self) -> List[Var]:
        """
        :return: List of vars (blockages & evacuees) in a topological order.
        """
        # V1, V2, V3, V4, E1,0 , E2,0 , E3,0 , E4,0, E1,1 , E2,1 , E3,1 , E4,1
        time_one = []
        time_zero = []
        for blockage_list in self.__blockages:
            for blockage in blockage_list:
                if blockage.get_time() == 0 and not self.is_blockage_exist(blockage, time_zero):
                    time_zero.append(copy.deepcopy(blockage))
                if blockage.get_time() == 1 and not self.is_blockage_exist(blockage, time_one):
                    time_one.append(copy.deepcopy(blockage))
        # sorted_topological = time_one + time_zero + self.__evacuees
        sorted_topological = self.__evacuees + time_zero + time_one
        return sorted_topological

    def is_blockage_exist(self, blockages: Blockages, blockages_list: List[Blockages]):
        name = blockages.get_name()
        for current_blockages in blockages_list:
            if name == current_blockages.get_name():
                return True
        return False

    def get_evacuees(self) -> List[Evacuees]:
        return self.__evacuees

    def get_blockages(self) -> List[Blockages]:
        blockages_list = []
        for current_blockages_list in self.__blockages:
            blockages_list += current_blockages_list
        return blockages_list

    def __build_evacuees(self):
        for vertex_name, vertex in self.__env_config.get_vertexes().items():
            self.__evacuees.append(Evacuees(True, vertex_name, vertex.get_evacuees_probability()))
        for evacuee in self.__evacuees:
            print(evacuee)

    def __build_blockages(self):
        possible_blockages = [edge_name for edge_name in self.__env_config.get_edges().keys()]
        for blockages_name in possible_blockages:
            self.__get_blockages_dependencies(blockages_name)

    def __get_blockages_dependencies(self, blockages_name: str):
        result = []
        print("EDGE {0}, TIME= {1}:".format(blockages_name, self.__time))
        if self.__time == 0:
            # noisy or
            first_vertex_name, second_vertex_name = self.__env_config.get_edges()[blockages_name].get_vertex_names()
            possible_is_evacuees_values = [[True, True], [True, False], [False, True], [False, False]]
            for x, y in possible_is_evacuees_values:
                evacuees_dependencies = [Evacuees(x, first_vertex_name), Evacuees(y, second_vertex_name)]
                blockages = Blockages(blockages_name + "," + str(self.__time), self.__time, evacuees_dependencies, [],
                                      True)
                probability = BlockagesUtils.noisy_or_probability_calc(blockages, self.__env_config)
                blockages.set_probability(probability)
                print(blockages)
                result.append(copy.deepcopy(blockages))
            self.__blockages.append(result)
        else:
            possible_values = [True, False]
            for x in possible_values:
                prev_blockages = Blockages(blockages_name + "," + str(self.__time - 1), self.__time - 1, [], [], x)
                blockages = Blockages(blockages_name + "," + str(self.__time), self.__time, [], [prev_blockages], True)
                probability = BlockagesUtils.persistence_probability_calc(blockages, self.__env_config)
                blockages.set_probability(probability)
                print(blockages)
                result.append(copy.deepcopy(blockages))
            self.__blockages.append(result)

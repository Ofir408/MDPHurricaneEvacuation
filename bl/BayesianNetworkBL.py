import copy

from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.Blockages import Blockages
from data_structures.Evacuees import Evacuees
from utils.BlockagesUtils import BlockagesUtils

import itertools


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
        if self.__time == 0:
            # noisy or
            first_vertex_name, second_vertex_name = self.__env_config.get_edges()[blockages_name].get_vertex_names()
            possible_is_evacuees_values = [[True, True], [True, False], [False, True], [False, False]]
            print("possible_is_evacuees_values= ", possible_is_evacuees_values)
            for x, y in possible_is_evacuees_values:
                evacuees_dependencies = [Evacuees(x, first_vertex_name), Evacuees(y, second_vertex_name)]
                blockages = Blockages(blockages_name, self.__time, evacuees_dependencies, [], True)
                probability = BlockagesUtils.noisy_or_probability_calc(blockages, self.__env_config)
                blockages.set_probability(probability)
                print(
                    "time={0}, blockages_name= {1}, probability= {2}".format(self.__time, blockages_name, probability))
                result.append(copy.deepcopy(blockages))
            self.__blockages.append(result)
        else:
            possible_values = [True, False]
            for x in possible_values:
                prev_blockages = Blockages(blockages_name, self.__time - 1, [], [], x)
                blockages = Blockages(blockages_name, self.__time, [], [prev_blockages], True)
                probability = BlockagesUtils.persistence_probability_calc(blockages, self.__env_config)
                blockages.set_probability(probability)
                print(
                    "time={0}, blockages_name= {1}, probability= {2}".format(self.__time, blockages_name, probability))
                result.append(copy.deepcopy(blockages))
            self.__blockages.append(result)

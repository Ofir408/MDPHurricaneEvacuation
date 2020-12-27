import copy
from typing import List

from bl.BayesianNetworkBL import BayesianNetworkBL
from data_structures.Var import Var


class EnumerationAlgo:

    def enumeration_ask(self, x: Var, e: List[Var], bn: BayesianNetworkBL) -> List[float]:
        """

        :param x: query Var
        :param e: observed values for variables E
        :param bn: Bayesian network
        :return: distribution over X
        """
        distribution_x = []
        bn_vars = bn.topological_sorter()
        e_backup = copy.deepcopy(e)
        for possible_x_value in x.get_possible_values():
            e = copy.deepcopy(e_backup)
            x.set_value(possible_x_value)
            e.append(copy.deepcopy(x))
            result = self.__enumerate_all(bn_vars, e, bn)
            distribution_x.append(result)
            print("result= ", result)
        return self.__normalize(distribution_x)

    def __enumerate_all(self, variables: List[Var], e: List[Var], bn: BayesianNetworkBL) -> float:
        if len(variables) == 0:
            return 1.0
        y = variables[0]
        if y in e:
            left_vars = copy.deepcopy(variables)
            left_vars.remove(y)
            return bn.get_from_bn(y, e) * self.__enumerate_all(left_vars, e, bn)
        else:
            total_prob_sum = 0
            left_vars = copy.deepcopy(variables)
            left_vars.remove(y)
            for y_possible_value in y.get_possible_values():
                current_y = copy.deepcopy(y)
                current_y.set_value(y_possible_value)
                e.append(current_y)
                print("bn.get_from_bn(current_y, e)= ", bn.get_from_bn(current_y, e))
                temp = self.__enumerate_all(left_vars, e, bn)
                print("self.__enumerate_all(left_vars, e, bn)= ", temp)
                current_prob = bn.get_from_bn(current_y, e) * temp
                total_prob_sum += current_prob
                print("current_prob= ", current_prob)
            print("total_prob_sum= ", total_prob_sum)
            return total_prob_sum

    def __normalize(self, distributions: List[float]):
        print("distributions= ", distributions)
        total_sum = 0
        for distribution in distributions:
            total_sum += distribution
        normalized_list = [current_distribution / total_sum for current_distribution in distributions]
        return normalized_list

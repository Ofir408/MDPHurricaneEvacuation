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
        for possible_x_value in x.get_possible_values():
            x.set_value(possible_x_value)
            e_tag = copy.deepcopy(e)
            e_tag.append(copy.deepcopy(x))
            result = self.__enumerate_all(copy.deepcopy(bn_vars), copy.deepcopy(e_tag), copy.deepcopy(bn))
            distribution_x.append(result)
            print("result= ", result)
        return self.__normalize(distribution_x)

    def __enumerate_all(self, variables: List[Var], e: List[Var], bn: BayesianNetworkBL) -> float:
        if len(variables) == 0:
            return 1.0
        y = variables[0]
        y_value_from_e = bn.get_y_value_from_e(y, e)
        if y_value_from_e is not None:
            left_vars = copy.deepcopy(variables)
            left_vars.remove(y)
            y.set_value(y_value_from_e)
            return bn.get_from_bn(y, e) * self.__enumerate_all(left_vars, e, bn)

        else:
            total_prob_sum = 0
            left_vars = copy.deepcopy(variables)
            left_vars.remove(y)
            for y_possible_value in y.get_possible_values():
                current_y = copy.deepcopy(y)
                current_y.set_value(y_possible_value)
                e_tag = copy.deepcopy(e)
                e_tag.append(current_y)
                current_prob = bn.get_from_bn(current_y, e_tag) * self.__enumerate_all(left_vars, e_tag, bn)
                total_prob_sum += current_prob
            return total_prob_sum

    def __normalize(self, distributions: List[float]):
        print("distributions= ", distributions)
        total_sum = 0
        for distribution in distributions:
            total_sum += distribution
        normalized_list = [current_distribution / total_sum for current_distribution in distributions]
        return normalized_list

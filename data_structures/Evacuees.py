from data_structures.Var import Var


class Evacuees(Var):

    def __init__(self, is_evacuees: bool, vertex_name: str, probability: float = None):
        super().__init__(vertex_name)
        super().set_value(is_evacuees)
        self.__vertex_name = vertex_name
        self.__probability = probability

    def get_probability(self) -> float:
        return self.__probability

    def get_possible_values(self):
        return [True, False]

    def __eq__(self, other: 'Evacuees'):
        return self.__vertex_name == other._name and self._is_true == other._is_true

    # Example output format: P(Evacuees) = 0.2 or P(not Evacuees) = 0.8
    def __str__(self):
        vertex_name_str = "VERTEX {0}:\n".format(self.__vertex_name)
        is_evacuees_str = "" if self._is_true else "not "
        negative_is_evacuees_str = "" if not self._is_true else "not "
        probability_str = "" if self.__probability is None else "= {0}".format(str(self.__probability))
        negative_probability_str = "" if self.__probability is None else "= {0}".format(str(1.0 - self.__probability))
        return vertex_name_str + "P({0}Evacuees) {1}\n".format(is_evacuees_str,
                                                               probability_str) + "P({0}Evacuees) {1}\n".format(
            negative_is_evacuees_str, negative_probability_str)

class Evacuees:
    def __init__(self, is_evacuees: bool, vertex_name: str, probability: float = None):
        self.__is_evacuees = is_evacuees
        self.__vertex_name = vertex_name
        self.__probability = probability

    def get_is_evacuees(self):
        return self.__is_evacuees

    def get_vertex_name(self):
        return self.__vertex_name

    def get_probability(self):
        return self.__probability

    def __eq__(self, other: 'Evacuees'):
        return self.__vertex_name == other.__vertex_name and self.__is_evacuees == other.__is_evacuees

    # Example output format: P(Evacuees) = 0.2 or P(not Evacuees) = 0.8
    def __str__(self):
        vertex_name_str = "VERTEX {0}:\n".format(self.__vertex_name)
        is_evacuees_str = "" if self.__is_evacuees else "not "
        negative_is_evacuees_str = "" if not self.__is_evacuees else "not "
        probability_str = "" if self.__probability is None else "= {0}".format(str(self.__probability))
        negative_probability_str = "" if self.__probability is None else "= {0}".format(str(1.0 - self.__probability))
        return vertex_name_str + "P({0}Evacuees) {1}\n".format(is_evacuees_str,
                                                               probability_str) + "P({0}Evacuees) {1}\n".format(
            negative_is_evacuees_str, negative_probability_str)

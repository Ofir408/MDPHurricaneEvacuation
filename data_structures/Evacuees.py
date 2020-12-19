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

    # Example output format: P(Evacuees) = 0.2 or P(not Evacuees) = 0.8
    def __str__(self):
        is_evacuees_str = "" if self.__is_evacuees else "not "
        probability_str = "" if self.__probability is None else "= {0}".format(str(self.__probability))
        return "P({0}Evacuees) {1}".format(is_evacuees_str, probability_str)

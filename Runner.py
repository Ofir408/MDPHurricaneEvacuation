from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from utils.BeliefStatesGenerator import BeliefStatesGenerator
from utils.EnvironmentUtils import EnvironmentUtils


class Runner:

    def run(self, config: EnvironmentConfiguration):
        EnvironmentUtils.print_environment(config)
        states = BeliefStatesGenerator.generate_states(config)
        for state in states:
            print(state)
        #print("Possible Vertices: ", [k for k in config.get_vertexes().keys()])
        #start_vertex = input("Enter Start vertex:\n")
        #end_vertex = input("Enter End vertex:\n")

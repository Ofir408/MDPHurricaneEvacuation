from bl.ValueIteration import ValueIteration
from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from utils.BeliefStatesGenerator import BeliefStatesGenerator
from utils.EnvironmentUtils import EnvironmentUtils
from utils.TransitionDistributionGenerator import TransitionDistributionGenerator


class Runner:

    def run(self, config: EnvironmentConfiguration):
        EnvironmentUtils.print_environment(config)
        states = BeliefStatesGenerator.generate_states(config)
        for state in states:
            print(state)
        transition_distributions = TransitionDistributionGenerator.generate_distributions(states,
                                                                                          config.get_edges().values())
        for transition_distribution in transition_distributions:
            print(transition_distribution)

        print("Possible Vertices: ", [k for k in config.get_vertexes().keys()])
        #start_vertex = input("Enter Start vertex:\n")
        end_vertex = input("Enter End vertex:\n")

        states_dict = {}
        for state in states:
            if state.get_vertex_name() == end_vertex:
                state.set_is_goal(True)
            states_dict[state] = 0.0
        value_iteration_algo = ValueIteration(transition_distributions, states_dict)
        result, states_dict = value_iteration_algo.value_iteration_algo(config)
        for k, v in result.items():
            print("State={0}, Best_Action={1}".format(k, v))
        print("------------------------------------------------------------------------------------")
        for k, v in states_dict.items():
            print("State={0}, Utility={1}".format(k, v))

        print("DONE")

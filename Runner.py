from bl.Simulator import Simulator
from bl.agents.adversarial_agents.MiniMaxAgent import MiniMaxAgent
from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.State import State
from utils.EnvironmentUtils import EnvironmentUtils


class Runner:

    def run(self, env_config: EnvironmentConfiguration):
        chosen_agents = []
        states = []
        output_msg = "Choose Agent: \n 1) Adversarial Agent\n 2) Full Cooperative Agent\n 3) Semi Cooperative agent\n"
        num_of_agent = int(input("Enter number of agents\n"))
        agent_num = int(input(output_msg))
        for i in range(num_of_agent):
            while agent_num > 4 or agent_num < 1:
                print("Invalid agent number")
                agent_num = int(input(output_msg))
            chosen_agents.append(self.__get_agent(agent_num))
            EnvironmentUtils.print_environment(env_config)
            initial_state_name = input("Choose initial state for agent{0}:\n".format(i + 1))
            states.append(State(initial_state_name, (0, 0), EnvironmentUtils.get_required_vertexes(env_config)))

        simulator = Simulator()
        simulator.run_simulate(chosen_agents, simulator.update_func, simulator.terminate_func,
                               simulator.performance_func, env_config, states)

    def __get_agent(self, agent_num):
        if agent_num == 1:
            return MiniMaxAgent(mode=MiniMaxAgent.ADVERSARIAL_MODE, cut_off_depth=10)
        elif agent_num == 2:
            return MiniMaxAgent(mode=MiniMaxAgent.COOPERATIVE_MODE, cut_off_depth=10)
        elif agent_num == 3:
            return MiniMaxAgent(mode=MiniMaxAgent.SEMI_COOPERATIVE_MODE, cut_off_depth=10)

from bl.Simulator import Simulator
from bl.agents.adversarial_agents.MiniMaxAgent import MiniMaxAgent
from bl.agents.adversarial_agents.TerminalEvaluator import TerminalEvaluator
from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.State import State
from utils.EnvironmentUtils import EnvironmentUtils


class Runner:

    def run(self, env_config: EnvironmentConfiguration):
        chosen_agents = []
        states = []
        output_msg = "Choose Agent: \n 1) Adversarial Agent\n 2) Full Cooperative Agent\n 3) Semi Cooperative agent\n"
        num_of_agent = int(input("Enter number of agents\n"))
        game_number = int(input(output_msg))
        for i in range(num_of_agent):
            while game_number > 4 or game_number < 1:
                print("Invalid game number")
                game_number = int(input(output_msg))
            chosen_agents.append(self.__get_agent(game_number))
            EnvironmentUtils.print_environment(env_config)
            initial_state_name = input("Choose initial state for agent{0}:\n".format(i + 1))
            states.append(State(initial_state_name, (0, 0), EnvironmentUtils.get_required_vertexes(env_config)))

        simulator = Simulator()
        scores = simulator.run_simulate(chosen_agents, simulator.update_func, simulator.terminate_func,
                                        simulator.performance_func, env_config, states)
        self.__print_final_scores(game_number, scores)

    def __get_agent(self, game_number):
        if game_number == 1:
            return MiniMaxAgent(mode=MiniMaxAgent.ADVERSARIAL_MODE, cut_off_depth=20)
        elif game_number == 2:
            return MiniMaxAgent(mode=MiniMaxAgent.FULL_COOPERATIVE_MODE, cut_off_depth=20)
        elif game_number == 3:
            return MiniMaxAgent(mode=MiniMaxAgent.SEMI_COOPERATIVE_MODE, cut_off_depth=20)

    def __print_final_scores(self, game_number, scores_of_agents):
        game_score = None
        is_max_player = True
        if len(scores_of_agents) != 2:
            return
        first_agent_score, second_agent_score = scores_of_agents
        temp = State("", (first_agent_score, second_agent_score))
        if game_number == 1:
            game_score = TerminalEvaluator.terminate_eval(temp, MiniMaxAgent.ADVERSARIAL_MODE, is_max_player)
        elif game_number == 2:
            game_score = TerminalEvaluator.terminate_eval(temp, MiniMaxAgent.FULL_COOPERATIVE_MODE, is_max_player)
        elif game_number == 3:
            game_score = TerminalEvaluator.terminate_eval(temp, MiniMaxAgent.SEMI_COOPERATIVE_MODE, is_max_player)

        print("Final Game Score: ", game_score)

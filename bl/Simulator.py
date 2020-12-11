from typing import List, Callable, Tuple

from bl.agents import IAgent
from bl.agents.adversarial_agents.GameState import GameState
from configuration_reader import EnvironmentConfiguration
from data_structures.State import State
from utils.EnvironmentUtils import EnvironmentUtils
from utils.StateUtils import StateUtils


class Simulator:

    def run_simulate(self, agents: List, update_func: Callable, termination_func: Callable,
                     performance_func: Callable,
                     env_conf: EnvironmentConfiguration, states: List[State]):
        """
        :param agents: list of the agents in the environment
        :param update_func: update function, returns the new state
        :param termination_func: termination function that receives the current state and decide if to terminate or not.
        :param performance_func: performance function, return the score given state
        :param env_conf: Environment configuration
        :param states: the states of the agents
        :return: list of the scores of the agents.
        """
        scores = [0] * len(agents)
        costs = [0] * len(agents)
        actions = [[] for _ in range(len(agents))]
        traveled_states = []
        should_terminate = False

        while not should_terminate:
            for agent_num, agent in enumerate(agents):
                percepts = self.__get_percepts(agent_num, states, env_conf)
                action = agent.get_action(percepts)
                new_state = update_func(agent, action, actions, agent_num, states, (costs, agent_num), env_conf)
                states[agent_num] = new_state if new_state is not None else states[agent_num]
                scores[agent_num] += performance_func(new_state, traveled_states, env_conf)
                should_terminate = termination_func(states, agents)
                self.__display_word_state(agent_num, states, len(agents), actions, costs, scores, env_conf)
        return scores

    def __get_percepts(self, agent_num, states, env_conf):
        for state in states:
            state.set_scores_of_agents((0, 0))  # reset the score
        game_state = GameState(agent_num + 1 == 1, states[0], states[1])
        return game_state, env_conf

    def update_func(self, agent: IAgent, action: str, actions, agent_num: int, states: List[State],
                    costs_info: Tuple[List, int],
                    env_conf: EnvironmentConfiguration):
        current_state = states[agent_num]
        # check if the deadline passed
        deadline = env_conf.get_deadline()
        if current_state.get_cost() > deadline:
            return None

        actions[agent_num].append(action)
        vertex = env_conf.get_vertexes()[current_state.get_current_vertex_name()]
        vertex.set_state(current_state)
        new_state = EnvironmentUtils.get_next_vertex(vertex, action, agent.step_cost, env_conf).get_state()
        new_state.set_visited_vertex(new_state.get_current_vertex_name())
        costs, agent_num = costs_info
        edges_dict = env_conf.get_edges()
        if action in edges_dict.keys():
            edge_weight = edges_dict[action].get_weight()
            costs[agent_num] += edge_weight
            new_state.set_cost(current_state.get_cost() + edge_weight)
        for state in states:
            state.set_visited_vertex(current_state.get_current_vertex_name())
        return new_state

    def performance_func(self, new_state: State, traveled_states, env_config: EnvironmentConfiguration):
        return StateUtils.get_saved_people_num(new_state, traveled_states, env_config)

    def terminate_func(self, states: List[State], agents: List):
        should_terminate = len([agent for agent in agents if agent.was_terminated()]) == len(agents)
        if should_terminate:
            return True
        traveled_states = []
        for state in states:
            traveled_states += StateUtils.get_state_traveled_vertexes(state)
        traveled_states = set().union(traveled_states)
        return len(traveled_states) == len(states[0].get_required_vertexes())

    def __display_word_state(self, current_agent_num, states, agents_num, actions, costs, scores, env_config):
        if current_agent_num == agents_num - 1:
            # calc actions without TRAVELLING steps
            temp = []
            for current_agent_action in actions:
                temp.append(
                    [action for action in current_agent_action if action != 'TRAVELLING' and action is not None])

            print("----------------------------------")
            print("The step is over. Display the state of the world:")
            EnvironmentUtils.print_environment(env_config)
            print("actions: ", actions)
            print("concise actions: ", temp)
            print("costs: ", costs)
            print("states: ", [state.__str__() for state in states])
            print("scores: ", scores)
            print("----------------------------------")

import copy
from typing import List, Callable, Tuple

from bl.agents import IAgent
from bl.agents.adversarial_agents.GameState import GameState
from bl.agents.adversarial_agents.MiniMaxAgent import MiniMaxAgent
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
        vertexes_paths = [[] for _ in range(len(agents))]
        traveled_states = []
        should_terminate = False

        agent_num = 0
        while not should_terminate:
            agent = agents[agent_num]
            percepts = self.__get_percepts(agent_num, states, env_conf)
            states[agent_num].set_distance(0)
            if states[agent_num].get_distance() == 0:
                action = agent.get_action(percepts)
                new_state = update_func(agent, action, actions, vertexes_paths, agent_num, states, (costs, agent_num),
                                        env_conf)
                states[agent_num] = copy.deepcopy(new_state)
                scores[agent_num] += performance_func(new_state if action is None else new_state.get_parent_state(),
                                                      traveled_states, env_conf)
                should_terminate = termination_func([states[0].get_parent_state(), states[1].get_parent_state()],
                                                    agents, action)
            else:
                states[agent_num].decrease_distance_by_one()
            self.__display_word_state(agent_num, len(agents), actions, vertexes_paths, costs, scores, env_conf)
            agent_num = 1 if agent_num == 0 else 0
        return scores

    def __get_percepts(self, agent_num, states, env_conf):
        for state in states:
            state.set_scores_of_agents((0, 0))  # reset the score
        game_state = GameState(agent_num + 1 == 1, states[0], states[1])
        return game_state, env_conf

    def update_func(self, agent: IAgent, action: str, actions, vertexes_paths, agent_num: int, states: List[State],
                    costs_info: Tuple[List, int],
                    env_conf: EnvironmentConfiguration):
        current_state = states[agent_num]
        # check if the deadline passed
        deadline = env_conf.get_deadline()
        if current_state.get_cost() > deadline:
            return None

        actions[agent_num].append(action)
        if action != 'TRAVELLING' and action != 'DONE':
            vertexes_paths[agent_num].append(current_state.get_current_vertex_name())
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
            new_state.set_distance(edge_weight - 1)
        for state in states:
            state.set_visited_vertex(current_state.get_current_vertex_name())
        new_state.set_visited_vertex(current_state.get_current_vertex_name())
        return new_state

    def performance_func(self, new_state: State, traveled_states, env_config: EnvironmentConfiguration):
        if new_state.get_distance() > 0:
            return 0
        return StateUtils.get_saved_people_num(new_state, traveled_states, env_config)

    def terminate_func(self, states: List[State], agents: List, action: str):
        should_terminate = len([agent for agent in agents if agent.was_terminated()]) == len(agents)
        if should_terminate:
            return True
        traveled_states = []
        if None in states:
            return False
        for state in states:
            traveled_states += StateUtils.get_state_traveled_vertexes(state)
        traveled_states = set().union(traveled_states)
        return len(traveled_states) == len(states[0].get_required_vertexes())

    def __display_word_state(self, current_agent_num, agents_num, actions, vertices_paths, costs, scores,
                             env_config):
        # calc actions without TRAVELLING steps
        temp = []
        for current_agent_action in actions:
            temp.append(
                [action for action in current_agent_action if action != 'TRAVELLING' and
                 action != 'DONE' and action is not None])

            print("----------------------------------")
            print("The step is over. Display the state of the world:")
            EnvironmentUtils.print_environment(env_config)
            print("concise actions: ", temp)
            print("vertices paths: ", vertices_paths)
            print("costs: ", costs)
            print("scores: ", scores)
            print("----------------------------------")

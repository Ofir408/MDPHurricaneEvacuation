from data_structures.BeliefState import BeliefState
from data_structures.Edge import Edge


class TransitionProbability:
    def __init__(self, required_belief_state: BeliefState, given_belief_state: BeliefState, action: Edge,
                 prob: float = 0):
        self.__required_belief_state = required_belief_state
        self.__given_belief_state = given_belief_state
        self.__action = action
        self.__prob = prob

    def set_prob(self, prob: float):
        self.__prob = prob

    def get_required_belief_state(self):
        return self.__required_belief_state

    def get_given_belief_state(self):
        return self.__given_belief_state

    def get_action(self):
        return self.__action

    def get_prob(self):
        return self.__prob

    def __str__(self):
        return "required_state= {0}, given_state= {1}, action={2}, prob={3}".format(self.__required_belief_state,
                                                                                    self.__given_belief_state,
                                                                                    self.__action, self.__prob)

    def __eq__(self, other: 'TransitionProbability'):
        return self.__required_belief_state == other.__required_belief_state \
               and self.__given_belief_state == other.__given_belief_state and \
               self.__action == other.__action and self.__prob == other.__prob

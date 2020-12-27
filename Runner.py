import copy

from bl.BayesianNetworkBL import BayesianNetworkBL
from bl.EnumerationAlgo import EnumerationAlgo
from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.Blockages import Blockages
from data_structures.Evacuees import Evacuees
from data_structures.Var import Var
from utils.EnvironmentUtils import EnvironmentUtils


class Runner:

    def __init__(self):
        self.__evidence_list = []
        self.__enumeration_algo = EnumerationAlgo()
        self.__should_terminate = False

    def run(self, config: EnvironmentConfiguration):
        EnvironmentUtils.print_environment(config)
        bayesian_network_bl = BayesianNetworkBL(config)
        bayesian_network_bl.build_bayes_network(time_limit=2)

        reset_evidences_msg = "1) Reset evidence list to empty"
        add_evidence_msg = "2) Add piece of evidence to evidence list"
        prob_reasoning_msg = "3) Do probabilistic reasoning"
        quit_msg = "4) Quit\n"
        messages = [reset_evidences_msg, add_evidence_msg, prob_reasoning_msg, quit_msg]
        while not self.__should_terminate:
            for msg in messages:
                print(msg)
            user_choice = int(input("Insert Your Choice:\n"))
            if user_choice < 1 or user_choice > 4:
                print("Invalid Choice")
            else:
                self.__handle_choice(user_choice, bayesian_network_bl)

    def __add_evidence(self, bn: BayesianNetworkBL):
        # "Evacuees reported at vertex 2", and then "No blockage reported at edge 1 at time 0" etc.)
        is_valid_choice = False
        evacuees_msg = "1) Evacuees Evidence"
        blockage_msg = "2) Blockage Evidence"
        while not is_valid_choice:
            print(evacuees_msg)
            print(blockage_msg)
            user_choice = input("Insert Your Choice:\n")
            if user_choice == '1':
                print("Possible names: ", [evacuee.get_name() for evacuee in bn.get_evacuees()])
                evacuee_name = input("Insert Evacuee Name:\n")
                is_true = input("Is True?\n 1) Yes\n 2) No\n")
                evacuees = Evacuees(is_true == 1, evacuee_name, 1)
                self.__evidence_list.append(evacuees)
                is_valid_choice = True
            else:
                print("Possible names: ", [blockage.get_name() for blockage in bn.get_blockages()])
                blockage_name = input("Insert Blockage Name:\n")
                time = input("Insert Time: \n")
                is_true = input("Is True?\n 1) Yes\n 2) No\n")
                blockages = Blockages(blockage_name, 0 if time == "0" else 1, [], [], is_true == 1)
                self.__evidence_list.append(blockages)
                is_valid_choice = True

    def __do_prob_reasoning(self, bn: BayesianNetworkBL):
        possible_names = [v.get_name() for v in bn.topological_sorter()]
        print("Possible names: ", possible_names)
        variable = input("Choose variable name:\n")
        x = Var(variable)
        results = self.__enumeration_algo.enumeration_ask(x, copy.deepcopy(self.__evidence_list), bn)
        # TODO: add a better prints
        print("Results: ", results)

    def __handle_choice(self, user_choice: int, bn: BayesianNetworkBL):
        if user_choice == 1:
            self.__evidence_list.clear()
        if user_choice == 2:
            self.__add_evidence(bn)
        if user_choice == 3:
            self.__do_prob_reasoning(bn)
        if user_choice == 4:
            self.__should_terminate = True

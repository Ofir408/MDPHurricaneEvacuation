import os
import sys

from bl.BayesianNetworkBL import BayesianNetworkBL
from configuration_reader.ConfigurationReader import ConfigurationReader
from utils.EnvironmentUtils import EnvironmentUtils

configuration_reader = ConfigurationReader()
config_path = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(
    os.curdir) + "/initial_configurations/example2.ascii"
config = configuration_reader.read_configuration(config_path)
EnvironmentUtils.print_environment(config)
bayesian_network_bl = BayesianNetworkBL(config)
bayesian_network_bl.build_bayes_network(time_limit=2)

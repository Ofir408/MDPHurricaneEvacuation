import copy
from typing import Optional, Tuple

from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.Edge import Edge
from data_structures.Vertex import Vertex


class ConfigurationReader:
    COMMENT_SEPARATOR = ";"
    SPACE_SEPARATOR = " "

    @staticmethod
    def read_configuration(file_path: str):
        with open(file_path, 'r') as f:
            lines = [line.split(ConfigurationReader.COMMENT_SEPARATOR)[0].strip() for line in f if
                     line.strip()]  # removes comments & empty lines.

        vertexes_dict = {}
        edges_dict = {}
        vertices_num = -1
        for current_line in lines:
            if current_line.startswith("#N"):
                vertices_num = int(current_line.split(ConfigurationReader.SPACE_SEPARATOR)[1])
            elif current_line.startswith("#V"):
                name, vertex = ConfigurationReader.create_vertex(current_line)
                vertexes_dict[name] = vertex
            elif current_line.startswith("#E"):
                name, edge = ConfigurationReader.create_edge(current_line)
                edges_dict[name] = copy.deepcopy(edge)
                # add the edge name to relevant vertexes
                first_vertex_name, second_vertex_name = edge.get_vertex_names()
                first_vertex_name = "#V" + first_vertex_name
                second_vertex_name = "#V" + second_vertex_name
                first_vertex = vertexes_dict[first_vertex_name]
                first_vertex.add_edge_name(edge.get_edge_name())
                second_vertex = vertexes_dict[second_vertex_name]
                second_vertex.add_edge_name(edge.get_edge_name())
        return EnvironmentConfiguration(vertices_num, vertexes_dict, edges_dict)

    @staticmethod
    # Example input: #E1 1 2 W1
    def create_edge(input_line: str) -> Optional[Tuple[str, Edge]]:
        parts = input_line.split(ConfigurationReader.SPACE_SEPARATOR)
        name = parts[0].replace("#E", "")
        first_vertex = parts[1]
        second_vertex = parts[2]
        weight = int(parts[3].replace("W", ""))
        blockages_prob = 0
        if len(parts) == 5:
            blockages_prob = float(parts[4].replace("B", ""))
        return name, Edge(name, weight, (first_vertex, second_vertex), blockages_prob)

    @staticmethod
    # Example input: #V4 P2 or #V4
    def create_vertex(input_line: str) -> Optional[Tuple[str, Vertex]]:
        parts = input_line.split(ConfigurationReader.SPACE_SEPARATOR)
        name = parts[0]
        return name, Vertex(name)

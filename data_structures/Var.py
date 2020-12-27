from abc import ABC, abstractmethod


class Var(ABC):

    def __init__(self, name: str):
        self._name = name
        self._is_true = None

    def get_possible_values(self):
        return [True, False]

    def get_name(self):
        return self._name

    def is_true(self):
        return self._is_true

    def set_value(self, new_value: bool):
        self._is_true = new_value

    def __eq__(self, other: 'Var'):
        return self._name == other._name and self._is_true == other._is_true

import argparse
from abc import ABC, abstractmethod


class Problem(ABC):

    @abstractmethod
    def initialize_parser(self, parser: argparse.ArgumentParser):
        raise NotImplementedError

    @abstractmethod
    def is_chosen_problem(self, args: argparse.Namespace) -> bool:
        raise NotImplementedError

    @abstractmethod
    def run(self, args: argparse.Namespace) -> None:
        raise NotImplementedError
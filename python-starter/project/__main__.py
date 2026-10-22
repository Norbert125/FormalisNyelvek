from project.problem import Problem
import argparse
import importlib
import pkgutil


class Main(object):

    def __init__(self):
        self.problems = []

    def load_problems(self):
        package = 'project.problems'

        for _, module_name, _ in pkgutil.iter_modules([package.replace('.', '/')]):
            module = importlib.import_module(f"{package}.{module_name}")

            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)

                if isinstance(attribute, type) and issubclass(attribute, Problem) and attribute is not Problem:
                    self.problems.append(attribute())

    def initialize_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--input', required=True, help='input file')
        parser.add_argument('--output', required=True, help='output file')

        for problem in self.problems:
            problem.initialize_parser(parser)

        return parser

    def run(self):
        self.load_problems()
        parser = self.initialize_parser()
        args = parser.parse_args()

        for problem in self.problems:
            if problem.is_chosen_problem(args):
                problem.run(args)
                return

        parser.error('No problem was chosen; use --det.')


if __name__ == '__main__':
    Main().run()
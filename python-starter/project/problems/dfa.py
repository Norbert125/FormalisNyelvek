import argparse

from project.problem import Problem


class DFA(object):

    def __init__(self, states, alphabet, start, finals, transitions):
        self.states = states
        self.alphabet = alphabet
        self.start = start
        self.finals = finals
        self.transitions = transitions

    @classmethod
    def from_file(cls, path):
        with open(path, 'r', encoding='utf-8') as input_file:
            lines = [line.split() for line in input_file if line.strip()]

        states = set(lines[0])
        alphabet = set(lines[1])
        start = lines[2][0]
        finals = set(lines[3])
        transitions = {(source, symbol): target for source, symbol, target in lines[4:]}
        return cls(states, alphabet, start, finals, transitions)

    def accepts(self, word):
        state = self.start
        for symbol in word:
            state = self.transitions.get((state, symbol))
            if state is None:
                return False
        return state in self.finals


class DFAProblem(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--check', help='comma separated words to check')

    def is_chosen_problem(self, args):
        return args.check is not None

    def run(self, args):
        dfa = DFA.from_file(args.input)
        words = args.check.split(',')
        results = ['IGEN' if dfa.accepts(word) else 'NEM' for word in words]

        with open(args.output, 'w', encoding='utf-8') as output_file:
            output_file.write('\n'.join(results))

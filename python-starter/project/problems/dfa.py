from project.problem import Problem
import argparse


class DFA(object):

    def __init__(self, states, alphabet, start, finals, transitions):
        self.states = states
        self.alphabet = alphabet
        self.start = start
        self.finals = finals
        self.transitions = transitions

    @classmethod
    def from_file(cls, path):
        """
        Read the automaton from the given file
        """
        with open(path, 'r') as f:
            lines = [line.split() for line in f if line.strip()]

        states = set(lines[0])
        alphabet = set(lines[1])
        start = lines[2][0]
        finals = set(lines[3])
        transitions = {(source, symbol): target for source, symbol, target in lines[4:]}

        return cls(states, alphabet, start, finals, transitions)

    def accepts(self, word):
        """
        Check if the automaton accepts the given word
        """
        state = self.start

        for symbol in word:
            state = self.transitions.get((state, symbol))
            if state is None:
                return False

        return state in self.finals


class DFAProblem(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        """
        Initialize the parser with the necessary arguments
        """
        parser.add_argument('--check', help='comma separated words to check')

    def is_chosen_problem(self, args):
        """
        Check if the problem is chosen
        """
        return args.check is not None

    def run(self, args):
        """
        Run the program
        """
        dfa = DFA.from_file(args.input)
        words = args.check.split(',')

        results = ['IGEN' if dfa.accepts(word) else 'NEM' for word in words]

        with open(args.output, 'w') as f:
            f.write('\n'.join(results))

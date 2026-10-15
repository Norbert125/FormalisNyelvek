from collections import deque

from project.problem import Problem


class NFA(object):

    def __init__(self, states, alphabet, start, finals, transitions):
        self.states = states
        self.alphabet = alphabet
        self.start = start
        self.finals = finals
        self.transitions = transitions

    @classmethod
    def from_file(cls, path):
        with open(path, 'r', encoding='utf-8') as input_file:
            lines = input_file.read().splitlines()

        if len(lines) < 4:
            raise ValueError('Input must contain states, alphabet, start state, and final states.')

        states = set(lines[0].split())
        alphabet = set(lines[1].split())
        if not states:
            raise ValueError('The state set cannot be empty.')

        start_line = lines[2].split()
        if len(start_line) != 1 or start_line[0] not in states:
            raise ValueError('The start state must be one of the declared states.')

        start = start_line[0]
        finals = set(lines[3].split())
        if not finals <= states:
            raise ValueError('Every final state must be declared in the state set.')

        transitions = {}
        for line_number, raw_line in enumerate(lines[4:], start=5):
            if not raw_line.strip():
                continue
            line = raw_line.split()
            if len(line) != 3:
                raise ValueError(f'Invalid transition on line {line_number}: expected three fields.')

            source, symbol, target = line
            if source not in states or target not in states:
                raise ValueError(f'Invalid transition on line {line_number}: unknown state.')
            if symbol not in alphabet:
                raise ValueError(f'Invalid transition on line {line_number}: unknown symbol.')

            transitions.setdefault((source, symbol), set()).add(target)

        return cls(states, alphabet, start, finals, transitions)

    def determinize(self):
        start_subset = frozenset((self.start,))
        subsets = [start_subset]
        subset_ids = {start_subset: 0}
        transitions = {}
        pending = deque([start_subset])
        alphabet = sorted(self.alphabet)

        while pending:
            subset = pending.popleft()
            source_id = subset_ids[subset]

            for symbol in alphabet:
                target_subset = frozenset(
                    target
                    for state in subset
                    for target in self.transitions.get((state, symbol), ())
                )
                if not target_subset:
                    continue

                if target_subset not in subset_ids:
                    subset_ids[target_subset] = len(subsets)
                    subsets.append(target_subset)
                    pending.append(target_subset)

                transitions[(source_id, symbol)] = subset_ids[target_subset]

        finals = {
            subset_ids[subset]
            for subset in subsets
            if subset & self.finals
        }
        return subsets, alphabet, finals, transitions


class DeterminizeProblem(Problem):

    def initialize_parser(self, parser):
        parser.add_argument('--det', action='store_true', help='determinize the input automaton')

    def is_chosen_problem(self, args):
        return args.det

    def run(self, args):
        nfa = NFA.from_file(args.input)
        subsets, alphabet, finals, transitions = nfa.determinize()
        state_names = [f's{state_id}' for state_id in range(len(subsets))]

        output_lines = [
            ' '.join(state_names),
            ' '.join(alphabet),
            's0',
            ' '.join(state_names[state_id] for state_id in sorted(finals)),
        ]

        for (source_id, symbol), target_id in sorted(
            transitions.items(), key=lambda transition: (transition[0][0], transition[0][1], transition[1])
        ):
            output_lines.append(f'{state_names[source_id]} {symbol} {state_names[target_id]}')

        with open(args.output, 'w', encoding='utf-8') as output_file:
            output_file.write('\n'.join(output_lines) + '\n')
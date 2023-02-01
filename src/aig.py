from typing import List, Dict
import random

# http://fmv.jku.at/aiger/FORMAT-20070427.pdf
class Aig:
    def __init__(self) -> None:
        self.inputs : List[int] = []
        self.outputs : List[int] = []
        self.and_gates : List[List[int]] = []

        self.idx = 1


    # creates a random aiger network
    # that is a single node, incomplete binary tree.
    # the root is the only primary output.
    # leaves are primary inputs.
    # the root as well as all internal nodes are and gates.
    # inverters are randomly added to input pins of and gates.
    def random_init(self, gate_limit : int = 30, input_limit : int = 10, inverter_ratio : float = 0.5) -> None:
        break_ratio : float = 1.0 / gate_limit

        self.outputs.append(1)
        stack = [1]
        while stack:
            # exceeds gate limit
            if len(self.and_gates) >= gate_limit:
                for node in stack:
                    if len(self.inputs) < input_limit:
                        self.inputs.append(node)
                    else:
                        rand_input = random.choice(self.inputs)
                        self.and_gates.append([node, rand_input, rand_input])
                break

            # process next node in stack
            node = stack.pop(0)

            # build leaf node
            if self.idx > 0 and random.random() < break_ratio:
                self.inputs.append(node)
                continue

            # build and gate
            self.idx += 1
            stack.append(self.idx)
            self.idx += 1
            stack.append(self.idx)

            and_gate = [node]
            if random.random() < inverter_ratio:
                and_gate.append(-(self.idx-1))
            else:
                and_gate.append(self.idx-1)
            if random.random() < inverter_ratio:
                and_gate.append(-self.idx)
            else:
                and_gate.append(self.idx)

            self.and_gates.append(and_gate)

    def serialize(self) -> str:
        aig_str = ''
        aig_str += f'aag {self.idx} {len(self.inputs)} {0} {len(self.outputs)} {len(self.and_gates)}\n'

        for input in self.inputs:
            aig_str += f'{2*input}\n'
        for output in self.outputs:
            aig_str += f'{2*output}\n'

        for and_gate in self.and_gates:
            assert len(and_gate) == 3, f'unrecognized and gate: {and_gate}'
            aig_str += f'{2*and_gate[0]} {2*and_gate[1] if and_gate[1] > 0 else -2*and_gate[1] + 1} {2*and_gate[2] if and_gate[2] > 0 else -2*and_gate[2] + 1}\n'

        return aig_str




    






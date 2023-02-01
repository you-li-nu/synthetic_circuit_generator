from typing import Dict, List

class Gate:
    def __init__(self, name='', type='', children=[]) -> None:
        self.name = name # out pin
        self.type = type # operator
        self.children : List[str] = children # operands

    def serialize(self, to_upper=True) -> str:
        children_str = ', '.join(self.children)
        if to_upper:
            return f'{self.name} = {self.type.upper()}({children_str})'
        return f'{self.name} = {self.type}({children_str})'

# a ckt can be either an encrypted circuit or an oracle circuit.
class Ckt:
    def __init__(self) -> None:
        self.inputs : List[str] = [] # names of primary inputs excluding keyinputs
        self.keyinputs : List[str] = []
        self.outputs : List[str] = [] # an output node can also be a gate node

        self.dffs : List[Gate] = []
        self.gates : List[Gate] = []

    # get a list of names for all original nodes
    def get_all_originals(self) -> List[str]:
        originals = self.inputs + self.keyinputs + self.outputs
        for dff_name in [dff.name for dff in self.dffs]:
            if dff_name not in originals:
                originals.append(dff_name)
        for gate_name in [gate.name for gate in self.gates]:
            if gate_name not in originals:
                originals.append(gate_name)
        assert 'vdd' not in originals and 'gnd' not in originals, f'constants should not be a node.'
        return originals

    def serialize(self, to_upper=True) -> str:
        bench_str = ''
        for input in self.inputs:
            bench_str += f'INPUT({input})\n'
        for keyinput in self.keyinputs:
            bench_str += f'INPUT({keyinput})\n'
        for output in self.outputs:
            bench_str += f'OUTPUT({output})\n'
        for dff in self.dffs:
            bench_str += dff.serialize(to_upper) + '\n'
        for gate in self.gates:
            bench_str += gate.serialize(to_upper) + '\n'
        return bench_str

if __name__ == '__main__':
    pass
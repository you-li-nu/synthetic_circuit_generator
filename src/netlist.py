from typing import List, Dict

from ckt import Gate, Ckt

class Netlist:
    def __init__(self, ckt : Ckt) -> None:
        self.ckt = ckt

        self.cells : List[str] = []
        self.nets : List[List[int]] = []

        self.cell2idx : Dict[str, int] = {}

        self.initialize()


    def initialize(self) -> None:
        self.cells = self.ckt.inputs + self.ckt.keyinputs
        self.cells.extend([dff.name for dff in self.ckt.dffs])
        self.cells.extend([gate.name for gate in self.ckt.gates])

        for i in range(len(self.cells)):
            self.cell2idx[self.cells[i]] = i

        self.nets = self.get_nets()

    # get a list of internal nets of a ckt.
    # each primary/secondary input and gate corresponds to a net (with exception, see below).
    # for a gate, its corresponding net is named after its output pin.
    # a gate has no corresponding net if it is a primary/secondary output.
    def get_nets(self) -> List[List[int]]:
        nets : List[List[int]] = []
        for cell in self.cells:
            nets.append([self.cell2idx[cell]])
        for gate in self.ckt.gates:
            for child in gate.children:
                nets[self.cell2idx[child]].append(self.cell2idx[gate.name])

        ret_nets : List[List[int]] = []
        for net in nets:
            if len(net) < 2:
                assert self.cells[net[0]] in self.ckt.outputs, f'dangling cell: {self.cells[net[0]]}'
            else:
                ret_nets.append(net)
        return ret_nets

    # first line:
    # num_cells num_nets
    # every other line:
    # driving_cell loading_cell_0 loading_cell_1 ...
    def serialize(self, verbose : bool = True) -> str:
        netlist_str = ''
        netlist_str += '#========num_cells num_nets\n'
        netlist_str += f'{len(self.cells)} {len(self.nets)}\n'
        netlist_str += '#========nets\n'
        for net in self.nets:
            netlist_str += ' '.join([str(idx) for idx in net]) + '\n'

        if verbose: # add names as comments
            netlist_str += '#========symbols\n'
            dff_names = [dff.name for dff in self.ckt.dffs]
            gate_names = [gate.name for gate in self.ckt.gates]
            for cell in self.cells:
                type = ''
                if cell in self.ckt.inputs:
                    type = 'input'
                elif cell in self.ckt.outputs:
                    type = 'output'
                elif cell in dff_names:
                    type = 'dff'
                elif cell in gate_names:
                    type = 'gate'
                else:
                    assert False, f'unrecognized cell: {cell}'
                netlist_str += f'# {self.cell2idx[cell]} {type} {cell}\n'

        return netlist_str







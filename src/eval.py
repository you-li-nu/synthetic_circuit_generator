import random
from typing import List, Dict

def write_random_solution(num_cells : int, outfile : str):
    solution_list = [i for i in range(num_cells)]
    random.shuffle(solution_list)
    with open(outfile, 'w') as f:
        f.write(' '.join(map(str, solution_list)))

class Evaluator:
    def __init__(self, netfile : str, ansfile : str) -> None:
        self.num_cells : int = 0
        self.num_nets : int = 0
        self.nets : List[List[int]] = []

        self.ans : List[int] = []
        self.cell2idx : Dict[int, int] = {}

        self.intervals : List[List[int]] = [] # interval : [leftmost_idx_in_net, rightmost_idx_in_net]

        self.read_netlist(netfile)
        self.read_ans(ansfile)

    # Leetcode 253: meeting room
    def compute_maxcut(self):
        self.compute_total_wirelength()
        starts = [interval[0] for interval in self.intervals]
        ends = [interval[1] for interval in self.intervals]

        starts.sort()
        ends.sort()

        maxcut = 0
        while starts:
            curr = starts.pop(0)
            while ends and ends[0] <= curr:
                ends.pop(0)
            maxcut = max(maxcut, len(ends) - len(starts))
        return maxcut

    # given a list of 1-D nets, compute their total wirelength.
    def compute_total_wirelength(self) -> int:
        total = 0
        for net in self.nets:
            total += self.compute_wirelength(net)
        return total

    # given a 1-D net, compute its wirelength.
    def compute_wirelength(self, net : List[int]) -> int:
        l = self.num_cells - 1
        r = 0
        for cell in net:
            l = min(l, self.cell2idx[cell])
            r = max(r, self.cell2idx[cell])
        assert r - l > 0, f'illegal cell: {cell}'
        self.intervals.append([l, r])
        return r - l

    # parse a .ans file.
    def read_ans(self, ansfile : str):
        with open(ansfile, 'r') as f:
            line = f.readline()
            assert len(line.strip().split()) == self.num_cells, f'length of answer {self.num_cells} is not equal to length of cells {len(line.strip().split())}.'
            self.ans = list(map(int, line.strip().split()))

        for i in range(len(self.ans)):
            self.cell2idx[self.ans[i]] = i

    # parse a .net file.
    def read_netlist(self, netfile : str):
        with open(netfile, 'r') as f:
            flag = False
            for line in f.readlines():
                if line.startswith('#'):
                    continue
                if not flag:
                    flag = True
                    assert len(line.strip().split()) == 2, f'unrecognized first line: {line}'
                    self.num_cells, self.num_nets = list(map(int, line.strip().split()))
                else:
                    self.nets.append(list(map(int, line.strip().split())))

    def serialize(self) -> str:
        netlist_str = ''
        netlist_str += '#========num_cells num_nets\n'
        netlist_str += f'{self.num_cells} {self.num_nets}\n'
        netlist_str += '#========nets\n'
        for net in self.nets:
            netlist_str += ' '.join(list(map(str, net))) + '\n'

        return netlist_str




if __name__ == '__main__':
    write_random_solution(32002, './playground/synth_50000_500.ans')
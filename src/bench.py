import re
import sys

from ckt import Gate, Ckt


# reference: https://github.com/gatelabdavis/RANE
def bench_parser(filename : str) -> Ckt:
    assert filename.endswith('.bench'), f'{filename} is not a .bench file.'
    bench_str = ''
    with open(filename, 'r') as f:
        bench_str = f.read()

    ckt = Ckt()

    # input and keyinput
    inputs = re.findall(r'INPUT\((.*?)\)', bench_str)
    for input in inputs:
        if not input.startswith('keyinput'):
            ckt.inputs.append(input)
        else:
            ckt.keyinputs.append(input)

    # output
    outputs = re.findall(r'OUTPUT\((.*?)\)', bench_str)
    ckt.outputs = outputs

    # dff and gate
    gates = re.findall(r'(.*?) = (.*?)\((.*?)\)', bench_str)
    for gate in gates:
        name = gate[0]
        type = gate[1].lower()
        children_str = gate[2]
        g = Gate(name, type, children_str.strip().replace(' ', '').split(','))
        if type == 'dff':
            ckt.dffs.append(g)
        else:
            ckt.gates.append(g)

    if False:
        print(f'INPUTS:')
        print(f'{ckt.inputs}')
        print(f'KEYINPUTS:')
        print(f'{ckt.keyinputs}')
        print(f'OUTPUTS:')
        print(f'{ckt.outputs}')

    return ckt

# lower_or_upper: convert all types to upper case if set to True. Keeps unchanged otherwise.
def bench_writer(filename : str, ckt : Ckt, to_upper=True) -> None:
    bench_str = ckt.serialize(to_upper)
    with open(filename, 'w') as f:
        f.write(bench_str)

if __name__ == '__main__':
    assert len(sys.argv) == 2, f'python3 ./src/bench.py ./bench/c17.bench'
    ckt = bench_parser(sys.argv[1])
    print(ckt.serialize())
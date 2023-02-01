from typing import List, Dict
import sys
import re
import logging

from pysmt.shortcuts import simplify, And
from ckt import Gate, Ckt
from bench import bench_writer

'''
convert (a subset of) structural verilog to .bench format.
see /bench/gcd_fast.v for an example.
'''
# reference: https://github.com/gatelabdavis/RANE
def verilog_parser(filename : str) -> Ckt:
    assert filename.endswith('.v'), f'{filename} is not a .v file.'
    verilog_str = ''
    with open(filename, 'r') as f:
        verilog_str = f.read()

    ckt = Ckt()

    # input and keyinput
    inputs = re.findall(r'input (\[(.*)\]|)([\s\S]*?);', verilog_str)
    for input in inputs:
        if input[2].strip() == 'clk' or input[2] == 'clock':
            continue

        # process signal range
        signal_range = [0, 0]
        if input[1]:
            first = int(input[1][:input[1].index(':')])
            second = int(input[1][input[1].index(':') + 1:])
            signal_range[0] = min(first, second)
            signal_range[1] = max(first, second)

        target = None
        if not input[2].startswith('keyinput'):
            target = ckt.inputs
        else:
            target = ckt.keyinputs

        if signal_range == [0, 0]:
            target.append(input[2].strip())
        else:
            for i in range(signal_range[0], signal_range[1] + 1):
                target.append(f'{input[2].strip()}[{i}]')

    # output
    outputs = re.findall(r'output (\[(.*)\]|)([\s\S]*?);', verilog_str)
    for output in outputs:
        # process signal range
        signal_range = [0, 0]
        if output[1]:
            first = int(output[1][:output[1].index(':')])
            second = int(output[1][output[1].index(':') + 1:])
            signal_range[0] = min(first, second)
            signal_range[1] = max(first, second)

        if signal_range == [0, 0]:
            ckt.outputs.append(output[2].strip())
        else:
            for i in range(signal_range[0], signal_range[1] + 1):
                ckt.outputs.append(f'{output[2].strip()}[{i}]')

    # dff and gate
    gates = re.findall(r'^\s*(\S*?)\s*(\S*?)\s*\(([\s\S]*?)\);', verilog_str, re.MULTILINE)
    for gate in gates:
        type = gate[0].lower()
        if type == 'module':
            continue

        port_list = gate[2].replace(' ', '').replace('\n', '').split(',')
        g, name = process_gate(type, port_list)
        if type == 'dff':
            ckt.dffs.append(g)
        else:
            ckt.gates.append(g)

    # wires
    wires = re.findall(r'assign (.*?) = (.*?);', verilog_str)
    for wire in wires:
        g = Gate(wire[0], 'buf', [wire[1]])
        name = wire[0]
        ckt.gates.append(g)

    logging.debug(f'INPUTS:')
    logging.debug(f'{ckt.inputs}')
    logging.debug(f'KEYINPUTS:')
    logging.debug(f'{ckt.keyinputs}')
    logging.debug(f'OUTPUTS:')
    logging.debug(f'{ckt.outputs}')

    return ckt

def process_gate(type : str, port_list : List[str]):
    d : Dict[str,str] = {}
    for port in port_list:
        k, v = process_port(port)
        d[k] = v

    g = None
    name = ''
    if type == 'dff':
        assert len(d) == 3 and 'C' in d and 'D' in d and 'Q' in d, f'unrecognized gate: {type}. {port_list}'
        g = Gate(d['Q'], type, [d['D']])
        name = d['Q']
    elif type == 'buf' or type == 'not':
        assert len(d) == 2 and 'A' in d and 'Y' in d, f'unrecognized gate: {type}. {port_list}'
        g = Gate(d['Y'], type, [d['A']])
        name = d['Y']
    elif type == 'and' or type == 'nand' or type == 'or' or type == 'nor':
        assert len(d) == 3 and 'A' in d and 'B' in d and 'Y' in d, f'unrecognized gate: {type}. {port_list}'
        g = Gate(d['Y'], type, [d['A'], d['B']])
        name = d['Y']
    elif type == 'xor': # unmapped
        assert len(d) == 3 and 'A' in d and 'B' in d and 'Y' in d, f'unrecognized gate: {type}. {port_list}'
        g = Gate(d['Y'], type, [d['A'], d['B']])
        name = d['Y']
    else:
        assert False, f'unrecognized gate: {type}. {port_list}'

    return g, name
        
def process_port(port : str):
    assert port.startswith('.'), f'unrecognized port {port}'
    k = port[1:port.index('(')]
    v = port[port.index('(') + 1 : port.rindex(')')]
    return k, v

if __name__ == '__main__':
    assert len(sys.argv) == 2, f'python3 ./src/verilog.py ./bench/aig/test_20_15.v'
    ckt = verilog_parser(sys.argv[1])
    print(ckt.serialize())
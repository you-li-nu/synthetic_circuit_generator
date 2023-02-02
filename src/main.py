'''
Author: You Li
Date: 2023-01
Institution: Northwestern University
'''

import argparse

from bench import bench_parser
from verilog import verilog_parser
from netlist import Netlist
from aig import Aig
from mapping import tech_mapping
from eval import Evaluator

parser = argparse.ArgumentParser()
parser.add_argument('--function', type=str, required=True, help='[ bench2nets | synth_nets | synth_bench | eval_wirelength | eval_maxcut ]')
parser.add_argument('--infile', type=str, required=False, help='input file (if applicable)')
parser.add_argument('--ansfile', type=str, required=False, help='answer file (if applicable)')
parser.add_argument('--outfile', type=str, required=False, help='output file (if applicable)')
parser.add_argument('--gate_limit', type=int, required=False, help='upper bound for the number of gates (if applicable)')
parser.add_argument('--input_limit', type=int, required=False, help='upper bound for the number of primary inputs (if applicable)')
args = parser.parse_args()


if args.function == 'bench2nets':
    assert args.infile, f'missing infile.'
    assert args.outfile, f'missing outfile.'
    ckt = bench_parser(args.infile)
    # print(ckt.serialize())
    netlist = Netlist(ckt)
    # print(netlist.serialize())
    with open(args.outfile, 'w') as f:
        f.write(netlist.serialize())
elif args.function == 'synth_nets':
    assert args.outfile, f'missing outfile.'
    assert args.gate_limit, f'missing gate_limit.'
    assert args.input_limit, f'missing input_limit.'

    prefix = args.outfile[:args.outfile.rindex('.')]

    aig = Aig()
    aig.random_init(args.gate_limit, args.input_limit)
    # print(aig.serialize())
    with open(prefix + '_tmp.aag', 'w') as f:
        f.write(aig.serialize())

    tech_mapping(prefix + '_tmp.aag', prefix + '_tmp.v')

    ckt = verilog_parser(prefix + '_tmp.v')
    # print(ckt.serialize())
    netlist = Netlist(ckt)
    with open(args.outfile, 'w') as f:
        f.write(netlist.serialize())
elif args.function == 'synth_bench':
    assert args.outfile, f'missing outfile.'
    assert args.gate_limit, f'missing gate_limit.'
    assert args.input_limit, f'missing input_limit.'

    prefix = args.outfile[:args.outfile.rindex('.')]

    aig = Aig()
    aig.random_init(args.gate_limit, args.input_limit)
    # print(aig.serialize())
    with open(prefix + '_tmp.aag', 'w') as f:
        f.write(aig.serialize())

    tech_mapping(prefix + '_tmp.aag', prefix + '_tmp.v')

    ckt = verilog_parser(prefix + '_tmp.v')
    with open(args.outfile, 'w') as f:
        f.write(ckt.serialize())
elif args.function == 'eval_wirelength':
    assert args.infile, f'missing infile.'
    assert args.ansfile, f'missing ansfile.'

    eval = Evaluator(args.infile, args.ansfile)
    print(f'total wirelength: {eval.compute_total_wirelength()}')
elif args.function == 'eval_maxcut':
    assert args.infile, f'missing infile.'
    assert args.ansfile, f'missing ansfile.'

    eval = Evaluator(args.infile, args.ansfile)
    print(f'maxcut: {eval.compute_maxcut()}')
else:
    assert False, f'unrecognized function: {args.function}'

from typing import List, Dict

from bench import bench_parser
from verilog import verilog_parser
from netlist import Netlist
from aig import Aig
from mapping import tech_mapping

def test_gen_mapping():
    aig = Aig()
    aig.random_init(20000,500)
    print(aig.serialize())
    with open('./playground/test_20000_500.aag', 'w') as f:
        f.write(aig.serialize())

    tech_mapping('./playground/test_20000_500.aag', './playground/test_20000_500.v')

    ckt = verilog_parser('./playground/test_20000_500.v')
    print(ckt.serialize())
    netlist = Netlist(ckt)
    with open('./playground/test_20000_500.net', 'w') as f:
        f.write(netlist.serialize())

def test_tech_mapping():
    tech_mapping('./bench/aig/test_20_15.aag', './bench/aig/test_20_15.v')

def test_generate_aiger():
    aig = Aig()
    aig.random_init(20,15)
    print(aig.serialize())
    with open('./playground/test.aag', 'w') as f:
        f.write(aig.serialize())

def test_netlist_parser():
    ckt = bench_parser('./bench/iscas85/c17.bench')
    print(ckt.serialize())
    netlist = Netlist(ckt)
    print(netlist.serialize())


def test_bench_parser():
    ckt = bench_parser('./bench/iscas85/c17.bench')
    print(ckt.serialize())


if __name__ == '__main__':
    test_gen_mapping()


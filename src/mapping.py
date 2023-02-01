from typing import List, Dict
import subprocess


def tech_mapping(aig_file : str, verilog_file : str, lib_file : str = './bench/lib/youl.lib') -> None:
    res = subprocess.run(['yosys', '-p', f'read_aiger {aig_file}', '-p', f'abc -liberty {lib_file}', '-p', f'write_verilog -noattr {verilog_file}'])
    assert res.returncode == 0, f'error in tech_mapping()'
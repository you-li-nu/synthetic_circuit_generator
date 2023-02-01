# Synthetic Netlist Generator

Generates random netlists to test placement & routing algorithms.

### Netlist format
Example circuit:
```
                .---.
            .-->| 1 |--.
            |   '---'  |
    .---.   |          |
.-->| 0 |---|          |
|   '---'   |          |
|           |          '-->.---.
|           |              | 2 |--.
|           '------------->'---'  |
|                                 |
'---------------------------------'
```
Corresponding Netlist:

```
#========num_cells num_nets
3 3
#========nets
0 1 2
1 2
2 0
#========symbols
# 0 gate n0
# 1 gate n1
# 2 gate n2
```

### Dependency
Ubuntu or other Linux distributions.
```
sudo apt-get install python-argparse
sudo apt install berkeley-abc
sudo apt install yosys
```
### Generate a netlist from a .bench file
```
python3 ./src/main.py --function bench2nets --infile ./bench/iscas85/c17.bench --outfile ./playground/c17.net
```

### Generate a synthetic netlist
A larger ```gate_limit``` will result in a larger circuit. The ```input_limit``` should not be too small: an adequate choice would be ```input_limit ~= sqrt(gate_limit)```.
```
python3 ./src/main.py --function synth_nets --outfile ./playground/synth_20000_500.net --gate_limit 20000 --input_limit 500
```

### Methodology
You can ignore this part if you are a student on CE357.

1. Randomly generate a single root, incomplete binary tree. (TODO: multiple roots)
2. Convert the tree to an And-Inverter-Graph, whose primary output is the root node, primary inputs are the leaves, internal nodes as well as the root are AND gates. Insert inverters to edges at random.
3. Use yosys for technology mapping. If you prefer larger cells/modules, modify /bench/lib/youl.lib to your own library. You may also need to modify verilog.py.
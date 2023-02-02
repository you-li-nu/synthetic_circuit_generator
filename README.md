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
sudo apt install python-argparse
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

### Generate a synthetic .bench file
```
python3 ./src/main.py --function synth_bench --outfile ./playground/synth_20000_500.bench --gate_limit 20000 --input_limit 500
```

### Compute total wirelength for a 1-D placement
```
python3 ./src/main.py --function eval_wirelength --infile ./playground/c17.net --ansfile ./playground/c17.ans
```

### Compute maxcut for a 1-D placement
```
python3 ./src/main.py --function eval_maxcut --infile ./playground/c17.net --ansfile ./playground/c17.ans
```

### Methodology
You can ignore this part if you are a student on CE357.

1. Randomly generate a single root, incomplete binary tree. (TODO: multiple roots)
2. Convert the tree to an And-Inverter-Graph, whose primary output is the root node, primary inputs are the leaves, AND gates are internal nodes as well as the root node. Inverters are attached to edges of the tree at random.
3. Use yosys for technology mapping. If you prefer larger cells/modules, modify /bench/lib/youl.lib to your own library. You may also need to modify verilog.py.
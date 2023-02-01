# SAT-based Attack

## Combinational
### Original SAT attack:
```
python3 ./src/main.py --tactic original --encrypted ./bench/comb/c432_enc05.bench --oracle ./bench/comb/c432.bench
```

### Generalized SAT attack:
```
python3 ./src/main.py --tactic generalization --encrypted ./bench/comb/c432_enc05.bench --oracle ./bench/comb/c432.bench
```

## Sequential

### Generalized Sequential SAT attack:
```
python3 ./src/main.py --tactic seq --encrypted ./bench/seq/s27_2.bench --oracle ./bench/seq/s27.bench
```

# verilog2bench

## RTL verilog to structural verilog
(through logic synthesis and technology mapping)

### Dependencies
```
sudo apt install berkeley-abc
sudo apt install yosys
```
### Runbook
```
yosys
read_verilog ./gcd_fast_m.v
synth -top gcd_fast_m
dfflibmap -liberty ./youl.lib
abc -liberty ./youl.lib
write_verilog -noattr ./gcd_fast.v
```

## structural verilog to .bench format
Creates a .bench file with the same filename under the same repository.
```
python3 ./src/verilog.py ./bench/gcd_fast.v
```

# Sequential Equivalence Checking

### Create Kairos wrapper for external model checker

```
python3 ../../src/kairos.py --symmetric ./inverse_fast.v ./inverse_slow.v ./inverse_kairos.bench
```
### Use ABC for model checking

```
read_bench ./inverse_kairos.bench
strash
write_aiger -s ./inverse_kairos.aig
pdr
```
# EAGER-gem5-GUI
**EAGER computer architecture learning tool utilizing gem5**
- This project would not be possible without [gem5](https://github.com/gem5/gem5).
## Prototype Version 1.0:

### Prerequisites:

#### Libraries and Python Packages:
  - gcc
  - python3
  - colorama
  - requests
  - Pillow
  - pydot
  
#### gem5 Binary:
  Our design assumes that `gem5.opt` is built using ISA = ALL. \
  Then we point to it with the GEM5_PATH environment variable: \
  ```export GEM5_PATH=/path/to/gem5.opt``` 

### Features:

#### gem5 Configuration:
  - gem5 simulations in SE mode
  - Simple boards
  - CPU types: atomic, timing, O3, minor
  - ISAs: x86 and ARM
  - All stdlib memory types
  - All stdlib cache types

#### User Programs:
  - Open, save, save as C programs
  - Compile for x86 architecture
  - Load as resource for Gem5

#### Stats:
  - View simulation statistics
  - Currently parses most important stats

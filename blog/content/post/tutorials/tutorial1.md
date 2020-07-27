---
title: "Tutorial 1"
date: 2020-06-04T13:15:46+10:00

categories: ["Tutorials"]
description: "Introduction to Tooling Frameworks"
hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# TODO

* Install `pwntools` - Python framework
* Install `pwndbg` - Extension for GDB

* Look at ROP Gadget
* Look at Ropper

---

# Using pwntools

* Generally, start with `from pwn import *`

```python
from pwn import *

p = process("./intro")

"""
Automation
"""

p.interactive() # Allow us to interact with the program after we finish the automated parts
```

## Debug

* Adding DEBUG at the end of a pwntools python script will show debug data.

## Debugger

We can use `pause()` to pause a pwntools script

# Useful commands

* `strings <file>` - find strings inside files
* `strace <program>` - syscall trace
* `ltrace <program>` - library trace
* `file <file>` / `objdump -f <file>` - Inspects the header of a file
* `objdump -d <program>` - Disassemble a program
  * Note: Uses AT&T syntax (left to right)
  * For Intel: `-M intel`
* `checksec <program>` - (PWNtools) Security feature detection
* `xxd <file>` - Hex editor

# pwndbg

* `stack`
* `s` - step
* `ni` - next instruction (run over the next instruction)
* `n` - next
* `si` - step instruction (explicitly step by next instruction)
* `fin` - finish a function
* `x <addr>` - examine
  * `x/10bx <addr>` - examine the next 10 bytes as hex
* `set *<address>=value` - Modify a value at an address
* `attach <pid>` - attach to a PID
* `context` - show useful stuff!

# Memory

* `esp` - stack pointer
* `ebp` - frame pointer
* `eax` - common return register

---
title: "Return Oriented Programming"
date: 2020-07-14T18:07:02+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# ROP

Return Oriented Programming is a turing-complete method of writing programs without writing any code (wooaaAAAhhh!!). It is able to delete NX protection and signed code checks

Instead of relying on a win function/shellcode; we take advantage of multibyte x86 instruction alignment, to chain together tiny functions to do a certain task.

This is done by using code that already exists in the program!

---

There are only a limited number of memory regions that can actually execute code.  

* ASLR makes it hard to find the heap and stack
* NX prevents the heap and stack from being executed

Angery!

But, the TEXT section is always in the same location - these are where our static libraries exist.  
One library is `libc`

## Gadgets

In x86, program instructions can be multiple bytes long.

> What if our program counter was in the middle of these bytes... haha jk...
What instruction would it then execute... kidding.... unless?

A **gadget** is a small set of instructions (which end with a a `ret`) that already exist in a program to do a small task.  

By **chaining** gadgets together, we could make the program do what we want!


* ret2code - calling functions defined in the program itself
* ret2libc - calling functions defined in libc
  * leak `system()` address
  * leak `/bin/sh` string address
* ret2XXX - calling functions defined in some part of the program
* ROP - calling functions you create yourself with gadgets

### pop pop ret

A `pop` `pop` `ret` gadget chain will clean up the stack by removing two items, then returning

## Finding Gadgets

### pwntools

```python
code = ELF("./program")
gadget = lambda x: next(code.search(asm(YOUR_ASSEMBLY_INSTRUCTION, os='linux', arch=code.arch)))

# p.elf.search('/bin/sh').next()
```

### Ropper

`ropper -f static --search 'pop eax; ret`

### libc

`libc.nullbyte.cat`

---

Sometimes we might not find exact gadgets that we need. We would need to work with the requirements of the existing gadgets

## ROPping

1) Work out what you want to execute
2) Find gadgets that you can chain together
3) ???
4) Profit

## Stack Pivots

_Sometimes ROP gadgets can get very large, bigger than the size of our buffer._  

A stack pivot is an instruction that either moves the stack pointer (by alot), or overwrites the ebp - as to move the program

### RETsled

If there are no useful stack pivoting gadgets, we could create use a RET sled

## ROP Automation

(Not allowed to use in the course but :shrug:)

* Symbolic Execution
  * Understands the effects of a gadget
* Constraint satisfaction problems
  * Generates the chains
* SAT Solver
  * Finds gadgets and chains such that the request is met.
  * Z3 SAT solver

## **angr**op

`angr` is a Python framework for analysing binaries.

`angrop` is an extension which finds ROP gadgets and chains.  
It uses constraint solving to generate and understand the effects of gadgets.
  
- Looks for dependencies of gadgets, and side effects


---

# One Gadgets

A single gadget that pops a shell :o.  
Often contains addresses

Useful in heap exploitation!

---
title: "Wargames 2"
date: 2020-06-08T12:00:00+10:00

categories: ["Wargames"]
hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

## jump

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week2/jump)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week2/solve-jump.py)]

### Scenario

The function address for the win function is given to us, which we need to execute somehow.

### Solution

We need to override the function pointer variable (`ebp - 0x8`) through the `gets` call. The distance between memory addresses of the function pointer variable and the string buffer (`ebp - 0x48`) is `0x40` bytes.  
We should send 0x40 bytes of pad followed by the address of the win function.

---

## blind

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week2/blind)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week2/solve-blind.py)]

### Scenario

A binary is given, without any immediately visible indicators.  

### Solution

Looking at the disassembly of the binary, there is a `win` function (`0x80484d6`), and a `vuln` function that is called by main. A `gets` call stores data into `ebp - 0x44` / `esp - 0x48`. We can perform a buffer overflow with `0x48` bytes of padding to modify the return address of `vuln` to our `win` function.

---

## Best Security

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week2/bestsecurity)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week2/solve-bestsecurity.py)]

### Scenario

A fixed-value stack canary of "1234" is hardcoded into the binary.

### Solution

The value of the canary is stored in `ebp - 0x5`, and the `gets` buffer is pointed to `ebp - 0x85`.  
We need to pad `0x80` bytes, then send "1234" in order to override the canary.

---

## Stack Dump

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week2/stack-dump)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week2/solve-stack-dump.py)]

### Scenario

The given binary file initialises a random-valued stack canary.  
When the quit function is called, the program checks if the stack canary has changed or not - crashing if it has.

### Solution

Through the given functions we need to override the return address to the win function, whilst maintaining the correct canary value.

* Buffer at `ebp - 0x68`
* Canary at `ebp - 0x8`
* Win function at `0x80486c6`

The stack pointer is revealed to us as the start of the program.  
Upon analysing the binary, we find that `esp = ebp - 0x71`.  
Likewise, `ebp = esp + 0x71`

We can leak the canary (`ebp - 0x8) by writing the address of the canary through the input data function, then calling the dump memory function. Once we have the canary, we can overflow the buffer with padding, the canary value, more padding and the win function address.

When the quit function is called, our buffer overflow ensures that the canary is the correct value, and hence proceeds and returns to our win function.

---

## Reverse Engineering

[[Disassembly](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week2/chall1.png)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week2/chall1.c)]

The function `main` performs a `scanf` call, which an the integer into the variable at address `ebp - 0xc`. This value is then compared to `0x539` (1337), which if true prints out _"Your so leet!"_, else _"Bye"_. The program returns with the status code `1`

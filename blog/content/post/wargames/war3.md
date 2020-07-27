---
title: "Wargames 3"
date: 2020-06-15T12:00:00+10:00

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

## simple

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week3/simple)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week3/solve-simple.py)]

### Scenario

The flag is opened with fd 1000, and our input shellcode is executed

### Solution

Write shellcode to use the read syscall to store the flag into our buffer (esp).  
Then write shellcode to print the flag from the buffer

---

## shellz

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week3/shellz)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week3/solve-shellz.py)]

### Scenario

We are given a buffer `0x2004` away from ebp, and a random address in the stack.  
We need to get a shell.

### Solution

To jump into our shellcode, we need to overwrite the return address by padding `0x2008` bytes.  
In our pad, we also need to write our shellcode which will setup a syscall for `execve("/bin/sh", NULL, NULL)`.  

For some reason, using `push` to store the string didn't work, so I ended up storing the string into the buffer during runtime

---

## Find Me

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week3/find-me)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week3/solve-find-me.py)]

### Scenario

We are given two buffers (0x14 and 0x100 bytes), of which the first buffer is executed.  
This would give us only 19 bytes (20 bytes, inclusive of a NULL terminator) to write a piece shellcode that would be around 36 bytes long!

### Solution

Write an egghunter (at most 19 bytes long) to find the address bigger buffer, where we can write our shellcode.  
The bigger buffer would read from fd 1000 and print out the flag

---

## Reverse Engineering

[[Disassembly](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week3/chall2.png)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week3/chall2.c)]

The function `main` creates a loop over a counter (initially 0). The loop increments by 1 until it reaches 10. During the loop, if the current number is odd (LSB is 1), then the number is printed out with printf. The program returns with the status code `1`.

The format string of printf is not disclosed, and we will assume it to be `"%d\n"`

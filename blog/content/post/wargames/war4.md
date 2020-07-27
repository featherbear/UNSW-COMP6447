---
title: "Wargames 4"
date: 2020-06-23T12:00:00+10:00

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

## Door

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week4/door)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week4/solve-door.py)]

### Scenario

There is a vulnerable printf function that is 0x200 bytes long.  
There are four bytes at ebp-0x5 that need to be overwritten to 'A', 'P', 'E', 'S'

### Solution

Perform a format string attack with the vulnerable printf function to overwrite the four bytes.  
When overwriting byte-by-byte, `%hhn` should be used.  
An offset of 1 byte was required to byte-align the values.

---

## Snake

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week4/snake)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week4/solve-snake.py)]

### Scenario

In the main program loop, there is a stack address leakable through the Print Flag option - if you enter the password.  
There is no win function, and the flag address probably doesn't have a flag... But we do have a vulnerable `gets` function, and an executable stack :hm:...

### Solution

A static analysis of the program reveals that any password greater than 0x50 bytes long is considered correct.  
From here, we learn about an address on the stack; which we can use to find the ebp and esp addresses for that frame.  
There is a vulnerable `gets` function in the `get_name` function, which we can populate with shellcode to launch a shell.  
To overflow the return address, we can find out (I'm not too sure how exactly to determine this, but I compared values during runtime with gdb) that the ebp address for the new frame is 0x78 bytes away from the calling frame - so we can do some maths to figure out the address of the start of the buffer. By overflowing the buffer and the return address, we can execute our shellcode to get the flag

---

## For Matrix

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week4/formatrix)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week4/solve-formatrix.py)]

### Scenario

There is a format string vulnerable `sprintf` function that allows a user to enter in up to 512 bytes.  
This format string will then be evaluated, meaning that we can override either the `puts` or `printf` GOT entry to point to the `win` function.

### Solution

We have a choice of either overwriting the `puts` or `printf` function.  
The `win` function however, also uses the `puts` function. So as to prevent an infinite loop, we'll override the `printf` function instead.  

We can push the four addresses of the bytes containing the `printf` GOT entry, and then write in the bytes with `%hhn`.  

---

## Sploitwarz

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week4/sploitwarz)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week4/solve-sploitwarz.py)]

### Scenario

The program has a win address that we need to jump to, either by means of overriding the return address, or by some other means...  
PIE and the NX bit is enabled, however RELRO is disabled... Hmm.. GOT?  
The program has a vulnerable printf function that occurs in the `do_gamble` function

### Solution

The vulnerable printf function occurs when the correct guess is made in the `do_gamble` function. We can reach this outcome by spamming the same guess choice until it matches.  
We can then leak the stack with `%p` to find out that the third entry on the stack contains an address that belongs to the program code. This allows us to counter the PIE protection as are able to find the program base address. We can then find the addresses of the `win` function as well as the address for `printf@GOT`, and modify the GOT table to call our win function when printf is called.

---
title: "Wargames 6"
date: 2020-07-12T12:00:00+10:00

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

## swrop

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week7/swrop)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week7/solve-swrop.py)]

### Scenario

The program contains a `read()` function that is vulnerable to a buffer overflow attack. The program also contains a `system()` function and `"/bin/sh"` string

### Solution

As PIE is disabled, the address of `system()` (or a call to system) can be found through static analysis. We can overflow the return address of the `vulnerable_function` function, and push the `"/bin/sh"` string address onto the stack to exploit.

---

## static

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week7/static)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week7/solve-static.py)]

### Scenario

The program contains a whole lot of library functions (embedded rather than linked). It has a vulnerable `gets()` function which allows us to overwrite the return address. There is no `"/bin/sh"` string within the binary.

### Solution

The `0x080a8cb6: pop eax; ret;` instruction does not work as it contains an `0x0a` byte (newline character) - which will cause `gets()` to finish reading. To work around this problem, we can `pop edx`, then `mov eax, edx`.

The `0x0806ee5b: push eax; adc al, 0x7c; and dword ptr [esi + 0x1a], edi; pop ebx; ret;` instruction can get around this `gets()` newline limitation, but... nah.

As there is no `"/bin/sh"` string, we will need to load it into the memory through a series of `pop ...` and `mov [...], ...` instructions.

The registers can then be modified to launch an `execve` syscall.

---

## roproprop

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week7/roproprop)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week7/solve-roproprop.py)]

### Scenario

The program has PIE enabled, meaning that an address leak is required to calculate offsets in the program. Libc is linked to this binary, so functions and gadgets can be found from the libc library.

### Solution

The the address of `setbuf` is given, which has an offset of `0x65ff0` from the libc base. This allows us to calculate the runtime address of the `system()` function, as well as the runtime address of the `"/bin/sh"` string.

---

## ropme

[[Binary](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week7/ropme)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week7/solve-ropme.py)]

### Scenario

The binary has a vulnerable `fgets()` function; however there are few gadgets that were found which would allow us to create an `execve("/bin/sh", ...)` call. There are also few gadgets which allow us to easily manipulate the `eax`, `ecx` and `edx` registers. The flag file is however opened at `fd 3`...

### Solution

Using the `read` and `write` syscalls, we can write from the flag (`fd 3`) into a buffer located at `ecx`. Thankfully `ecx` contains the buffer used in and returned from `fgets()`. The flag can then be written out from the buffer to `stdout` (`fd 1`).

---

## Reversing Challenge

[[Disassembly](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week7/re.png)]  
[[Solution](https://github.com/featherbear/UNSW-COMP6447/raw/master/wargames/week7/re.c)]

The disassembly shows a function that performs a number of memory allocation, and modifications to that memory. If a memory allocation fails, the program exits with a status code of `1`.

A struct is supposedly defined to have a `char` value and a pointer to another node (linked list!). Each time a new struct is defined, it is made the 'head' of the list, and the previous head is attached to the node. The 10 nodes are assigned a data value from 'A' to 'J' respectively.  

The program seems to have a bug, which causes the nodes in the list to unlink themselves (`mov dword ptr [eax + 4], 0`).  
This is likely Adam's fault :) and can be fixed by making the change in the below source code

```c
# OLD
node->next = 0;
---
# NEW
node->value = 0;
```

Alternatively, the statement can be removed as it is reassigned immediately after.

At the end of the loop, the head of the list is returned.

---
title: "Shellcode"
date: 2020-06-16T19:05:23+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

> Normal programs don't have a win function :(.  
Make our own!

Shellcode is a piece of machine code that contains assembly instructions to give us control.

`payload = shellcode + address of shellcode`

**Shellcodes are position independent**

# Writing shellcode

* Write the ASM by hand, and assemble using NASM, then extract the bytes
* Write test code in C
* pwntools + python = win
  * `asm()`

# Uses of shell code

* Reverse shell
* Socket reuse
* Egghunter - small bit of shellcode (egg)
  * An omelette egghunter finds the eggs (identifiable signature) and combines them together
* Download a second stage (larger payload)

# Egghunter

Often we don't have enough space to write meaningful code.  
When injecting shellcode in larger memory regions - We don't know where it is.

With an egghunter, we can write code to search for the larger shellcode and execute it.  
We can do this by adding a 'signature' to identify the data as our shellcode

# System Calls

System calls are executed through their syscall number.

number - `eax`  
1 - `ebx`  
2 - `ecx`  
3 - `edx`  
4 - `esx`  
5 - `edi`

# Strings

* To call `system("/bin/sh")` we need to somehow put the string "/bin/sh"
* We should try to avoid using null-bytes in our shellcode, because the calling function might handle null bytes differently (i.e. `strcpy` stops when it reads a null byte)

## Workarounds

* `"/bin/sh"` -> `"/bin//sh"` so that two full push instructions can be written.  
* If we need a null byte, we could use write the shellcode for a clear/xor instruction.

## Usage

> **Shellcodes are position independent**

* Approach one - Push string onto stack, then use value of esp 
* Approach two - Add the string to the end of your shellcode, then offset from the address of your shellcode

# NOP Sled

When we don't know the exact address of our shellcode, we can add some `nop` (`0x90`) instructions - which do nothing, but move to the next address.  

If firewalls detect and block `NOP*1000`, we could use other useless 1-byte instructions.

---

# Preventing shellcode

`mprotect` can disable the executability of a memory region by adding the NX bit - preventing shellcode

## Circumventing the NX bit

// Next time :)

# Other

* Syscall proxy
* Mosdef 


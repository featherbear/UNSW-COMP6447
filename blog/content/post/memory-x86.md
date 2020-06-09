---
title: "Memory in x86 Systems"
date: 2020-06-09T18:19:43+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

Registers in the x86 processor are 32 bits wide.

* 4 general purpose registers
  * EAX, EBX, ECX, EDX
  * The upper 8 bits of the lower 16 bits can be accessed with AH, BH, CH, DH
  * The lower 8 bits of the lower 16 bits can be accessed with AL, BL, CL, DL
* ESI - Another general purpose register
* EDI - Another general purpose register
* ESP - stack pointer
* EBP - base pointer
* EFLAGS - Status Register
* EIP - Instruction pointer

---

# Stack Frames

* Stack grows down

* Stack pointer points to the top of the stack
* Frame pointer points to the start of the stack

* In x86, it is the responsibility of the caller to set up the arguments in the stack for the function to be called
  * The caller is also responsible to remove the arguments in the stack

* Prologue - Pushing items setting up the stack
* Epilogue - Tearing down the stack

* The `ret` function will pop the last item on the stack and put it onto the stack

---

# Use Intel syntax in gdb

> `echo "set disassembly-flavor intel" >> ~/.gdbinit`

---

* eax = ebx -> `mov eax, ebx`
* eax = *ebx -> `mov eax, [ebx]`
* eax = *(ebx+4) -> `mov eax, [ebx+4]`

---

LEA -> Get address / dereference

`lea ebx, [ecx+4]` == `mov ebx, ecx` -> `add ebx, 4`



--- 

# cdecl

```
function(a,b,c)

-> push c
-> push b
-> push a
-> call function
-> add esp, 0ch ; add 0x0c to the esp to clean up the stack
```


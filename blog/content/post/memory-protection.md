---
title: "Memory Protection"
date: 2020-06-23T20:28:29+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# Prevention

* Stack reorder, randomised padding
* Canary
* FORTIFY
* RELRO
* Write good code

# Mitigation

* ASLR / PIE Randomisation
* NX
* Pointer Authentication
* Hypervisor

Use `checksec` to figure out what memory protection technologies are applied to a given binary


# Address Space Layout Randomisation - ASLR

A system-wide setting that randomises the base of the stack and heap.  

When a new process executes, each memory region gets an ASLR slide - random number (aligned to a boundary with a final byte of 00).

* Does not affect functions (which belong in the code segment)
* Pwndbg disables ASLR by default

* Attempts to increase entropy, have to guess XX bits

# Position Independent Execution - PIE

* Randomises the base address of the text and code regions (related to the program)
* **Requires ASLR** to be enable for it to be effective.

To beat PIE, we need to be able to leak an address in the required memory region, and through static analysis - find the base address. Since items _inside_ the same memory region is still relative (only the base is randomised), we can find addresses to other items in that same memory address.

# No eXecute Bits - NX bits

Prevents the stack from being executed.  
Set by the compiler, enforced by hardware

To beat the NX bit we can use RIP / RET2code / RET2libc

# RELocation Read Only - RELRO

* Makes the GOT read-only
* Partial RELRO
  * Useless
* Full RELRO
  * GOT is read-only

# FORTIFY

Adds some checks into the program, to attempt to detect possible buffer overflows

* Only allows `%n` to be used in a format string if the string is in read-only memory

# Pointer Authentication (PAC)

Detect pointers created by an external entity.  
Jumped to a signed version of an address, which needs to be verified (pointer + secret key (process context) + some third value(current stack pointer))

---

# Patterns

There are some common patterns

`0x565...` - Binary base when PIE is enabled  
`0x804...` - Binary base when PIE is disabled  
`0xF7...` - Library base  
`0xFF...` - Stack base  

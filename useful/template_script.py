#!/usr/bin/python3

"""
> Insert checksec output here <
"""

binary_path = ""
remote_addr = ('host', 'port')

#############################
from pwn import *;DEBUG=context.log_level==logging.DEBUG;p=process(binary_path);elf=p.elf;p=remote(*remote_addr) if args["REMOTE"] else p;
#############################

# Exploit

addr = dict()
offs = dict()

p.interactive()
